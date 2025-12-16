import React, { useState } from 'react';
import { Mail, MapPin } from 'lucide-react';

// API base URL - can be overridden by environment variable
const API_BASE_URL = "http://localhost:8000";

const ContactSection: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Clear previous messages and set loading state
    setSuccessMessage(null);
    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/contact/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          message: formData.message,
        }),
      });

      if (response.status === 201) {
        // Success
        setSuccessMessage(
          "Thanks for reaching out! I've received your message and will reply within 24 hours."
        );
        setFormData({ name: '', email: '', message: '' });
      } else if (response.status === 400) {
        // Validation error
        setErrorMessage("Please check your details and try again.");
      } else if (response.status === 429) {
        // Rate limited
        setErrorMessage(
          "You've sent too many messages in a short time. Please wait a while and try again."
        );
      } else {
        // Other error
        setErrorMessage("Something went wrong while sending your message. Please try again.");
      }
    } catch (error) {
      // Network error
      setErrorMessage("Something went wrong while sending your message. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section id="contact" className="py-20 lg:py-24 px-6 md:px-12 bg-dark-800 border-b border-dark-700/50 relative overflow-hidden">
      <div className="container mx-auto max-w-5xl relative">

        {/* Top Heading Area matching Simone structure */}
        <div className="relative mb-20 text-center w-full flex flex-col items-center justify-center">
          {/* Faded Background Text (Watermark) */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full select-none pointer-events-none">
            <span className="text-[5rem] md:text-[8rem] lg:text-[9rem] font-bold text-gray-500 opacity-10 uppercase font-poppins whitespace-nowrap">
              Contact
            </span>
          </div>

          {/* Visible Foreground Text */}
          <div className="relative z-10">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-3 font-poppins">Get in Touch</h2>
            <div className="h-1 w-20 bg-accent mx-auto"></div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">

          {/* Contact Info (Left Column) */}
          <div className="lg:col-span-4 space-y-8">
            <h3 className="text-2xl font-bold text-white mb-4 font-poppins">Let's Build Something Reliable</h3>
            <div className="text-gray-400 text-sm leading-relaxed font-sans space-y-4">
              <p>
                If you're looking to build or improve a web platform, backend system, or automation workflow, I'd be happy to discuss your project. I work with businesses and founders who value clean architecture, performance, and security.
              </p>
              <p>
                I'm available for freelance and contract-based work, as well as long-term technical collaborations.
              </p>
            </div>

            <div className="space-y-4 pt-4">
              <div className="flex items-start">
                <span className="text-accent mt-1 mr-4"><Mail size={20} /></span>
                <div>
                  <h4 className="text-white font-medium font-poppins">Email</h4>
                  <a href="mailto:mukeshcoder1984@gmail.com" className="text-gray-400 text-sm hover:text-accent font-sans">mukeshcoder1984@gmail.com</a>
                </div>
              </div>
              <div className="flex items-start">
                <span className="text-accent mt-1 mr-4"><MapPin size={20} /></span>
                <div>
                  <h4 className="text-white font-medium font-poppins">Location</h4>
                  <p className="text-gray-400 text-sm font-sans">Nepal (Working with international clients remotely)</p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form (Right Column) */}
          <div className="lg:col-span-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Name"
                    required
                    disabled={isSubmitting}
                    className="w-full bg-dark-900 border border-dark-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-accent transition-colors font-sans disabled:opacity-50"
                  />
                </div>
                <div>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Email"
                    required
                    disabled={isSubmitting}
                    className="w-full bg-dark-900 border border-dark-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-accent transition-colors font-sans disabled:opacity-50"
                  />
                </div>
              </div>
              <div>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder="Project details / requirements"
                  rows={5}
                  required
                  disabled={isSubmitting}
                  className="w-full bg-dark-900 border border-dark-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-accent transition-colors resize-none font-sans disabled:opacity-50"
                ></textarea>
              </div>

              {/* Success Message */}
              {successMessage && (
                <div className="p-4 rounded-lg bg-accent/10 border border-accent/30 text-accent text-sm font-sans">
                  {successMessage}
                </div>
              )}

              {/* Error Message */}
              {errorMessage && (
                <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm font-sans">
                  {errorMessage}
                </div>
              )}

              <div className="flex flex-col items-center sm:items-start">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-8 py-3 bg-accent hover:bg-accent-hover text-white rounded-full font-semibold transition-all shadow-lg hover:shadow-accent/30 font-poppins disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? 'Sending...' : 'Send Message'}
                </button>
                <p className="text-gray-500 text-sm mt-4 font-sans">Typical response time: within 24 hours</p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;