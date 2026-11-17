import test from "node:test";
import assert from "node:assert/strict";
import {validateScenes,makeTimeline,frameAt,outputMime} from "./studio-core.mjs";
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
