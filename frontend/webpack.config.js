const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const path = require('path');

module.exports = function(env, { mode }) {
  const production = mode === 'production';
  return {
    mode: production ? 'production' : 'development',
    devtool: production ? 'source-map' : 'inline-source-map',
    entry: {
      home: ['./src/pages/home/index.ts'],
      profle: ['./src/pages/profile/index.ts'],
    },
    output: {
      filename: '[name].js',
      path: __dirname + '/build',
      chunkFilename: '[id].[chunkhash].js'
    },
    resolve: {
      extensions: ['.ts', '.js', '.png'],
      modules: ['src', 'node_modules']
    },
    devServer: {
      port: 9000,
      historyApiFallback: true,
      open: !process.env.CI,
      devMiddleware: {
        writeToDisk: true,
      },
      compress: true,
      static: {
        directory: path.join(__dirname, './')
      },
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      hot: true
    },
    plugins: [
      new CleanWebpackPlugin()
    ],
    optimization: {
      splitChunks: {
        cacheGroups: {
          commons: {
            name: 'vendors',
            chunks: 'initial',
            minChunks: 2,
          },
        },
      },
    },
    module: {
      rules: [
        {
          test: /\.ts$/i,
          use: [
            {
              loader: 'ts-loader'
            }
          ],
          exclude: /node_modules/
        },
        {
          test: /\.(png|jpe?g|gif|jp2|webp)$/,
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
          },
        }
      ]
    }
  }
}