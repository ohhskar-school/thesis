const defaultTheme = require('tailwindcss/defaultTheme');

const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		fontFamily: {
			mono: ['Roboto Mono', ...defaultTheme.fontFamily.mono]
		},
		extend: {}
	},

	plugins: []
};

module.exports = config;
