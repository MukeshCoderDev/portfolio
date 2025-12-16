import React from 'react';
import { SERVICES } from '../constants';

const ServicesSection: React.FC = () => {
  return (
    <section id="services" className="py-20 lg:py-24 px-6 md:px-12 bg-dark-800 border-b border-dark-700/50 relative overflow-hidden">
      <div className="container mx-auto max-w-5xl relative">
        
        {/* Top Heading Area matching Simone structure */}
        <div className="relative mb-20 text-center w-full flex items-center justify-center">
            {/* Faded Background Text (Watermark) */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full select-none pointer-events-none">
              <span className="text-[5rem] md:text-[8rem] lg:text-[9rem] font-bold text-gray-500 opacity-10 uppercase font-poppins whitespace-nowrap">
                Services
              </span>
            </div>

            {/* Visible Foreground Text */}
            <div className="relative z-10">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-3 font-poppins">What I Do</h2>
                <div className="h-1 w-20 bg-accent mx-auto"></div>
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-10">
          {SERVICES.map((service, index) => (
            <div key={index} className="bg-dark-900/50 p-8 rounded-lg border border-dark-700 hover:border-accent/50 transition-all duration-300 group hover:-translate-y-1">
              <div className="w-16 h-16 bg-dark-800 rounded-lg flex items-center justify-center text-accent mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300 border border-dark-700">
                <service.icon size={30} />
              </div>
              <h3 className="text-xl font-bold text-white mb-4 font-poppins">{service.title}</h3>
              <p className="text-gray-400 leading-relaxed text-sm lg:text-[15px] font-sans">
                {service.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;