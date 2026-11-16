import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import timeline from '../scenes.json';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'};
const gold = '#ffd17e';

const Scene = ({scene, length}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = Math.min(1, frame / Math.max(1, length - 1));
  const isDragon = scene.id >= 17 && scene.id <= 19;
  const isDark = [13,14,15,16,24].includes(scene.id);
  const isQuiet = [1,3,8,9,14,15,22,23,24].includes(scene.id);
  const zoom = interpolate(p, [0,1], isDragon ? [1.04,1.23] : isQuiet ? [1.04,1.12] : [1.07,1.17], clamp);
  const direction = scene.id % 3 === 0 ? -1 : 1;
  const x = interpolate(p,[0,1], [-25 * direction, 25 * direction],clamp);
  const y = interpolate(p,[0,1], [scene.id % 2 ? 12 : -12, scene.id % 2 ? -12 : 12],clamp);
  const edge = Math.min(10, Math.floor(length / 6));
  const opacity = Math.min(1, Math.max(0, frame / Math.max(1, edge)), Math.max(0, (length - frame) / Math.max(1, edge)));
  const breathing = Math.sin(frame / fps * (isDragon ? 9 : 2.3));
  const glow = isDragon ? 0.15 + 0.12 * Math.max(0, breathing) : 0.04 + 0.025 * breathing;
  const particles = Array.from({length: isDragon ? 24 : 11}, (_,i) => {
    const seed = (i * 97 + scene.id * 31) % 101;
    const px = (i * 157 + scene.id * 37) % 1920;
    const py = (i * 251 + scene.id * 41) % 1080;
    const drift = ((frame * (0.14 + (i % 4) * 0.1)) + seed * 8) % 1200;
    return <div key={i} style={{position:'absolute',left:px,top:(py - drift + 1200)%1200 - 40,width:i%6===0?7:3,height:i%6===0?7:3,borderRadius:20,background:gold,opacity:(isDark?0.43:0.3)*(0.5+0.5*Math.sin(frame/12+i)),boxShadow:'0 0 12px 2px rgba(255,211,134,.65)',pointerEvents:'none'}}/>;
  });
  const titleCard = scene.id === 24;
  return <AbsoluteFill style={{backgroundColor: '#080f19',opacity,overflow:'hidden'}}>
    <Img src={staticFile(scene.image)} style={{position:'absolute',width:'100%',height:'100%',objectFit:'cover',transform:`translate(${x}px,${y}px) scale(${zoom})`,filter:isDark?'brightness(.82) saturate(1.09)':'saturate(1.08) contrast(1.035)'}}/>
    <AbsoluteFill style={{background:'linear-gradient(180deg,rgba(9,16,27,.22),transparent 28%,transparent 65%,rgba(8,10,28,.20))'}}/>
    {particles}
    {(isDragon||scene.id===16) && <AbsoluteFill style={{mixBlendMode:'screen',background:`radial-gradient(circle at ${50+Math.sin(frame/11)*16}% 50%, rgba(255,190,88,${glow}),transparent 44%)`}}/>}
    {scene.id===2 && <AbsoluteFill style={{background:'linear-gradient(90deg, transparent 45%,rgba(255,218,145,.13) 50%,transparent 55%)',transform:`translateX(${interpolate(p,[0,1],[-820,800],clamp)}px)`}}/>}
    {titleCard && <AbsoluteFill style={{justifyContent:'flex-end',alignItems:'center',paddingBottom:105}}><div style={{fontFamily:'Georgia,serif',fontSize:45,fontWeight:600,color:'#fff0cf',textAlign:'center',textShadow:'0 2px 12px #09101c',maxWidth:1450}}>Papa a pensé à toi chaque jour. Il a cherché à te revoir.<br/>Les grandes personnes s’occupent du pont.<br/>Toi, tu peux continuer à jouer.</div></AbsoluteFill>}
  </AbsoluteFill>;
};

export const PapaClip = () => <AbsoluteFill style={{backgroundColor:'#0c1421'}}>
  {timeline.scenes.map((scene) => {
    const from = Math.round(scene.start * timeline.fps);
    const to = Math.round(scene.end * timeline.fps);
    return <Sequence key={scene.id} from={from} durationInFrames={to-from}>
      <Scene scene={scene} length={to-from}/>
    </Sequence>;
  })}
  <Audio src={staticFile('assets/audio/song.mp3')}/>
</AbsoluteFill>;
