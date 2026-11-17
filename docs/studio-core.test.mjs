import test from "node:test";
import assert from "node:assert/strict";
import {validateScenes,makeTimeline,frameAt,outputMime,cameraAt,cameraPreset} from "./studio-core.mjs";
test("audio duration distributed across images",()=>{
 const scenes=makeTimeline([{name:"01.jpg"},{name:"02.jpg"}],10);
 assert.equal(scenes[0].end,5);assert.equal(scenes[1].end,10);
 assert.equal(frameAt(scenes,8).id,2);
});
test("reject invalid inputs and discontinuity",()=>{
 assert.throws(()=>makeTimeline([],10));assert.throws(()=>makeTimeline([{name:"a"}],0));
 assert.throws(()=>validateScenes([{id:1,start:0,end:2},{id:2,start:3,end:4}]));
});
test("prefer mp4 only when supported",()=>{
 assert.match(outputMime(x=>x.startsWith("video/webm")),/webm/);
 assert.match(outputMime(()=>true),/mp4/);
 assert.equal(outputMime(()=>false),"");
});

test("CPU keyframe interpolation is bounded, deterministic and smooth",()=>{
  const keys=cameraPreset("pan");
  assert.equal(cameraAt(keys,0).x,-0.55);
  assert.equal(cameraAt(keys,1).x,0.55);
  assert.ok(Math.abs(cameraAt(keys,0.5).x)<1e-9);
  assert.deepEqual(cameraAt(keys,-10),cameraAt(keys,0));
  assert.deepEqual(cameraAt(keys,10),cameraAt(keys,1));
  assert.throws(()=>cameraAt([{t:0,x:0,y:0,zoom:0}],0));
  for(const effect of ["zoom","pan","rise","orbit","none"]){
    for(let i=0;i<=100;i++) {
      const f=cameraAt(cameraPreset(effect),i/100);
      assert.ok(f.zoom>=1);
      assert.ok(Number.isFinite(f.x)&&Number.isFinite(f.y));
    }
  }
});
