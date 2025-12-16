import { LucideIcon } from "lucide-react";

export interface NavItem {
  id: string;
  label: string;
  icon?: LucideIcon;
}

export interface Service {
  title: string;
  description: string;
  icon: LucideIcon;
}

export interface ExperienceItem {
  title: string;
  subtitle: string;
  year?: string;
  description: string | string[];
}

export interface Skill {
  name: string;
  percentage: number;
}

export interface Project {
  title: string;
  description: string;
  techStack: string;
  highlights?: string[];
  image: string;
  githubLink?: string;
  demoLink?: string;
}