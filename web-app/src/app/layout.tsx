import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JurisLens — Autonomous Compliance Guardian",
  description: "Navigate Global Financial Regulations with Autonomous Precision, powered by Elasticsearch.",
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
