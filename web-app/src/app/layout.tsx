import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JurisLens — Elastic Agent Builder Pro",
  description: "Autonomous Compliance powered by ELSER v2 & ES|QL.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
