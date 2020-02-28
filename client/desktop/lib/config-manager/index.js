'use strict';

/**
 * External Dependencies
 */

/**
 * Module variables
 */
let config = new Map();

module.exports = {
  init: function() {

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
      config.add(configName, configValue);
    }
  }
};
