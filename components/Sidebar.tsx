import React from 'react';
import { NAV_ITEMS } from '../constants';
import { Github, Linkedin, Mail, Facebook } from 'lucide-react';

interface SidebarProps {
  activeSection: string;
  isMobileOpen: boolean;
  onCloseMobile: () => void;
  onNavigate: (id: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, isMobileOpen, onCloseMobile, onNavigate }) => {
  return (
    <>
      {/* Overlay for mobile */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed top-0 left-0 h-full w-72 bg-dark-800 border-r border-dark-700 z-50 transition-transform duration-300 ease-in-out lg:translate-x-0 ${isMobileOpen ? 'translate-x-0' : '-translate-x-full'
          } flex flex-col`}
      >
        {/* Profile Header */}
        <div className="flex flex-col items-center justify-center pt-12 pb-8 px-6 text-center border-b border-dark-700/50">
          {/* Profile Avatar - Clean Single Circle */}
          <div
            className="sidebar-avatar"
            role="img"
            aria-label="Mukesh Shah"
          />

          {/* Name - Simone Style */}
          <h2 className="profile-name">
            Mukesh Shah
          </h2>

          {/* Role Text - Two lines, Simone Style */}
          <p className="profile-role">
            Full Stack Developer<br />
            API & Automation Specialist
          </p>
        </div>

        {/* Navigation - Simone Style */}
        <nav className="flex-1 overflow-y-auto py-6">
          <ul className="space-y-0">
            {NAV_ITEMS.map((item) => (
              <li key={item.id}>
                <button
                  onClick={() => {
                    onNavigate(item.id);
                    onCloseMobile();
                  }}
                  className={`sidebar-nav-link w-full ${activeSection === item.id ? 'active' : ''
                    }`}
                >
                  {item.label}
                </button>
              </li>
            ))}
          </ul>
        </nav>

        {/* Footer / Socials */}
        <div className="p-8 border-t border-dark-700/50">
          <div className="flex justify-center space-x-4">
            <a href="https://facebook.com/" target="_blank" rel="noreferrer" className="text-gray-400 hover:text-accent transition-colors">
              <Facebook size={18} />
            </a>
            <a href="https://github.com/your-username" target="_blank" rel="noreferrer" className="text-gray-400 hover:text-accent transition-colors">
              <Github size={18} />
            </a>
            <a href="#" target="_blank" rel="noreferrer" className="text-gray-400 hover:text-accent transition-colors">
              <Linkedin size={18} />
            </a>
            <a href="mailto:mukeshcoder1984@gmail.com" className="text-gray-400 hover:text-accent transition-colors">
              <Mail size={18} />
            </a>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;