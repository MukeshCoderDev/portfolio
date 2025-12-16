import React from 'react';
import { EDUCATION, EXPERIENCE, SKILLS } from '../constants';

const ResumeSection: React.FC = () => {
  return (
    <section id="resume" className="py-20 lg:py-24 px-6 md:px-12 bg-dark-800 border-b border-dark-700/50">
      <div className="container mx-auto max-w-5xl">
        
        {/* Header - Simple Style matching Simone's Resume & other sections */}
        <div className="relative mb-12 text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-3 font-poppins">Resume</h2>
            <div className="h-1 w-20 bg-accent mx-auto"></div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
          
          {/* Education Column */}
          <div>
            <h3 className="text-2xl font-bold text-white mb-6 font-poppins">My Education</h3>
            <div className="space-y-6">
              {EDUCATION.map((edu, idx) => (
                <div key={idx} className="bg-dark-900 p-6 rounded-lg border-l-4 border-accent shadow-md">
                  {edu.year && (
                    <span className="inline-block px-2 py-1 bg-dark-800 text-accent text-xs font-bold rounded mb-2 font-poppins">
                      {edu.year}
                    </span>
                  )}
                  <h4 className="text-xl font-semibold text-white mb-1 font-poppins">{edu.title}</h4>
                  <p className="text-accent text-sm mb-3 font-medium font-poppins">{edu.subtitle}</p>
                  <p className="text-gray-400 text-sm font-sans leading-relaxed">{edu.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Experience Column */}
          <div>
            <h3 className="text-2xl font-bold text-white mb-6 font-poppins">My Experience</h3>
            <div className="space-y-6">
              {EXPERIENCE.map((exp, idx) => (
                <div key={idx} className="bg-dark-900 p-6 rounded-lg border-l-4 border-accent shadow-md">
                   {exp.year && (
                    <span className="inline-block px-2 py-1 bg-dark-800 text-accent text-xs font-bold rounded mb-2 font-poppins">
                      {exp.year}
                    </span>
                   )}
                   <h4 className="text-xl font-semibold text-white mb-1 font-poppins">{exp.title}</h4>
                   <p className="text-accent text-sm mb-3 font-medium font-poppins">{exp.subtitle}</p>
                   {Array.isArray(exp.description) ? (
                     <ul className="text-gray-400 text-sm space-y-1 font-sans">
                       {exp.description.map((item, i) => (
                         <li key={i} className="flex items-start">
                           <span className="mr-2 text-accent mt-1">•</span>
                           <span className="leading-relaxed">{item}</span>
                         </li>
                       ))}
                     </ul>
                   ) : (
                     <p className="text-gray-400 text-sm font-sans leading-relaxed">{exp.description}</p>
                   )}
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Skills */}
        <div>
           <h3 className="text-2xl font-bold text-white mb-8 font-poppins">My Skills</h3>
           <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
             {SKILLS.map((skill, idx) => (
               <div key={idx}>
                 <div className="mb-2">
                   <span className="text-white font-medium font-poppins">{skill.name}</span>
                 </div>
                 <div className="h-2 bg-dark-900 rounded-full overflow-hidden">
                   <div 
                     className="h-full bg-accent rounded-full"
                     style={{ width: `${skill.percentage}%` }}
                   />
                 </div>
               </div>
             ))}
           </div>
        </div>
      </div>
    </section>
  );
};

export default ResumeSection;