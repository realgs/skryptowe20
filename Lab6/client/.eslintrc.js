module.exports = {
	root: true,
	env: {
		node: true
	},

	parser: "vue-eslint-parser",

	parserOptions: {
		parser: "@typescript-eslint/parser",
		ecmaVersion: 2020
	},

	extends: [
		"plugin:vue/essential",
		"eslint:recommended",
		"@vue/typescript/recommended",
		"@vue/prettier",
		"@vue/prettier/@typescript-eslint"
	],

	rules: {
		"no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
		"no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
		"@typescript-eslint/interface-name-prefix": "off",
		"@typescript-eslint/no-explicit-any": "off"
	}
};
