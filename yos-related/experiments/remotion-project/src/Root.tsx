import React from "react";
import { Composition, Series } from "remotion";
import { Seq01_Prologue, DURATION_SEQ01 } from "./sequences/Seq01_Prologue";
import { Seq02_Message, DURATION_SEQ02 } from "./sequences/Seq02_Message";
import { Seq03_AppelIA, DURATION_SEQ03 } from "./sequences/Seq03_AppelIA";
import { Seq04_LangagePere, DURATION_SEQ04 } from "./sequences/Seq04_LangagePere";
import { Seq05_Permutations, DURATION_SEQ05 } from "./sequences/Seq05_Permutations";
import { Seq06_Rotations, DURATION_SEQ06 } from "./sequences/Seq06_Rotations";
import { Seq07_Code, DURATION_SEQ07 } from "./sequences/Seq07_Code";
import { Seq08_Crypto, DURATION_SEQ08 } from "./sequences/Seq08_Crypto";
import { Seq09_Cosmos, DURATION_SEQ09 } from "./sequences/Seq09_Cosmos";
import { Seq10_Frequence, DURATION_SEQ10 } from "./sequences/Seq10_Frequence";
import { Seq11_Synthese, DURATION_SEQ11 } from "./sequences/Seq11_Synthese";
import { Seq12_Chute, DURATION_SEQ12 } from "./sequences/Seq12_Chute";
import { Seq13_Epilogue, DURATION_SEQ13 } from "./sequences/Seq13_Epilogue";

const TOTAL_DURATION =
  DURATION_SEQ01 +
  DURATION_SEQ02 +
  DURATION_SEQ03 +
  DURATION_SEQ04 +
  DURATION_SEQ05 +
  DURATION_SEQ06 +
  DURATION_SEQ07 +
  DURATION_SEQ08 +
  DURATION_SEQ09 +
  DURATION_SEQ10 +
  DURATION_SEQ11 +
  DURATION_SEQ12 +
  DURATION_SEQ13;

// Film complet en une seule composition sérialisée
const BonjourSoleilFilm: React.FC = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={DURATION_SEQ01}>
        <Seq01_Prologue />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ02}>
        <Seq02_Message />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ03}>
        <Seq03_AppelIA />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ04}>
        <Seq04_LangagePere />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ05}>
        <Seq05_Permutations />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ06}>
        <Seq06_Rotations />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ07}>
        <Seq07_Code />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ08}>
        <Seq08_Crypto />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ09}>
        <Seq09_Cosmos />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ10}>
        <Seq10_Frequence />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ11}>
        <Seq11_Synthese />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ12}>
        <Seq12_Chute />
      </Series.Sequence>
      <Series.Sequence durationInFrames={DURATION_SEQ13}>
        <Seq13_Epilogue />
      </Series.Sequence>
    </Series>
  );
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Composition complète — film entier */}
      <Composition
        id="BonjourSoleil"
        component={BonjourSoleilFilm}
        durationInFrames={TOTAL_DURATION}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />

      {/* Compositions individuelles pour preview/debug */}
      <Composition id="Seq01_Prologue" component={Seq01_Prologue} durationInFrames={DURATION_SEQ01} fps={30} width={1920} height={1080} />
      <Composition id="Seq02_Message" component={Seq02_Message} durationInFrames={DURATION_SEQ02} fps={30} width={1920} height={1080} />
      <Composition id="Seq03_AppelIA" component={Seq03_AppelIA} durationInFrames={DURATION_SEQ03} fps={30} width={1920} height={1080} />
      <Composition id="Seq04_LangagePere" component={Seq04_LangagePere} durationInFrames={DURATION_SEQ04} fps={30} width={1920} height={1080} />
      <Composition id="Seq05_Permutations" component={Seq05_Permutations} durationInFrames={DURATION_SEQ05} fps={30} width={1920} height={1080} />
      <Composition id="Seq06_Rotations" component={Seq06_Rotations} durationInFrames={DURATION_SEQ06} fps={30} width={1920} height={1080} />
      <Composition id="Seq07_Code" component={Seq07_Code} durationInFrames={DURATION_SEQ07} fps={30} width={1920} height={1080} />
      <Composition id="Seq08_Crypto" component={Seq08_Crypto} durationInFrames={DURATION_SEQ08} fps={30} width={1920} height={1080} />
      <Composition id="Seq09_Cosmos" component={Seq09_Cosmos} durationInFrames={DURATION_SEQ09} fps={30} width={1920} height={1080} />
      <Composition id="Seq10_Frequence" component={Seq10_Frequence} durationInFrames={DURATION_SEQ10} fps={30} width={1920} height={1080} />
      <Composition id="Seq11_Synthese" component={Seq11_Synthese} durationInFrames={DURATION_SEQ11} fps={30} width={1920} height={1080} />
      <Composition id="Seq12_Chute" component={Seq12_Chute} durationInFrames={DURATION_SEQ12} fps={30} width={1920} height={1080} />
      <Composition id="Seq13_Epilogue" component={Seq13_Epilogue} durationInFrames={DURATION_SEQ13} fps={30} width={1920} height={1080} />
    </>
  );
};
