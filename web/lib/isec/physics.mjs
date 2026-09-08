import RAPIER from '@dimforge/rapier3d-compat';
export async function createPhysics(data){
 await RAPIER.init();
 const world=new RAPIER.World({x:0,y:-9.81,z:0});world.timestep=1/60;
 world.createCollider(RAPIER.ColliderDesc.trimesh(new Float32Array(data.vertices),new Uint32Array(data.indices)));
 const body=world.createRigidBody(RAPIER.RigidBodyDesc.kinematicPositionBased().setTranslation(12,.9,-7));
 const collider=world.createCollider(RAPIER.ColliderDesc.capsule(.55,.28),body);
 const controller=world.createCharacterController(.015);controller.enableAutostep(.23,.10,false);controller.enableSnapToGround(.26);controller.setMaxSlopeClimbAngle(Math.PI/4);controller.setMinSlopeSlideAngle(Math.PI/3);
 let velocityY=0;world.step();
 return {
  world,body,controller,
  reset(x,y,z){body.setTranslation({x,y:y+.86,z},true);body.setNextKinematicTranslation({x,y:y+.86,z});velocityY=0;world.step();},
  step(dx,dz,dt=1/60){
   velocityY=controller.computedGrounded()?-1.5:Math.max(-12,velocityY-9.81*dt);
   controller.computeColliderMovement(collider,{x:dx,y:velocityY*dt,z:dz});
   const d=controller.computedMovement(),p=body.translation();body.setNextKinematicTranslation({x:p.x+d.x,y:p.y+d.y,z:p.z+d.z});world.step();return body.translation();
  },
  feet(){const p=body.translation();return {x:p.x,y:p.y-.83,z:p.z};},
  dispose(){world.free();}
 };
}
