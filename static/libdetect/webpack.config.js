const path = require("path");
const Obfuscator = require("webpack-obfuscator");

const OUT_PATH = process.env.OUT_PATH || "../files/js";
module.exports = {
  mode: "production",
  entry: {
    libdetect: "./libdetect.js",
  },
  output: {
    path: path.resolve(OUT_PATH),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  plugins: [new Obfuscator({ rotateStringArray: true })],
};
