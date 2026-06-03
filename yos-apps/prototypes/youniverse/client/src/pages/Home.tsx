// Y-OS Universe — Home.tsx
// Main orchestrator: 4-level navigation (L0→L1→L2→L3)
// + ⌘K search overlay, InfoPanel with full satellite details
// + GSAP camera transitions, double-tap up navigation

import { useState, useCallback, useRef, useEffect, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import type { PlanetNode, MoonNode, SatelliteNode } from '../types/cms';
import { useCMS } from '../hooks/useCMS';
import L0Scene from '../components/three/L0Scene';
import L1Scene from '../components/three/L1Scene';
import L2Scene from '../components/three/L2Scene';
import L3Scene from '../components/three/L3Scene';
import Breadcrumb from '../components/Breadcrumb';
import InfoPanel from '../components/InfoPanel';
import CockpitFilter from '../components/CockpitFilter';
import LLMCommandPanel from '../components/LLMCommandPanel';
import SearchOverlay from '../components/SearchOverlay';

type Level = 0 | 1 | 2 | 3;
type FilterKey = 'all' | 'alert' | 'recent' | 'favorite' | 'active' | 'done' | 'dormant';

export default function Home() {
  const { data, loading, error } = useCMS();

  const [level, setLevel] = useState<Level>(0);
  const [selectedPlanet, setSelectedPlanet] = useState<PlanetNode | null>(null);
  const [selectedMoon, setSelectedMoon] = useState<MoonNode | null>(null);
  const [selectedSatellite, setSelectedSatellite] = useState<SatelliteNode | null>(null);
  const [filter, setFilter] = useState<FilterKey>('all');
  const [llmOpen, setLlmOpen] = useState(false);
  const [infoPanelVisible, setInfoPanelVisible] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);

  // ⌘K / Ctrl+K keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setSearchOpen(o => !o);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Double-tap to navigate up
  const lastTapRef = useRef<number>(0);
  const DOUBLE_TAP_MS = 350;

  const handleCanvasDoubleTap = useCallback(() => {
    const now = Date.now();
    if (now - lastTapRef.current < DOUBLE_TAP_MS) {
      if (level === 3) {
        setLevel(2);
        setSelectedSatellite(null);
        setInfoPanelVisible(false);
      } else if (level === 2) {
        setLevel(1);
        setSelectedMoon(null);
        setInfoPanelVisible(false);
      } else if (level === 1) {
        setLevel(0);
        setSelectedPlanet(null);
        setInfoPanelVisible(false);
      }
    }
    lastTapRef.current = now;
  }, [level]);

  // Navigation handlers
  const handleSelectPlanet = useCallback((planet: PlanetNode) => {
    setSelectedPlanet(planet);
    setLevel(1);
    setInfoPanelVisible(true);
  }, []);

  const handleSelectMoon = useCallback((moon: MoonNode) => {
    setSelectedMoon(moon);
    setLevel(2);
    setInfoPanelVisible(true);
  }, []);

  const handleSelectSatellite = useCallback((sat: SatelliteNode) => {
    setSelectedSatellite(sat);
    setLevel(3);
    setInfoPanelVisible(true);
  }, []);

  const handleBreadcrumbNavigate = useCallback((targetLevel: number) => {
    if (targetLevel === 0) {
      setLevel(0);
      setSelectedPlanet(null);
      setSelectedMoon(null);
      setSelectedSatellite(null);
      setInfoPanelVisible(false);
    } else if (targetLevel === 1) {
      setLevel(1);
      setSelectedMoon(null);
      setSelectedSatellite(null);
      setInfoPanelVisible(false);
    } else if (targetLevel === 2) {
      setLevel(2);
      setSelectedSatellite(null);
      setInfoPanelVisible(false);
    }
  }, []);

  // Search navigation — jump directly to the right level
  const handleSearchNavigate = useCallback((result: { type: string; planet: PlanetNode; moon?: MoonNode; satellite?: SatelliteNode }) => {
    if (result.type === 'planet') {
      setSelectedPlanet(result.planet);
      setSelectedMoon(null);
      setSelectedSatellite(null);
      setLevel(1);
      setInfoPanelVisible(true);
    } else if (result.type === 'moon' && result.moon) {
      setSelectedPlanet(result.planet);
      setSelectedMoon(result.moon);
      setSelectedSatellite(null);
      setLevel(2);
      setInfoPanelVisible(true);
    } else if (result.type === 'satellite' && result.moon && result.satellite) {
      setSelectedPlanet(result.planet);
      setSelectedMoon(result.moon);
      setSelectedSatellite(result.satellite);
      setLevel(3);
      setInfoPanelVisible(true);
    }
  }, []);

  const handleLLMCommand = useCallback((cmd: string) => {
    const lower = cmd.toLowerCase();
    if (!data) return;

    if (lower.includes('navigue') || lower.includes('navigate')) {
      const planet = data.planets.find(p =>
        lower.includes(p.name.toLowerCase()) || lower.includes(p.id.toLowerCase())
      );
      if (planet) {
        handleSelectPlanet(planet);
        return;
      }
    }
    if (lower.includes('retour') || lower.includes('back') || lower.includes('up')) {
      handleBreadcrumbNavigate(Math.max(0, level - 1));
    }
    if (lower.includes('cherch') || lower.includes('search') || lower.includes('find')) {
      setSearchOpen(true);
    }
  }, [data, level, handleSelectPlanet, handleBreadcrumbNavigate]);

  // Breadcrumb items
  const breadcrumbItems = [
    { label: data?.sun?.name || 'Y-OS', level: 0, color: '#FFD700' },
    ...(selectedPlanet ? [{ label: selectedPlanet.name, level: 1, color: selectedPlanet.color }] : []),
    ...(selectedMoon ? [{ label: selectedMoon.name, level: 2, color: selectedMoon.color }] : []),
    ...(selectedSatellite ? [{ label: selectedSatellite.name, level: 3, color: selectedSatellite.color }] : []),
  ];

  // InfoPanel target
  const infoTarget = !infoPanelVisible ? null :
    level === 3 && selectedSatellite ? { type: 'satellite' as const, data: selectedSatellite } :
    level === 2 && selectedMoon ? { type: 'moon' as const, data: selectedMoon } :
    level === 1 && selectedPlanet ? { type: 'planet' as const, data: selectedPlanet } :
    null;

  // Stats
  const totalPlanets = data?.planets?.length ?? 0;
  const totalMoons = data?.planets?.reduce((s, p) => s + (p.moons?.length ?? 0), 0) ?? 0;
  const totalSats = data?.planets?.reduce((s, p) =>
    s + (p.moons?.reduce((ms, m) => ms + (m.satellites?.length ?? 0), 0) ?? 0), 0) ?? 0;

  if (loading) {
    return (
      <div style={{
        width: '100dvw',
        height: '100dvh',
        background: '#04040C',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#FFD700',
        fontFamily: '"Space Mono", monospace',
        fontSize: 14,
        letterSpacing: '0.1em',
      }}>
        Y-OS UNIVERSE · LOADING…
      </div>
    );
  }

  if (error || !data) {
    return (
      <div style={{
        width: '100dvw',
        height: '100dvh',
        background: '#04040C',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#FF4444',
        fontFamily: '"Space Mono", monospace',
        fontSize: 14,
      }}>
        ERROR: {error || 'No data'}
      </div>
    );
  }

  return (
    <div style={{
      width: '100dvw',
      height: '100dvh',
      background: '#04040C',
      overflow: 'hidden',
      position: 'fixed',
      top: 0,
      left: 0,
    }}>
      {/* Header: stats + search button */}
      <div style={{
        position: 'fixed',
        top: 0,
        right: 0,
        zIndex: 51,
        padding: '10px 16px',
        display: 'flex',
        alignItems: 'center',
        gap: 12,
      }}>
        <span style={{
          fontSize: 11,
          color: '#444466',
          fontFamily: '"Space Mono", monospace',
          letterSpacing: '0.05em',
        }}>
          {totalPlanets}P · {totalMoons}L · {totalSats}S
        </span>
        {/* Search button — mobile-friendly 44px target */}
        <button
          onClick={() => setSearchOpen(true)}
          style={{
            width: 40,
            height: 40,
            minWidth: 44,
            minHeight: 44,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'rgba(255,255,255,0.06)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 8,
            color: '#888899',
            fontSize: 16,
            cursor: 'pointer',
            padding: 0,
          }}
          title="Rechercher (⌘K)"
        >
          ⌕
        </button>
      </div>

      {/* Breadcrumb */}
      <Breadcrumb
        items={breadcrumbItems}
        onNavigate={handleBreadcrumbNavigate}
        currentLevel={level}
      />

      {/* 3D Canvas */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          touchAction: 'none',
          WebkitTouchCallout: 'none',
          WebkitUserSelect: 'none',
        }}
        onClick={handleCanvasDoubleTap}
      >
        <Canvas
          dpr={[1, 2]}
          gl={{
            antialias: true,
            alpha: false,
            powerPreference: 'high-performance',
            failIfMajorPerformanceCaveat: false,
          }}
          camera={{
            fov: 55,
            near: 0.1,
            far: 500,
            position: [0, 20, 60],
          }}
          style={{
            width: '100%',
            height: '100%',
            background: '#04040C',
          }}
          onCreated={({ gl }) => {
            gl.domElement.addEventListener('webglcontextlost', (e) => {
              e.preventDefault();
              console.warn('WebGL context lost — attempting recovery');
            });
          }}
        >
          <Suspense fallback={null}>
            {level === 0 && (
              <L0Scene
                data={data}
                onSelectPlanet={handleSelectPlanet}
                selectedPlanetId={selectedPlanet?.id}
              />
            )}
            {level === 1 && selectedPlanet && (
              <L1Scene
                planet={selectedPlanet}
                onSelectMoon={handleSelectMoon}
                selectedMoonId={selectedMoon?.id}
              />
            )}
            {level === 2 && selectedMoon && (
              <L2Scene
                moon={selectedMoon}
                onSelectSatellite={handleSelectSatellite}
              />
            )}
            {level === 3 && selectedSatellite && (
              <L3Scene satellite={selectedSatellite} />
            )}
          </Suspense>

          <OrbitControls
            enablePan={false}
            enableZoom
            enableRotate
            rotateSpeed={0.5}
            zoomSpeed={0.8}
            minDistance={5}
            maxDistance={200}
            makeDefault
          />
        </Canvas>
      </div>

      {/* Bottom hint — only at L0 */}
      {level === 0 && (
        <div style={{
          position: 'fixed',
          bottom: 68,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontSize: 12,
          color: '#333355',
          fontFamily: '"Space Mono", monospace',
          pointerEvents: 'none',
          padding: '0 16px',
          zIndex: 30,
        }}>
          Tap planète · Pinch zoom · Double-tap → retour · ⌘K rechercher
        </div>
      )}

      {/* InfoPanel */}
      {infoTarget && (
        <InfoPanel
          target={infoTarget}
          onClose={() => setInfoPanelVisible(false)}
        />
      )}

      {/* Cockpit filter — hidden when InfoPanel is open */}
      {!infoPanelVisible && (
        <CockpitFilter active={filter} onChange={setFilter} />
      )}

      {/* LLM Command Panel */}
      <LLMCommandPanel
        isOpen={llmOpen}
        onToggle={() => setLlmOpen(o => !o)}
        onCommand={handleLLMCommand}
      />

      {/* Search Overlay — ⌘K */}
      {data && (
        <SearchOverlay
          data={data}
          isOpen={searchOpen}
          onClose={() => setSearchOpen(false)}
          onNavigate={handleSearchNavigate}
        />
      )}
    </div>
  );
}
