/** @type {import('tailwindcss').Config} */
const withMT = require("@material-tailwind/react/utils/withMT");

module.exports = withMT({
	content: [
	  "./app/**/*.{js,ts,jsx,tsx}",
	  "./pages/**/*.{js,ts,jsx,tsx}",
	  "./components/**/*.{js,ts,jsx,tsx}",
   
	  // Or if using `src` directory:
	  "./src/**/*.{js,ts,jsx,tsx}",
	],
	theme: {
	  extend: {},
	},
	plugins: [require("flowbite/plugin")],
  })