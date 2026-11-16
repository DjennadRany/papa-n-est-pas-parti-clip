import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, staticFile} from 'remotion';
import timeline from '../scenes.json';

// Every scene must have a generated video. Missing footage is an error, not a slideshow fallback.
export const PapaClip = () => <AbsoluteFill style={{backgroundColor:'#080e1a'}}>
  {timeline.scenes.map(scene => {
    const from=Math.round(scene.start*timeline.fps);
    const to=Math.round(scene.end*timeline.fps);
    const frames=to-from;
    const playbackRate=3.5/(frames/timeline.fps);
    return <Sequence key={scene.id} from={from} durationInFrames={frames}>
      <AbsoluteFill>
        <OffthreadVideo
          src={staticFile('assets/video/'+String(scene.id).padStart(2,'0')+'.mp4')}
          playbackRate={playbackRate}
          muted
          style={{width:'100%',height:'100%',objectFit:'cover'}}
        />
      </AbsoluteFill>
    </Sequence>;
  })}
  <Audio src={staticFile("assets/audio/Papa n'est pas parti(1).mp3")}/>
</AbsoluteFill>;
