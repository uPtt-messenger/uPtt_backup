'use strict';

/**
 * Dependencies
 */
const electron = require( 'electron' );
const app = electron.app;

 /**
 * Uptt lib
 */
const logger = require('./lib/log-manager');
const WindowManager = require('./lib/window-manager');
const ConfigManager = require('./lib/config-manager');

const DEBUG_MODE = true;
// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.

module.exports = function() {
  logger.debug('uptt-client start');

  ConfigManager.init();

  if ( app.isReady() ) {
    // TODO:
  } else {
    app.on('ready', function() {
      console.log('app ready');
      WindowManager.openLogin()
    });
  }
};
