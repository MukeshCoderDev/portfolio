import React, { useState, useEffect } from 'react';
import { ArrowDown } from 'lucide-react';

interface HeroSectionProps {
  onNavigate: (id: string) => void;
}

const HeroSection: React.FC<HeroSectionProps> = ({ onNavigate }) => {
  const [displayedText, setDisplayedText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [index, setIndex] = useState(0);
  
  const phrases = ["Full Stack Developer", "API & Automation Specialist"];
  const typingSpeed = 100;
  const deletingSpeed = 50;
  const pauseTime = 2000;

  useEffect(() => {
    const currentPhrase = phrases[index % phrases.length];
    
    let timer: ReturnType<typeof setTimeout>;

    if (isDeleting) {
      if (displayedText === '') {
        setIsDeleting(false);
        setIndex(prev => prev + 1);
        // Small pause before typing next phrase
        timer = setTimeout(() => {}, 200);
      } else {
        timer = setTimeout(() => {
          setDisplayedText(prev => prev.slice(0, -1));
        }, deletingSpeed);
      }
    } else {
      if (displayedText === currentPhrase) {
        timer = setTimeout(() => {
            setIsDeleting(true);
        }, pauseTime);
      } else {
        timer = setTimeout(() => {
            setDisplayedText(currentPhrase.slice(0, displayedText.length + 1));
        }, typingSpeed);
      }
    }

    return () => clearTimeout(timer);
  }, [displayedText, isDeleting, index, phrases]);

  return (
    <section id="home" className="min-h-screen flex items-center justify-center relative bg-[url('https://images.unsplash.com/photo-1497215728101-856f4ea42174?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80')] bg-cover bg-center bg-no-repeat bg-fixed">
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/40" />
      
      <div className="container px-6 relative z-10 text-center">
        <h2 className="text-2xl md:text-3xl font-medium text-white mb-3 font-poppins">Welcome</h2>
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-4 tracking-tight font-poppins">
          I'm <span className="text-white">Mukesh Shah</span>
        </h1>
        
        {/* Animated Role Line */}
        <div className="text-xl md:text-3xl font-semibold text-gray-200 mb-6 h-10 flex items-center justify-center font-poppins">
          <span>{displayedText}</span>
          <span className="typewriter-cursor"></span>
        </div>
        
        {/* Description */}
        <p className="text-base md:text-lg text-gray-100 max-w-2xl mx-auto mb-10 leading-relaxed font-sans">
          I build secure, scalable APIs and automation systems for modern businesses.
          <br className="hidden md:block" />
          Specialized in React, Django and FastApi with a strong focus on performance and security.
        </p>

        {/* Call to Action */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button 
            onClick={() => onNavigate('contact')}
            className="px-10 py-4 bg-accent hover:bg-accent-hover text-white rounded-full font-semibold transition-all shadow-lg hover:shadow-accent/30 hover:-translate-y-1 w-full sm:w-auto text-lg"
          >
            Start a Project
          </button>
        </div>
      </div>
      
      <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
        <ArrowDown className="text-white/80" size={32} />
      </div>
    </section>
  );
};

export default HeroSection;