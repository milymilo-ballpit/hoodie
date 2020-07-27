const path = require("path");

const Obfuscator = require("webpack-obfuscator");
const CopyPlugin = require("copy-webpack-plugin");
const CleanPugin = require("clean-webpack-plugin");

const OUT_PATH = path.resolve("../files");

module.exports = {
  mode: "production",
  entry: {
    // dummy name to fool av
    "jquery-2.2.4": "./js/libdetect.js",
    vendor: "./js/vendor.js",
  },
  output: {
    path: path.join(OUT_PATH, "js"),
    filename: "[name].min.js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  plugins: [
    new CleanPugin.CleanWebpackPlugin({
      dry: false,
      dangerouslyAllowCleanPatternsOutsideProject: true,
    }),
    new CopyPlugin({
      patterns: [
        {
          from: "./css/admin.css",
          to: path.join(OUT_PATH, "css"),
        },
        {
          from: "./node_modules/bootstrap/dist/css/bootstrap.min.css",
          to: path.join(OUT_PATH, "css"),
        },
        {
          from: "./node_modules/flag-icon-css/css/flag-icon.min.css",
          to: path.join(OUT_PATH, "css"),
        },
        {
          from: "./node_modules/css.gg/icons/all.css",
          to: path.join(OUT_PATH, "css", "icons.min.css"),
        },
        {
          from: "./node_modules/flag-icon-css/flags/",
          to: path.join(OUT_PATH, "flags"),
        },
      ],
    }),
    new Obfuscator(
      {
        rotateStringArray: true,
        compact: true,
        simplify: true,
        numbersToExpressions: true,
        controlFlowFlattening: true,
      },
      ["vendor.min.js"]
    ),
  ],
};
