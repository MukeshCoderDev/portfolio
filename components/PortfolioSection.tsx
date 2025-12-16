import React from 'react';
import { PROJECTS } from '../constants';
import { Github, ExternalLink } from 'lucide-react';

const PortfolioSection: React.FC = () => {
  return (
    <section id="portfolio" className="py-20 lg:py-24 px-6 md:px-12 bg-dark-800 border-b border-dark-700/50 relative overflow-hidden">
      <div className="container mx-auto max-w-5xl relative">
        
        {/* Top Heading Area matching Simone structure */}
        <div className="relative mb-20 text-center w-full flex flex-col items-center justify-center">
            {/* Faded Background Text (Watermark) */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full select-none pointer-events-none">
              <span className="text-[5rem] md:text-[8rem] lg:text-[9rem] font-bold text-gray-500 opacity-10 uppercase font-poppins whitespace-nowrap">
                Portfolio
              </span>
            </div>

            {/* Visible Foreground Text */}
            <div className="relative z-10">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-3 font-poppins">My Work</h2>
                <div className="h-1 w-20 bg-accent mx-auto mb-4"></div>
                <p className="text-gray-400 font-sans">Selected Projects</p>
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {PROJECTS.map((project, index) => (
            <div key={index} className="group bg-dark-900 rounded-lg overflow-hidden shadow-lg border border-dark-700 hover:border-accent/50 transition-all duration-300 flex flex-col h-full">
              
              <div className="relative overflow-hidden aspect-video bg-dark-700">
                <img 
                  src={project.image} 
                  alt={project.title} 
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-dark-900/80 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center space-x-4">
                  <a href={project.githubLink} className="p-3 bg-dark-800 rounded-full text-white hover:text-accent transition-colors">
                    <Github size={20} />
                  </a>
                  {project.demoLink && (
                    <a href={project.demoLink} className="p-3 bg-dark-800 rounded-full text-white hover:text-accent transition-colors">
                      <ExternalLink size={20} />
                    </a>
                  )}
                </div>
              </div>

              <div className="p-6 flex flex-col flex-grow">
                <h3 className="text-xl font-bold text-white mb-3 font-poppins">{project.title}</h3>
                <p className="text-gray-400 text-sm mb-4 leading-relaxed font-sans">{project.description}</p>
                
                {project.highlights && (
                  <div className="mb-4">
                    <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2 font-poppins">Key capabilities</h4>
                    <ul className="space-y-1.5">
                      {project.highlights.map((h, i) => (
                        <li key={i} className="text-sm text-gray-400 flex items-start font-sans">
                          <span className="mr-2 text-accent mt-1.5 text-xs">●</span>
                          <span className="leading-relaxed">{h}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                <div className="mt-auto pt-4 border-t border-dark-700">
                  <p className="text-gray-400 text-xs font-medium font-sans">
                    <span className="text-white font-semibold">Tech stack:</span> {project.techStack}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default PortfolioSection;