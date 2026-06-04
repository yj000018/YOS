import { Composition } from 'remotion';
import { MorningEdition } from './compositions/MorningEdition';
import { HeadlineTicker } from './compositions/HeadlineTicker';

export const Root: React.FC = () => {
  return (
    <>
      {/* 30s Headline Ticker — 16:9 for web/social */}
      <Composition
        id="HeadlineTicker"
        component={HeadlineTicker}
        durationInFrames={900}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ lang: 'en', date: 'April 4, 2027' }}
      />

      {/* 30s Morning Edition — 9:16 vertical (story/reel format) */}
      <Composition
        id="MorningEdition"
        component={MorningEdition}
        durationInFrames={900}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ lang: 'en', date: 'April 4, 2027' }}
      />
    </>
  );
};
