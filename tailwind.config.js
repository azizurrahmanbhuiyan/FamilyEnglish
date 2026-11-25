/** Build: npx tailwindcss -i static/css/tailwind.input.css -o static/css/app.css --minify */
module.exports = {
  content: ["./studio/**/*.py", "./templates/**/*.html", "./core/**/*.py", "./learning/**/*.py", "./practice/**/*.py", "./course/**/*.py", "./growth/**/*.py", "./static/js/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '"Hind Siliguri"', "system-ui", "sans-serif"],
        display: ['"Plus Jakarta Sans"', '"Hind Siliguri"', "system-ui", "sans-serif"],
        bn: ['"Hind Siliguri"', "sans-serif"],
      },
      colors: {
        // v12 night theme: sky-blue actions, violet accents, marigold highlights (dark surfaces come from theme.css).
        brand: { 50: "#eaf4ff", 100: "#d3e8ff", 200: "#a9d2ff", 300: "#78b8ff", 400: "#46a8ff", 500: "#1d8fff", 600: "#1677e0", 700: "#155fb4", 800: "#174f8f", 900: "#173f6e" },
        violet: { 50: "#f3efff", 100: "#e6dcff", 200: "#cdb9ff", 300: "#b294ff", 400: "#9b7bff", 500: "#8b6bff", 600: "#7550f0", 700: "#5f3dcc", 800: "#4b31a3", 900: "#3a2880" },
        purple: { 50: "#f3efff", 100: "#e6dcff", 200: "#cdb9ff", 300: "#b294ff", 400: "#9b7bff", 500: "#8b6bff", 600: "#7550f0", 700: "#5f3dcc", 800: "#4b31a3", 900: "#3a2880" },
        fuchsia: { 50: "#fdf6e7", 100: "#fbe9c4", 200: "#f6d58f", 300: "#f1c063", 400: "#e9a93c", 500: "#d98e22", 600: "#b9731a", 700: "#935a17", 800: "#764816", 900: "#5f3a14" },
        indigo: { 50: "#eaf4ff", 100: "#d3e8ff", 200: "#a9d2ff", 300: "#78b8ff", 400: "#46a8ff", 500: "#1d8fff", 600: "#1677e0", 700: "#155fb4", 800: "#174f8f", 900: "#173f6e" },
        marigold: { 50: "#fdf6e7", 100: "#fbe9c4", 400: "#e9a93c", 500: "#d98e22", 600: "#b9731a" },
        paper: "#faf6ee",
      },
    },
  },
  plugins: [],
};
