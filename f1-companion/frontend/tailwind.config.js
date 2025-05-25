 /** @type {import('tailwindcss').Config} */
 export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"], // Add this line
  theme: {
    extend: {
      fontFamily: {
        mulish: ['Mulish', 'sans-serif'],
        genos: ['Genos', 'sans-serif']
      }
    },
   },
  plugins: [],
};