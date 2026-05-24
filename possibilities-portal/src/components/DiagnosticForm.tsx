"use client";

import { useState } from "react";

export default function DiagnosticForm() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    topic: "",
    message: "",
  });
  const [files, setFiles] = useState<File[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const submitData = new FormData();
    submitData.append("name", formData.name);
    submitData.append("email", formData.email);
    submitData.append("company", formData.company);
    submitData.append("topic", formData.topic);
    submitData.append("message", formData.message);

    files.forEach((file) => {
      submitData.append("attachments", file);
    });

    try {
      const response = await fetch("/api/contact-api", {
        method: "POST",
        body: submitData,
      });

      if (response.ok) {
        setIsSuccess(true);
      } else {
        alert("Failed to submit inquiry. Please try again.");
      }
    } catch (error) {
      console.error(error);
      alert("An error occurred while submitting.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-8 rounded-2xl bg-[#111] border border-white/10 shadow-2xl backdrop-blur-sm">
      {!isSuccess ? (
        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="border-b border-white/10 pb-6">
            <h2 className="text-3xl font-light tracking-tight text-white mb-2">Diagnostic Intake</h2>
            <p className="text-gray-400 font-light">
              Step {step} of 3: {step === 1 ? "Client Details" : step === 2 ? "Project Scope" : "Architectural Files"}
            </p>
          </div>

          {step === 1 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300 uppercase tracking-widest">Full Name</label>
                  <input
                    type="text"
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleInputChange}
                    className="w-full bg-black/50 border border-white/10 rounded-lg p-4 text-white focus:ring-2 focus:ring-white/20 focus:border-transparent transition-all outline-none"
                    placeholder="John Doe"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300 uppercase tracking-widest">Email Address</label>
                  <input
                    type="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full bg-black/50 border border-white/10 rounded-lg p-4 text-white focus:ring-2 focus:ring-white/20 focus:border-transparent transition-all outline-none"
                    placeholder="john@example.com"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 uppercase tracking-widest">Organization / Project Entity</label>
                <input
                  type="text"
                  name="company"
                  value={formData.company}
                  onChange={handleInputChange}
                  className="w-full bg-black/50 border border-white/10 rounded-lg p-4 text-white focus:ring-2 focus:ring-white/20 focus:border-transparent transition-all outline-none"
                  placeholder="Apex Holdings LLC"
                />
              </div>
              <button
                type="button"
                onClick={() => setStep(2)}
                disabled={!formData.name || !formData.email}
                className="w-full bg-white text-black py-4 rounded-lg font-medium hover:bg-gray-200 transition-colors disabled:opacity-50"
              >
                Continue to Scope
              </button>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 uppercase tracking-widest">Project Category</label>
                <select
                  name="topic"
                  value={formData.topic}
                  onChange={handleInputChange}
                  className="w-full bg-black/50 border border-white/10 rounded-lg p-4 text-white focus:ring-2 focus:ring-white/20 focus:border-transparent transition-all outline-none appearance-none"
                >
                  <option value="Custom Home Build">Custom Home Build</option>
                  <option value="Luxury Hardscaping">Luxury Hardscaping</option>
                  <option value="Commercial Development">Commercial Development</option>
                  <option value="Other">Other Consulting</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 uppercase tracking-widest">Project Vision & Budget Constraints</label>
                <textarea
                  name="message"
                  required
                  value={formData.message}
                  onChange={handleInputChange}
                  rows={5}
                  className="w-full bg-black/50 border border-white/10 rounded-lg p-4 text-white focus:ring-2 focus:ring-white/20 focus:border-transparent transition-all outline-none"
                  placeholder="Describe your vision. Please include estimated timeline (e.g. Q3 2026) and financial budget range (e.g. $1M - $1.5M)."
                />
              </div>
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="px-6 py-4 rounded-lg font-medium border border-white/10 text-white hover:bg-white/5 transition-colors"
                >
                  Back
                </button>
                <button
                  type="button"
                  onClick={() => setStep(3)}
                  disabled={!formData.message}
                  className="flex-1 bg-white text-black py-4 rounded-lg font-medium hover:bg-gray-200 transition-colors disabled:opacity-50"
                >
                  Continue to Files
                </button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="space-y-4">
                <label className="text-sm font-medium text-gray-300 uppercase tracking-widest">Upload Documentation</label>
                <p className="text-sm text-gray-500">Attach CAD files, topography maps, or site photos (Max 10MB per file).</p>
                <div className="relative border-2 border-dashed border-white/20 rounded-xl p-12 text-center hover:bg-white/5 hover:border-white/40 transition-all group">
                  <input
                    type="file"
                    multiple
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <div className="space-y-2 pointer-events-none">
                    <svg className="mx-auto h-12 w-12 text-gray-400 group-hover:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                    </svg>
                    <p className="text-white font-medium">Click to upload or drag and drop</p>
                    <p className="text-sm text-gray-400">{files.length} file(s) selected</p>
                  </div>
                </div>
              </div>
              
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setStep(2)}
                  className="px-6 py-4 rounded-lg font-medium border border-white/10 text-white hover:bg-white/5 transition-colors"
                >
                  Back
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 bg-[#0070f3] text-white py-4 rounded-lg font-medium hover:bg-blue-600 transition-colors shadow-[0_0_20px_rgba(0,112,243,0.3)] disabled:opacity-50"
                >
                  {isSubmitting ? "Transmitting to Keystone..." : "Submit Inquiry"}
                </button>
              </div>
            </div>
          )}
        </form>
      ) : (
        <div className="py-12 text-center animate-in zoom-in duration-500">
          <div className="mx-auto w-20 h-20 bg-green-500/20 rounded-full flex items-center justify-center mb-6 border border-green-500/30">
            <svg className="w-10 h-10 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 className="text-3xl font-light text-white mb-4">Submission Received.</h3>
          <p className="text-gray-400 mb-8 max-w-md mx-auto">
            Your architectural data has been securely transmitted. A Keystone partner will evaluate your scope and respond shortly.
          </p>
          <button
            onClick={() => {
              setStep(1);
              setFormData({ name: "", email: "", company: "", topic: "", message: "" });
              setFiles([]);
              setIsSuccess(false);
            }}
            className="text-white border border-white/20 px-8 py-3 rounded-lg hover:bg-white/10 transition-colors"
          >
            Submit Another Project
          </button>
        </div>
      )}
    </div>
  );
}
