/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
        colors :{
          'main-color' : '#053B50',
          'primary-highlight' : '#176b87',
          'highlight' : '#64CCC5',
          'highlight-dark' : '#56aca6',
          'highlight-dark-light' : '#74e3dc',
          'highlight-light' : '#F3E9CC',
          'accent' : '#F5E2D9'
        }
      },
  },
  plugins: [],
}

