import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Adaptive Loop — Intervention Intelligence Engine",
  description: "Closed-loop protocol evaluation between testing cycles for longevity medicine.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
