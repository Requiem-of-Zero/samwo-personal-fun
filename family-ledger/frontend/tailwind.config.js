/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}", // if you still have an App.js/tsx
    "./app/**/*.{js,jsx,ts,tsx}", // all pages and layouts
    "./components/**/*.{js,jsx,ts,tsx}",
    "./screens/**/*.{js,jsx,ts,tsx}", // if you ever keep separate screens folder
  ],
  theme: {
    extend: {
      colors: {
        background: "#2E2E33",
        primary: "#6C63FF",
        accent: "#FF6B6B",
        muted: "#999999",
      },
      textColor: {
        primary: "#FFFFFF",
        secondary: "#CCCCCC",
        accent: "#6C63FF",
        muted: "#888888",
      },
    },
  },
  presets: [
    require("nativewind/preset"), // ← add this
  ],
};
