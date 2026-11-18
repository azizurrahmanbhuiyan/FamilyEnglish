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
        brand: { 50: "#fff1f2", 100: "#ffe4e6", 500: "#f43f5e", 600: "#e11d48", 700: "#be123c" },
      },
    },
  },
  plugins: [],
};
