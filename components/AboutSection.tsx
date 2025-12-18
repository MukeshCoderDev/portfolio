import React from 'react';

const AboutSection: React.FC = () => {
  return (
    <section id="about" className="py-20 lg:py-24 px-6 md:px-12 bg-dark-800 border-b border-dark-700/50 relative overflow-hidden">
      <div className="container mx-auto max-w-6xl relative">
        
        {/* Top Heading Area matching Simone structure */}
        <div className="relative mb-20 text-center w-full flex items-center justify-center">
            {/* Faded Background Text (Watermark) */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full select-none pointer-events-none">
              <span className="text-[5rem] md:text-[8rem] lg:text-[9rem] font-bold text-gray-500 opacity-10 uppercase font-poppins whitespace-nowrap">
                About Me
              </span>
            </div>

            {/* Visible Foreground Text */}
            <div className="relative z-10">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-3 font-poppins">Know Me More</h2>
                <div className="h-1 w-20 bg-accent mx-auto"></div>
            </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
          {/* Left Column: Bio */}
          <div className="lg:col-span-8 text-center lg:text-left">
            <h3 className="text-2xl md:text-[1.75rem] font-semibold text-accent mb-6 font-poppins leading-tight">
              I’m Mukesh Shah, a Full Stack Developer specializing in API development, automation, and secure backend systems.
            </h3>
            <div className="space-y-4 text-gray-300 leading-relaxed font-sans text-base md:text-lg">
              <p>
                I design and build scalable REST APIs using Python (Django, Django REST Framework, FastAPI) and connect them with modern React frontends. My work focuses on clean architecture, performance, and reliability — ensuring applications are easy to maintain and scale as businesses grow.
              </p>
              <p>
                I regularly work on real-world challenges such as authentication systems, third-party API integrations, background processing with Celery, and performance optimization. Security is a core part of my development process, and I follow best practices to protect data and systems from common vulnerabilities.
              </p>
              <p>
                I collaborate with startups and small teams to deliver production-ready solutions and aim to build long-term partnerships based on trust, clear communication, and quality work.
              </p>
            </div>
          </div>

          {/* Right Column: Personal Details */}
          <div className="lg:col-span-4">
            <div className="space-y-0">
              
              <div className="border-b border-dark-700 py-4 first:pt-0">
                <span className="block text-sm text-gray-500 font-semibold uppercase mb-1 font-poppins tracking-wide">Name:</span>
                <span className="text-white font-medium font-sans">Mukesh Shah</span>
              </div>
              
              <div className="border-b border-dark-700 py-4">
                <span className="block text-sm text-gray-500 font-semibold uppercase mb-1 font-poppins tracking-wide">Email:</span>
                <a href="mailto:mukeshshah.dev@gmail.com" className="text-accent hover:underline font-medium font-sans">mukeshcoder1984@gmail.com</a>
              </div>
              
              <div className="border-b border-dark-700 py-4">
                <span className="block text-sm text-gray-500 font-semibold uppercase mb-1 font-poppins tracking-wide">Location:</span>
                <span className="text-white font-medium font-sans">Nepal (Remote)</span>
              </div>
              
              <div className="border-b border-dark-700 py-4">
                <span className="block text-sm text-gray-500 font-semibold uppercase mb-1 font-poppins tracking-wide">Role:</span>
                <span className="text-white font-medium font-sans">Full Stack Developer | API & Automation</span>
              </div>
              
              <div className="border-b border-dark-700 py-4">
                <span className="block text-sm text-gray-500 font-semibold uppercase mb-1 font-poppins tracking-wide">Availability:</span>
                <span className="text-accent font-medium font-sans">Open for freelance & contract work</span>
              </div>
              
            </div>
            
            <div className="mt-8 text-center lg:text-left">
              <a 
                href="/Mukesh_Shah_CV.pdf" 
                className="inline-block px-10 py-3.5 bg-accent hover:bg-accent-hover text-white rounded-full font-semibold transition-all shadow-lg hover:shadow-accent/30 font-poppins"
              >
                Download CV
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;