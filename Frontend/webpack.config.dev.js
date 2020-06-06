const webpack = require("webpack");
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { spawn } = require("child_process");
const base_conifg = require("./webpack.config.base");
const merge = require("webpack-merge");

// Config directories
const SRC_DIR = path.resolve(__dirname, "src");
const OUTPUT_DIR = path.resolve(__dirname, "dist");

// Any directories you will be adding code/files into, need to be added to this array so webpack will pick them up
const defaultInclude = [SRC_DIR];

module.exports = merge.smart(base_conifg, {
  entry: SRC_DIR + "/index.js",
  output: {
    path: OUTPUT_DIR,
    publicPath: "/",
    filename: "bundle.js",
    libraryTarget: "commonjs2",
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [{ loader: "style-loader" }, { loader: "css-loader" }],
        include: defaultInclude,
      },
      {
        test: /\.scss$/,
        use: ["style-loader", "css-loader", "sass-loader"],
      },
      {
        test: /\.(jpe?g|png|gif)$/,
        use: [{ loader: "file-loader?name=img/[name]__[hash:base64:5].[ext]" }],
        include: defaultInclude,
      },
      {
        test: /\.(eot|svg|ttf|woff|woff2)$/,
        use: [
          { loader: "file-loader?name=font/[name]__[hash:base64:5].[ext]" },
        ],
        include: defaultInclude,
      },
    ],
  },
  target: "electron-renderer",
  plugins: [
    new HtmlWebpackPlugin(),
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("development"),
    }),
  ],
  devtool: "cheap-source-map",
  devServer: {
    contentBase: OUTPUT_DIR,
    port: 42069,
    stats: {
      colors: true,
      chunks: false,
      children: false,
    },
    setup() {
      spawn("electron", ["."], {
        shell: true,
        env: process.env,
        stdio: "inherit",
      })
        .on("close", (code) => process.exit(0))
        .on("error", (spawnError) => console.error("xD", spawnError));
    },
  },
  mode: "development",
});