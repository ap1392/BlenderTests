import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
// @ts-ignore shared module is also exercised by the Node navigation tests
import {createPhysics} from './physics.mjs';
export async function createWalkthrough(host:HTMLDivElement,report:(s:any)=>void){
 const renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'});renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setSize(host.clientWidth,host.clientHeight);renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;host.appendChild(renderer.domElement);
 const scene=new THREE.Scene();scene.background=new THREE.Color('#d6e2eb');
 const pmrem=new THREE.PMREMGenerator(renderer),env=pmrem.fromScene(new RoomEnvironment(),.04);scene.environment=env.texture;scene.environmentIntensity=.35;
 scene.add(new THREE.HemisphereLight(0xf0f5ff,0xb2a793,2.1));
 const sun=new THREE.DirectionalLight(0xfff1db,2);sun.position.set(10,35,15);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-40;sun.shadow.camera.right=40;sun.shadow.camera.top=40;sun.shadow.camera.bottom=-40;sun.shadow.normalBias=.025;scene.add(sun);
 const fill=new THREE.DirectionalLight(0xe1efff,.8);fill.position.set(-20,12,-15);scene.add(fill);
 const camera=new THREE.PerspectiveCamera(70,host.clientWidth/host.clientHeight,.07,220);camera.rotation.order='YXZ';
 const decoder=new DRACOLoader();decoder.setDecoderPath('/draco/');const loader=new GLTFLoader();loader.setDRACOLoader(decoder);
 report({status:'Loading architecture…'});
 const [gltf,data]=await Promise.all([loader.loadAsync('/models/ISEC.glb'),fetch('/models/collision.json').then(r=>{if(!r.ok)throw Error('Collision data could not load');return r.json();})]);
 gltf.scene.traverse((o:any)=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;const m=o.material;
  if(m.name.includes('glazing')){o.material=new THREE.MeshStandardMaterial({color:0xd3e4eb,transparent:true,opacity:.13,roughness:.1,metalness:.15,side:THREE.DoubleSide,depthWrite:false});o.renderOrder=2;o.castShadow=false;}
  else {m.side=THREE.DoubleSide;if(m.emissiveIntensity>0)m.emissiveIntensity=Math.min(m.emissiveIntensity,.8);}
 }});scene.add(gltf.scene);
 const physics=await createPhysics(data);let yaw=2.1,pitch=.23,active=false,drag=false,alive=true,frame=0,last=performance.now(),accumulator=0,statTime=0;
 const keys=new Set<string>();physics.reset(12,0,-7);
 function resize(){renderer.setSize(host.clientWidth,host.clientHeight);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();}
 function lockChange(){active=document.pointerLockElement===renderer.domElement;keys.clear();report({active});}
 function keydown(e:KeyboardEvent){if(['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','ShiftLeft'].includes(e.code)){keys.add(e.code);if(active)e.preventDefault();}if(e.code==='Escape'){active=false;drag=false;keys.clear();report({active:false});}}
 function keyup(e:KeyboardEvent){keys.delete(e.code);}
 function look(e:MouseEvent){if(document.pointerLockElement===renderer.domElement||drag){yaw-=e.movementX*.002;pitch=Math.max(-1.45,Math.min(1.45,pitch-e.movementY*.002));}}
 async function enter(){try{await renderer.domElement.requestPointerLock();}catch{active=true;report({active:true,status:'Drag to look · WASD to walk'});}}
 function down(){if(active)drag=true;else void enter();}function up(){drag=false;}function blur(){keys.clear();drag=false;}
 window.addEventListener('resize',resize);document.addEventListener('pointerlockchange',lockChange);window.addEventListener('keydown',keydown);window.addEventListener('keyup',keyup);window.addEventListener('mousemove',look);renderer.domElement.addEventListener('mousedown',down);window.addEventListener('mouseup',up);window.addEventListener('blur',blur);
 function tick(now:number){if(!alive)return;const delta=Math.min((now-last)/1000,.1);last=now;accumulator+=delta;
  while(accumulator>=1/60){
   const f=active?(Number(keys.has('KeyW')||keys.has('ArrowUp'))-Number(keys.has('KeyS')||keys.has('ArrowDown'))):0;
   const r=active?(Number(keys.has('KeyD')||keys.has('ArrowRight'))-Number(keys.has('KeyA')||keys.has('ArrowLeft'))):0;
   const scale=(keys.has('ShiftLeft')?2.5:1.8)/60/Math.max(1,Math.hypot(f,r));
   physics.step((-Math.sin(yaw)*f+Math.cos(yaw)*r)*scale,(-Math.cos(yaw)*f-Math.sin(yaw)*r)*scale);accumulator-=1/60;
  }
  const p=physics.feet();camera.position.set(p.x,p.y+1.65,p.z);camera.rotation.set(pitch,yaw,0);renderer.render(scene,camera);
  if(now-statTime>500){report({level:Math.max(1,Math.min(6,Math.round(p.y/4.2)+1)),fps:Math.round(1/Math.max(.001,delta)),position:p});statTime=now;}
  frame=requestAnimationFrame(tick);
 }
 frame=requestAnimationFrame(tick);report({ready:true,status:'',active:false});
 const lifecycle=new AbortController();
 const api={enter,view(level:number){keys.clear();physics.reset(level===1?12:10,(level-1)*4.2,level===1?-7:0);yaw=2.1;pitch=.12;},dispose(){lifecycle.abort();alive=false;cancelAnimationFrame(frame);window.removeEventListener('resize',resize);document.removeEventListener('pointerlockchange',lockChange);window.removeEventListener('keydown',keydown);window.removeEventListener('keyup',keyup);window.removeEventListener('mousemove',look);window.removeEventListener('mouseup',up);window.removeEventListener('blur',blur);physics.dispose();gltf.scene.traverse((o:any)=>{if(o.isMesh){o.geometry.dispose();o.material.dispose();}});renderer.dispose();pmrem.dispose();env.dispose();decoder.dispose();renderer.domElement.remove();}};
 const mc=(document as any).modelContext;
 if(mc?.registerTool){
  const register=(tool:any)=>Promise.resolve(mc.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});
  register({name:'read_walkthrough_position',description:'Read the current floor and position in the ISEC walkthrough.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute(){return {position:physics.feet(),level:Math.max(1,Math.min(6,Math.round(physics.feet().y/4.2)+1))};}});
  register({name:'view_atrium_floor',description:'Move to the same gallery viewpoint as the floor buttons in the walkthrough menu.',inputSchema:{type:'object',properties:{floor:{type:'integer',minimum:1,maximum:6}},required:['floor'],additionalProperties:false},execute(input:any){if(!Number.isInteger(input.floor)||input.floor<1||input.floor>6)throw Error('Floor must be 1 through 6');api.view(input.floor);return new Promise(resolve=>requestAnimationFrame(()=>resolve({floor:input.floor})));}});
  register({name:'walk_in_atrium',description:'Walk up to five meters forwards, backwards, left, or right using the same collision controller as WASD.',inputSchema:{type:'object',properties:{direction:{type:'string',enum:['forward','backward','left','right']},meters:{type:'number',minimum:.05,maximum:5}},required:['direction','meters'],additionalProperties:false},execute(input:any){if(!['forward','backward','left','right'].includes(input.direction)||!Number.isFinite(input.meters)||input.meters<.05||input.meters>5)throw Error('Invalid direction or distance');const f=input.direction==='forward'?1:input.direction==='backward'?-1:0;const r=input.direction==='right'?1:input.direction==='left'?-1:0;const n=Math.ceil(input.meters/.025),d=input.meters/n;for(let i=0;i<n;i++)physics.step((-Math.sin(yaw)*f+Math.cos(yaw)*r)*d,(-Math.cos(yaw)*f-Math.sin(yaw)*r)*d);return new Promise(resolve=>requestAnimationFrame(()=>resolve({position:physics.feet()})));}});
 }
 return api;
}
