import React, { useState, useEffect } from 'react';
import { Menu } from 'lucide-react';
import Sidebar from './components/Sidebar';
import HeroSection from './components/HeroSection';
import AboutSection from './components/AboutSection';
import ServicesSection from './components/ServicesSection';
import ResumeSection from './components/ResumeSection';
import PortfolioSection from './components/PortfolioSection';
import ContactSection from './components/ContactSection';
import ScrollToTop from './components/ScrollToTop';

const App: React.FC = () => {
  const [activeSection, setActiveSection] = useState('home');
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  // Function to handle scrolling to section
  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setActiveSection(id);
    }
  };

  // Intersection Observer to update active nav link on scroll
  useEffect(() => {
    const sections = ['home', 'about', 'services', 'resume', 'portfolio', 'contact'];
    
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      {
        threshold: 0.2, // Trigger when 20% of the section is visible
        rootMargin: "-20% 0px -50% 0px" // Adjust viewport to center detection
      }
    );

    sections.forEach((id) => {
      const element = document.getElementById(id);
      if (element) observer.observe(element);
    });

    return () => {
      sections.forEach((id) => {
        const element = document.getElementById(id);
        if (element) observer.unobserve(element);
      });
    };
  }, []);

  return (
    <div className="flex flex-col lg:flex-row min-h-screen bg-dark-900 text-gray-300">
      
      {/* Mobile Toggle Button */}
      <button 
        className="fixed top-4 right-4 z-50 p-2 bg-dark-800 rounded lg:hidden text-white shadow-lg border border-dark-700"
        onClick={() => setIsMobileOpen(!isMobileOpen)}
      >
        <Menu size={24} />
      </button>

      {/* Sidebar */}
      <Sidebar 
        activeSection={activeSection} 
        isMobileOpen={isMobileOpen}
        onCloseMobile={() => setIsMobileOpen(false)}
        onNavigate={scrollToSection}
      />

      {/* Main Content Area */}
      <main className="flex-1 lg:ml-72 relative">
        <HeroSection onNavigate={scrollToSection} />
        <AboutSection />
        <ServicesSection />
        <ResumeSection />
        <PortfolioSection />
        <ContactSection />
        
        {/* Footer for Main Content */}
        <footer className="py-8 text-center border-t border-dark-700/50 text-gray-500 text-sm">
          <p>© {new Date().getFullYear()} Mukesh Shah. All Rights Reserved.</p>
        </footer>
      </main>
      
      <ScrollToTop />
    </div>
  );
};

export default App;