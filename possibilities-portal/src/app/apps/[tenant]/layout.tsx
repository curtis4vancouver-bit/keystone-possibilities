import { ThemeProvider, BrandTheme } from "../../../components/ThemeProvider";

// CSS Brand Defaults from Blueprint
const tenantThemes: Record<string, BrandTheme> = {
  landscaping: {
    primary: "#15803d", // Forest Green
    secondary: "#86efac", // Mint
    bg: "#f0fdf4", // Off-white Green
    font: "system-ui, sans-serif",
    radius: "0.5rem", // Rounded
  },
  roofing: {
    primary: "#b91c1c", // Safety Red
    secondary: "#f3f4f6", // Light Gray
    bg: "#fafafa", // Pure White
    font: "var(--font-brand)", // Custom or Roboto
    radius: "0px", // Sharp
  },
  "custom-homes": {
    primary: "#0f172a", // Slate Black
    secondary: "#b45309", // Amber Gold
    bg: "#f8fafc", // Slate Gray Tint
    font: "Georgia, serif",
    radius: "0.125rem", // Slightly Rounded
  },
};

export default async function TenantLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ tenant: string }>;
}) {
  const { tenant } = await params;
  
  // Resolve theme, defaulting to landscaping if slug is unknown
  const activeTheme = tenantThemes[tenant] || tenantThemes.landscaping;

  return (
    <ThemeProvider theme={activeTheme}>
      {children}
    </ThemeProvider>
  );
}
