"use client";

import React, { createContext, useEffect } from "react";

export interface BrandTheme {
  primary: string;
  secondary: string;
  bg: string;
  font: string;
  radius: string;
}

export const ThemeContext = createContext<{ theme: BrandTheme | null }>({ theme: null });

export function ThemeProvider({ theme, children }: { theme: BrandTheme; children: React.ReactNode }) {
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty("--brand-primary", theme.primary);
    root.style.setProperty("--brand-secondary", theme.secondary);
    root.style.setProperty("--brand-bg", theme.bg);
    root.style.setProperty("--brand-font", theme.font);
    root.style.setProperty("--brand-radius", theme.radius);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme }}>
      <div 
        style={{ 
          fontFamily: "var(--brand-font)", 
          backgroundColor: "var(--brand-bg)",
          borderRadius: "var(--brand-radius)" 
        }} 
        className="min-h-screen transition-colors duration-500"
      >
        {children}
      </div>
    </ThemeContext.Provider>
  );
}
