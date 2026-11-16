import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, staticFile} from 'remotion';
import timeline from '../scenes.json';

// Each shot is a real AI-generated MP4. The timeline follows start times, not IDs.
// Every shot is retimed to its musical window. No still-image fallback.
export const PapaClip = () => (
  <AbsoluteFill style={{backgroundColor:'#080e1a'}}>
    {[...timeline.scenes].sort((a,b)=>a.start-b.start).map(scene => {
      const from=Math.round(scene.start*timeline.fps);
      const to=Math.round(scene.end*timeline.fps);
      const frames=to-from;
      const duration=frames/timeline.fps;
      const speed=3.5/duration;
      return <Sequence key={scene.id} from={from} durationInFrames={frames}>
        <AbsoluteFill>
          <OffthreadVideo
            src={staticFile('assets/video/'+String(scene.id).padStart(2,'0')+'.mp4')}
            playbackRate={speed}
            muted
            style={{width:'100%',height:'100%',objectFit:'cover'}}
          />
        </AbsoluteFill>
      </Sequence>;
    })}
    <Audio src={staticFile("assets/audio/Papa n'est pas parti(1).mp3")}/>
  </AbsoluteFill>
);
