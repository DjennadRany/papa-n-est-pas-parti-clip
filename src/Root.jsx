import React from 'react';
import {Composition} from 'remotion';
import {PapaClip} from './Clip';
import timeline from '../scenes.json';

export const Root = () => (
  <Composition
    id="PapaClip"
    component={PapaClip}
    durationInFrames={Math.ceil(timeline.duration_seconds * timeline.fps)}
    fps={timeline.fps}
    width={timeline.width}
    height={timeline.height}
  />
);
