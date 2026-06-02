'use client';

import React, { useState } from 'react';
import Image from 'next/image';

interface VideoFacadeProps {
  videoId: string;
  type?: 'youtube' | 'vimeo';
  placeholderImg?: string;
}

export default function VideoFacade({ videoId, type = 'youtube', placeholderImg }: VideoFacadeProps) {
  const [isPlaying, setIsPlaying] = useState(false);

  const bgImg = placeholderImg || (type === 'youtube' ? `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg` : '/assets/video-placeholder.jpg');

  const handlePlay = () => {
    setIsPlaying(true);
    
    // GA4 Tracking
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('event', 'video_start', {
        video_id: videoId,
        event_category: 'Video Engagement',
        event_label: 'YouTube Video Started',
      });
    }
  };

  return (
    <div 
      className="relative w-full aspect-video bg-black rounded-lg overflow-hidden cursor-pointer group"
      onClick={handlePlay}
      role="region"
      aria-label="Video Player Placeholder"
    >
      {!isPlaying ? (
        <>
          {/* Facade Background */}
          <div 
            className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-105"
            style={{ backgroundImage: `url(${bgImg})` }}
          />
          {/* Facade Overlay */}
          <div className="absolute inset-0 bg-black/40 group-hover:bg-black/20 transition-colors duration-300" />
          
          {/* Play Button */}
          <div className="absolute inset-0 flex items-center justify-center">
            <button 
              className="w-16 h-16 bg-[#c4a265] text-white rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(196,162,101,0.5)] transition-transform duration-300 group-hover:scale-110"
              aria-label="Play Embedded Video"
            >
              <svg className="w-8 h-8 ml-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
              </svg>
            </button>
          </div>

          {/* Fallback for Googlebot */}
          <noscript>
            <iframe 
              src={`https://www.youtube.com/embed/${videoId}?rel=0`} 
              width="100%" 
              height="100%" 
              style={{ position: 'absolute', top: 0, left: 0 }} 
              frameBorder="0" 
              allowFullScreen 
              title="YouTube Video Fallback"
            />
          </noscript>
        </>
      ) : (
        <iframe
          src={`https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0`}
          className="absolute top-0 left-0 w-full h-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          title="YouTube Video"
        />
      )}
    </div>
  );
}
