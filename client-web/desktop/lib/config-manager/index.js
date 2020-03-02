'use strict';

/**
 * External Dependencies
 */
const path = require('path');

/**
 * Module variables
 */
let config = new Map();

module.exports = {
  init: function() {
    let dirPath = __dirname;
    dirPath = dirPath.substring(0, dirPath.indexOf('desktop'));
    this.add('dirPath', dirPath);
    console.log('dirPath', path.join(__dirname, './build/index.html'),);
  },
	get: function(configName) {
    if (configName) {
      return config.get(configName);
    } else {
      return null;
    }
  },
  add: function(configName, configValue) {
    if (configName) {
      config.set(configName, configValue);
    }
  }
};
