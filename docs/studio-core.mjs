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
