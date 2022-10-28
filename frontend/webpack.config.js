const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const path = require('path');

module.exports = function(env, { mode }) {
  const production = mode === 'production';
  return {
    mode: production ? 'production' : 'development',
    devtool: production ? 'source-map' : 'inline-source-map',
    entry: {
      home: ['./src/pages/home/index.ts'],
      profile: ['./src/pages/profile/index.ts'],
      signon: ['./src/pages/signon/index.ts'],
      inbox: ['./src/pages/inbox/index.ts'],
      followers: ['./src/pages/followers/index.ts'],
    },
    output: {
      filename: '[name].js',
      path: __dirname + '/build',
      chunkFilename: production ? '[id].[chunkhash].js' : '[id].chunk.js'
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
      liveReload: true,
      compress: true,
      headers: {
        'Access-Control-Allow-Origin': '*'
      }
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
            name: 'assets/images/[name].[ext]',
          },
        }
      ]
    }
  }
}