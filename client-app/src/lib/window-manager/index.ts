import { app, BrowserWindow, Menu, Tray } from 'electron';
import * as path from 'path';
import * as url from 'url';
import { ConfigManager } from '../config-manager';
import { WindowItem } from './window-item';
import { LogManager } from '../log-manager';

const DEBUG_MODE = true;

// app.on('ready', () => {
//   screen = electron.screen;
//   // initWebsocket();
//   // createWindow();
// });

export class WindowManager {

  private windowPool: WindowItem[] = [
    {
      name: 'login',
      url: './resource/index.html',
      window: null,
      options: {
        width: 400,
        height: 700,
        title: 'uPtt',
        icon: 'resource/assets/images/uptt.ico',
        webPreferences: {
          nodeIntegration: true,
        }
      }
    }
  ];

  constructor(private logger: LogManager, private configManager: ConfigManager) { }

  public openLogin(): void {
    this.openWindow('login');
  }

  private openWindow(windowName: string): void {
    if (windowName) {
      const windowItem = this.windowPool.find((item) => item.name === windowName);
      if (windowItem) {
        if (windowItem.window === null) {
          this.logger.debug(`window ${windowName} is null.`);
          windowItem.window = new BrowserWindow(windowItem.options);
          windowItem.window.loadURL(url.format({
            pathname: path.join(this.configManager.get('dirPath'), './resource/index.html'),
            protocol: 'file:',
            slashes: true,
          }));
          // Open the DevTools.
          if (DEBUG_MODE) {
            windowItem.window.webContents.openDevTools();
          }
          // 視窗關閉時會觸發。
          windowItem.window.on('closed', () => {
            // 拿掉 window 物件的參照。如果你的應用程式支援多個視窗，
            // 你可能會將它們存成陣列，現在該是時候清除相關的物件了。
            windowItem.window = null;
          });

          windowItem.window.on('close', (event: any) => {
            event.preventDefault();
            windowItem.window.hide();
            // if (!app.isQuiting) {
            // }
            // 建立 System Tray
            // const contextMenu = Menu.buildFromTemplate([
            //   { label: '登入', type: 'normal', click: function (){
            //     windowItem.window.show();
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
          this.logger.debug(`window ${windowName} is exist.`);
          windowItem.window.show();
        }
      }
    }
  }

  public hideWindow(windowName: string): void {
    if (windowName) {
      const windowItem = this.windowPool.find((item) => item.name === windowName);
      if (windowItem) {
        if (windowItem.window != null) {
          windowItem.window.hide();
        }
      }
    }
  }

}
