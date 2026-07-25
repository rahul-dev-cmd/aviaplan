import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AviaPlan - Autonomous Trip-Planning Agent",
  description: "Autonomous multi-tool trip planning agent powered by LangGraph, FastAPI, and live API fallback logic.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-cream-50 text-slate-800 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
