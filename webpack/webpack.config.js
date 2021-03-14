const makeConfig = require('idgx-recipe-staticresources');


module.exports = makeConfig(
  // name
  'idgx.portal',

  // shortName
  'idgxportal',

  // path
  `${__dirname}/dist`,
  // `${__dirname}/../src/idgx/portal/browser/static`,
  // `${__dirname}/../src/idgx/portal/theme`,

  //publicPath
  '',
  // '++resource++idgx.portal/',
  // '++theme++idgx.portal/',

  //callback
  (config, options) => {
  },
);
