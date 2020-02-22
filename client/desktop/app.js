'use strict';

/**
 * Dependencies
 */
const electron = require( 'electron' );
const app = electron.app;

 /**
 * Uptt lib
 */
const WindowManager = require('./lib/window-manager');

const DEBUG_MODE = true;
// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.

module.exports = function() {
  console.log('uptt-client start');
  // Start the app window
  if ( app.isReady() ) {
    // TODO:
  } else {
    app.on('ready', function() {
      console.log('app ready');
      WindowManager.openLogin()
    });
  }
};
