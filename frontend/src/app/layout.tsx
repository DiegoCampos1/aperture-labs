import type { Metadata } from "next";
import Providers from "@/providers/Providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "Aperture Labs - Employees",
  description: "Employee time tracking application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div id="__next">
          <Providers>{children}</Providers>
        </div>
      </body>
    </html>
  );
}
