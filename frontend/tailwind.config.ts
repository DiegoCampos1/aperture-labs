import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/providers/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  important: "#__next",
  corePlugins: {
    preflight: false,
  },
  theme: {
    extend: {
      colors: {
        navy: "#1B3A5C",
        "green-accent": "#1DBF73",
        "gray-bg": "#F5F6FA",
        "card-border": "#C5D1E0",
        "input-border": "#D0D5DD",
        "avatar-teal": "#6BB8C4",
      },
    },
  },
  plugins: [],
};

export default config;
