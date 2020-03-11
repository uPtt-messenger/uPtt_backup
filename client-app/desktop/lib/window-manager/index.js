'use strict';

/**
 * Env
 */
const DEBUG_MODE = true;

/**
 * External Dependencies
 */
const electron = require( 'electron' );
const BrowserWindow = electron.BrowserWindow;
const app = electron.app;
const Tray = electron.Tray;
const Menu = electron.Menu;

/**
 * Uptt lib
 */
const ConfigManager = require('../config-manager');

// app.on('ready', () => {
//   screen = electron.screen;
//   // initWebsocket();
//   // createWindow();
// });

const url = require('url');
const path = require('path');

/**
 * Module variables
 */
let tray = null;
const windows = {
  login: {
    url: './resource/index.html',
    window: null,
    options: {
      width: 400,
      height: 700,
      title: "uPtt",
      icon:'resource/assets/images/uptt.ico',
      webPreferences: {
        nodeIntegration: true
      }
    }
  }
};

function openWindow(windowName) {
  if (windowName && windows[windowName]) {
    const window = windows[windowName];
    if (window.window === null) {
      windows[windowName].window = new BrowserWindow(window.options);
      windows[windowName].window.loadURL(url.format({
        pathname: path.join(ConfigManager.get('dirPath'), './resource/index.html'),
        protocol: 'file:',
        slashes: true
      }));
      // Open the DevTools.
      if (DEBUG_MODE) {
        windows[windowName].window.webContents.openDevTools();
      }
      // 視窗關閉時會觸發。
      windows[windowName].window.on('closed', () => {
        // 拿掉 window 物件的參照。如果你的應用程式支援多個視窗，
        // 你可能會將它們存成陣列，現在該是時候清除相關的物件了。
        windows[windowName].window = null;
      });

      windows[windowName].window.on('close', function (event) {
        if(!app.isQuiting){
            event.preventDefault();
            windows[windowName].window.hide();
        }
        // 建立 System Tray
        // const contextMenu = Menu.buildFromTemplate([
        //   { label: '登入', type: 'normal', click: function (){
        //     windows[windowName].window.show();
        //   }},
        //   { label: '關於', type: 'normal' },
        //   { label: '結束', type: 'normal', click: function() {
        //     app.isQuiting = true;
        //     app.quit();
        //   } }
        // ])
        // // TODO:
        // tray.setContextMenu(contextMenu)
        return false;
      });

    } else {
      windows[windowName].window.show();
    }

  }
}

module.exports = {
	openLogin: function() {
    if (windows['login'].window === null) {
      // 建立 System Tray
      tray = new Tray('resource/assets/images/uptt.ico')
      const contextMenu = Menu.buildFromTemplate([
        { label: '關於', type: 'normal' },
        { label: '結束', type: 'normal', click: function() {
          app.isQuiting = true;
          app.quit();
        } }
      ]);
      tray.setToolTip('uPtt');
      tray.setContextMenu(contextMenu);
    }
		openWindow('login');
  }
};
