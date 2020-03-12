'use strict';

/**
 * External Dependencies
 */
const log = require('electron-log');

module.exports = {
  error: function(logContent) {
    log.error(logContent);
  },
	warn: function(logContent) {
    log.warn(logContent);
  },
  info: function(logContent) {
    log.info(logContent);
  },
  verbose: function(logContent) {
    log.verbose(logContent);
  },
  debug: function(logContent) {
    log.debug(logContent);
  },
  silly: function(logContent) {
    log.silly(logContent);
  }
};
