const makeConfig = require('idgx-recipe-staticresources'),
      CopyWebpackPlugin = require('copy-webpack-plugin'),
      ExtractTextPlugin = require('extract-text-webpack-plugin'),
      HardSourceWebpackPlugin = require('hard-source-webpack-plugin');


module.exports = makeConfig(
  // name
  'idgx.portal',

  // shortName
  'idgxportal',

  // path
  `${__dirname}/../src/idgx/portal/browser/static`,

  //publicPath
  '++resource++idgx.portal/',

  //callback
  (config, options) => {
    config.entry.unshift(
      './app/img/preview.png',
    );

    config.output['filename'] = `${options.shortName}.js`;

    config.plugins = [
      // Speed up module build
      new HardSourceWebpackPlugin(),
      // Default CSS generation configuration
      new ExtractTextPlugin({
        filename: `${options.shortName}.css`,
        allChunks: true
      }),
    ]
  },
);
