module.exports = {
	transpileDependencies: ["vuetify"],
	devServer: {
		proxy: "http://127.0.0.1:5000/ "
	},
	chainWebpack: config => {
		config.module
			.rule("raw")
			.test(/\.md$/)
			.use("raw-loader")
			.loader("raw-loader")
			.end();
	}
};
