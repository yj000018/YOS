// Y-OS Universe — CMS Types
// 4-level hierarchy: Sun → Planet → Moon → Satellite → Child

export type NodeStatus = 'active' | 'dormant' | 'done' | 'alert' | 'favorite' | 'recent';
export type MaterialArchetype = 'crystal' | 'gas' | 'organic' | 'rocky';
export type NodeType = 'doc' | 'link' | 'task' | 'note' | 'media' | 'tagline' | 'tool' | string;

export interface ChildNode {
  id: string;
  name: string;
  description?: string;
  type?: NodeType;
  color?: string;
  size?: number;
}

export interface SatelliteNode {
  id: string;
  name: string;
  description?: string;
  color?: string;
  size?: number;
  status?: NodeStatus;
  tags?: string[];
  url?: string;
  featured?: boolean;
  type?: NodeType;
  children?: ChildNode[];
}

export interface MoonNode {
  id: string;
  name: string;
  subtitle?: string;
  color?: string;
  emissive?: string;
  archetype?: MaterialArchetype;
  description?: string;
  size?: number;
  orbitRadius?: number;
  orbitSpeed?: number;
  orbitInclination?: number;
  satellites?: SatelliteNode[];
}

export interface PlanetNode {
  id: string;
  name: string;
  subtitle?: string;
  color?: string;
  glowColor?: string;
  emissive?: string;
  archetype?: MaterialArchetype;
  size?: number;
  orbitRadius?: number;
  orbitSpeed?: number;
  orbitInclination?: number;
  description?: string;
  frequency?: string;
  element?: string;
  moons?: MoonNode[];
}

export interface SunNode {
  id: string;
  name: string;
  subtitle?: string;
  description?: string;
  color?: string;
  glowColor?: string;
}

export interface CMSData {
  version: string;
  meta: {
    title: string;
    subtitle?: string;
    description?: string;
    author?: string;
    created?: string;
    owner?: string;
    note?: string;
  };
  sun: SunNode;
  planets: PlanetNode[];
}
