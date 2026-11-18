/** Build: npx tailwindcss -i static/css/tailwind.input.css -o static/css/app.css --minify */
module.exports = {
  content: ["./templates/**/*.html", "./core/**/*.py", "./learning/**/*.py", "./static/js/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Nunito", "Hind Siliguri", "system-ui", "sans-serif"],
        display: ['"Baloo 2"', "Nunito", "sans-serif"],
        bn: ['"Hind Siliguri"', "sans-serif"],
      },
      colors: {
        brand: { 50: "#f5f3ff", 100: "#ede9fe", 200: "#ddd6fe", 500: "#8b5cf6", 600: "#7c3aed", 700: "#6d28d9", 800: "#5b21b6" },
      },
    },
  },
  plugins: [],
};
