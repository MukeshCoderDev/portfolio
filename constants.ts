import {
  Monitor,
  Server,
  Database,
  ShieldCheck,
  Home,
  User,
  Briefcase,
  FileText,
  Layers,
  Mail
} from 'lucide-react';
import { NavItem, Service, ExperienceItem, Skill, Project } from './types';

export const NAV_ITEMS: NavItem[] = [
  { id: 'home', label: 'Home', icon: Home },
  { id: 'about', label: 'About Me', icon: User },
  { id: 'services', label: 'What I Do', icon: Monitor },
  { id: 'resume', label: 'Resume', icon: FileText },
  { id: 'portfolio', label: 'Portfolio', icon: Layers },
  { id: 'contact', label: 'Contact', icon: Mail },
];

export const SERVICES: Service[] = [
  {
    title: "Full Stack Web Development",
    description: "I build reliable, scalable web applications using React on the frontend and Django/FastAPI on the backend, focused on performance, maintainability, and clean architecture.",
    icon: Monitor
  },
  {
    title: "API & Automation Development",
    description: "I design production-ready REST APIs with secure authentication, validation, and documentation. I also implement automation and background processing using tools like Celery and Redis to handle long-running tasks efficiently.",
    icon: Server
  },
  {
    title: "Database Design & Integration",
    description: "I work with PostgreSQL to design scalable data models, ensure data integrity, and support high-performance backend systems as applications grow.",
    icon: Database
  },
  {
    title: "Security-First Development",
    description: "I follow security best practices including secure authentication, authorization, input validation, and protection against common vulnerabilities to ensure applications are safe and dependable.",
    icon: ShieldCheck
  }
];

export const EDUCATION: ExperienceItem[] = [
  {
    year: "2020 - Present",
    title: "Independent Software Development",
    subtitle: "Project-Based Learning",
    description: "Focused on backend systems, API development, automation, and frontend integration through continuous project-based learning."
  }
];

export const EXPERIENCE: ExperienceItem[] = [
  {
    title: "Founder & Lead Developer – Scalify Labs",
    subtitle: "Independent Software Studio",
    description: [
      "Designing and building full stack web applications for real-world use cases",
      "Developing secure REST APIs using Django REST Framework and FastAPI",
      "Integrating React frontends with backend services",
      "Implementing automation and background processing (Celery, Redis)",
      "Managing deployments, version control, and system improvements"
    ]
  },
  {
    title: "Independent Projects & System Development",
    subtitle: "Self-Directed Work",
    description: [
      "Built multiple API-driven applications with authentication, file uploads, and background processing",
      "Developed frontend dashboards connected to backend services",
      "Implemented real-world workflows including user management, processing pipelines, and deployment setups",
      "Focused on performance, scalability, and maintainable architecture",
      "Designed and implemented a production-ready contact & automation backend system using Django, Django REST Framework, Celery, Redis, PostgreSQL and JWT authentication, including async email workflows, spam protection, rate limiting and 33 automated tests"
    ]
  }
];

export const SKILLS: Skill[] = [
  { name: "JavaScript (ES6+)", percentage: 70 },
  { name: "React", percentage: 70 },
  { name: "Python", percentage: 80 },
  { name: "Django / DRF", percentage: 80 },
  { name: "FastAPI", percentage: 70 },
  { name: "REST APIs", percentage: 80 },
  { name: "PostgreSQL", percentage: 65 },
  { name: "Git & GitHub", percentage: 70 },
  { name: "HTML / CSS", percentage: 75 },
  { name: "Basic Cybersecurity", percentage: 60 },
];

export const PROJECTS: Project[] = [
  {
    title: "Video Automation Platform",
    description: "A production-ready video automation system that allows users to upload videos and receive processed outputs such as trailers, subtitles, and social-media–ready exports.",
    techStack: "React · Django REST Framework · Celery · FFmpeg · PostgreSQL",
    highlights: [
      "Asynchronous video processing using background workers",
      "Automated trailer generation, subtitle handling, and format conversion",
      "Real-time frontend dashboard with task status tracking",
      "Secure user authentication and API-based architecture"
    ],
    image: "https://picsum.photos/600/400?random=1",
    githubLink: "#",
    demoLink: "#"
  },
  {
    title: "Secure REST API Backend System",
    description: "A scalable and secure backend API platform designed for user management and data-driven applications.",
    techStack: "Python · Django REST Framework · PostgreSQL",
    highlights: [
      "Token-based authentication and authorization",
      "Clean RESTful API design with validation and error handling",
      "Modular architecture suitable for web or mobile clients"
    ],
    image: "https://picsum.photos/600/400?random=2",
    githubLink: "#",
    demoLink: "#"
  },
  {
    title: "Developer Portfolio & Business Website",
    description: "A modern, responsive website built to showcase projects, technical skills, and contact information with a clean user experience.",
    techStack: "React · JavaScript · HTML · CSS",
    highlights: [
      "Component-based frontend architecture",
      "Optimized performance and responsive design",
      "Deployed as a production-ready static application"
    ],
    image: "https://picsum.photos/600/400?random=3",
    githubLink: "#",
    demoLink: "#"
  }
];