import fs from 'node:fs';import {createPhysics}from '../lib/isec/physics.mjs';
const data=JSON.parse(fs.readFileSync(new URL('../public/models/collision.json',import.meta.url)));
const p=await createPhysics(data);let report=[];
const settle=()=>{for(let i=0;i<120;i++)p.step(0,0);};
function walk(x,z,max=1200){for(let i=0;i<max;i++){const q=p.feet();const d=Math.hypot(x-q.x,z-q.z);if(d<.06)return true;p.step((x-q.x)/d*.025,(z-q.z)/d*.025);}return false;}
for(let l=0;l<6;l++){p.reset(l?10:12,l*4.2,l?0:-7);settle();const q=p.feet();report.push({test:'Stable floor '+(l+1),pass:Math.abs(q.y-l*4.2)<.09,position:q});}
// North wall: a long attempted walk must stop at the classroom boundary.
p.reset(0,0,-13);settle();walk(0,-25,800);report.push({test:'Closed classroom boundary',pass:p.feet().z>-19,position:p.feet()});
// Upper interior lab glass should block crossing, even though transparent.
p.reset(10,4.2,-14);settle();walk(10,-8,700);report.push({test:'Lab glass blocks passage',pass:p.feet().z<-11.5&&Math.abs(p.feet().y-4.2)<.2,position:p.feet()});
// Stair centerline for a full upper turn, step heights and intermediate landings.
p.reset(2.24*Math.cos(-47*Math.PI/180),4.2,-2.24*Math.sin(-47*Math.PI/180));settle();let reached=0;
for(let i=1;i<=180;i++){const a=(-47+i*2)*Math.PI/180; if(!walk(2.24*Math.cos(a),-2.24*Math.sin(a),60))break;reached=i;}
report.push({test:'One upper spiral revolution',pass:reached===180&&Math.abs(p.feet().y-8.4)<.2,waypoints:reached,position:p.feet()});

for(let lev=2;lev<=4;lev++){
 let reached=0;for(let i=1;i<=180;i++){const a=(-47+i*2)*Math.PI/180;if(!walk(2.24*Math.cos(a),-2.24*Math.sin(a),60))break;reached=i;}
 report.push({test:'Continuous ascent to floor '+(lev+2),pass:reached===180&&Math.abs(p.feet().y-(lev+1)*4.2)<.2,position:p.feet()});
}
for(let lev=4;lev>=1;lev--){
 let reached=0;for(let i=1;i<=180;i++){const a=(-47-i*2)*Math.PI/180;if(!walk(2.24*Math.cos(a),-2.24*Math.sin(a),60))break;reached=i;}
 report.push({test:'Continuous descent to floor '+(lev+1),pass:reached===180&&Math.abs(p.feet().y-lev*4.2)<.2,position:p.feet()});
}
p.reset(10,4.2,0);settle();walk(10,-7,600);report.push({test:'Gallery railing prevents fall',pass:Math.abs(p.feet().y-4.2)<.15&&p.feet().z>-3,position:p.feet()});
p.reset(10,4.2,0);settle();walk(10,8,600);report.push({test:'Office partition stays closed',pass:Math.abs(p.feet().y-4.2)<.15&&p.feet().z<4,position:p.feet()});
p.reset(20,0,1);settle();walk(30,1,600);report.push({test:'Exterior glass blocks escape',pass:p.feet().x<24&&Math.abs(p.feet().y)<.15,position:p.feet()});
p.reset(-16.8,0,.8);settle();walk(-16.8,-7.2,900);report.push({test:'Broad stair ascends',pass:Math.abs(p.feet().y-4.2)<.18,position:p.feet()});

const lower=JSON.parse(fs.readFileSync(new URL('../../renders/validation/lower_stair_route.json',import.meta.url)));
p.reset(lower[0][0],0,lower[0][2]);settle();let count=0;
for(const [x,y,z] of lower){if(!walk(x,z,160))break;count++;}
report.push({test:'Lower sculptural stair ascent',pass:count===lower.length&&Math.abs(p.feet().y-4.2)<.2,waypoints:count,total:lower.length,position:p.feet()});
for(const [x,y,z] of [...lower].reverse()){if(!walk(x,z,160))break;}
report.push({test:'Lower sculptural stair descent',pass:Math.abs(p.feet().y)<.2,position:p.feet()});

p.reset(lower[0][0],0,lower[0][2]);settle();
let connected=true;for(const [x,y,z] of lower)connected=walk(x,z,180)&&connected;
for(const [x,z]of [[2.2,3.7],[2.1,2.7],[1.53,1.64]])connected=walk(x,z,240)&&connected;
report.push({test:'Ground stair connects to upper spiral',pass:connected&&Math.abs(p.feet().y-4.2)<.25,position:p.feet()});
p.reset(12,0,-7);settle();walk(11,-5,300);report.push({test:'Major furniture blocks passage',pass:Math.hypot(p.feet().x-11,p.feet().z+5)>.4,position:p.feet()});
console.log(JSON.stringify(report,null,2));fs.writeFileSync(new URL('../../renders/validation/navigation_report.json',import.meta.url),JSON.stringify(report,null,2));p.dispose();if(report.some(r=>!r.pass))process.exitCode=1;
