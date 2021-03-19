const makeConfig = require('idgx-recipe-staticresources');


module.exports = makeConfig(
  // name
  'idgx.portal',

  // shortName
  'idgxportal',

  // path
  `${__dirname}/dist`,
  `${__dirname}/../src/idgx/portal/browser/static`,

  //publicPath
  '++resource++idgx.portal/',

  //callback
  (config, options) => {
    config.entry.unshift(
      './app/img/preview.png',
    );
  },
);
