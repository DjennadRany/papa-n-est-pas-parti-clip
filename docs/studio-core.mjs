// Pure, browser/Node-compatible timeline helpers.
export function validateScenes(scenes) {
  if (!Array.isArray(scenes) || !scenes.length) throw Error("Aucune scène");
  const ordered=[...scenes].sort((a,b)=>a.start-b.start);
  for (const [i,s] of ordered.entries()) {
    if (!Number.isFinite(s.start)||!Number.isFinite(s.end)||s.end<=s.start) throw Error("Durée invalide: plan "+s.id);
    if (i && Math.abs(ordered[i-1].end-s.start)>0.01) throw Error("Raccord manquant: plan "+s.id);
  }
  return ordered;
}
export function makeTimeline(files,duration) {
  if (!files.length || !Number.isFinite(duration)||duration<=0) throw Error("Images et durée audio requises");
  return files.map((file,i)=>({id:i+1,title:file.name||"Plan "+(i+1),start:i*duration/files.length,end:(i+1)*duration/files.length,image:file.name}));
}
export function frameAt(scenes,time) {
  return scenes.find(s=>time>=s.start && time<s.end) || scenes[scenes.length-1];
}
export function outputMime(supported) {
  for (const m of ["video/mp4;codecs=avc1.42E01E,mp4a.40.2","video/webm;codecs=vp9,opus","video/webm;codecs=vp8,opus","video/webm"]) if(supported(m)) return m;
  return "";
}

/** Deterministic CPU/browser keyframe interpolation for scene-specific camera direction. */
export function cameraAt(keyframes, progress) {
  if (!Array.isArray(keyframes) || keyframes.length < 2) throw Error("Deux images-clés minimum");
  const frames=[...keyframes].sort((a,b)=>a.t-b.t);
  for(const frame of frames) {
    if(!Number.isFinite(frame.t)||frame.t<0||frame.t>1||!Number.isFinite(frame.x)||!Number.isFinite(frame.y)||!Number.isFinite(frame.zoom)||frame.zoom<1) throw Error("Image-clé invalide");
  }
  const t=Math.min(1,Math.max(0,progress));
  let right=frames.findIndex(f=>f.t>=t);
  if(right<0)right=frames.length-1;
  if(right===0)return {...frames[0]};
  const a=frames[right-1],b=frames[right];
  const u=b.t===a.t?1:(t-a.t)/(b.t-a.t);
  const ease=u*u*(3-2*u);
  return {t,x:a.x+(b.x-a.x)*ease,y:a.y+(b.y-a.y)*ease,zoom:a.zoom+(b.zoom-a.zoom)*ease};
}
export function cameraPreset(effect) {
  if(effect==="zoom")return [{t:0,x:0,y:0,zoom:1.02},{t:1,x:0,y:0,zoom:1.12}];
  if(effect==="pan")return [{t:0,x:-0.55,y:0,zoom:1.14},{t:1,x:0.55,y:0,zoom:1.14}];
  if(effect==="rise")return [{t:0,x:0,y:0.55,zoom:1.14},{t:1,x:0,y:-0.55,zoom:1.14}];
  if(effect==="orbit")return [{t:0,x:-0.4,y:0.2,zoom:1.13},{t:0.5,x:0.35,y:-0.2,zoom:1.17},{t:1,x:0.4,y:0.2,zoom:1.13}];
  return [{t:0,x:0,y:0,zoom:1},{t:1,x:0,y:0,zoom:1}];
}
