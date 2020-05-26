import { app, BrowserWindow, Menu, Tray } from 'electron';
import * as path from 'path';
import * as url from 'url';
import { ConfigManager } from '../config-manager';
import { WindowItem } from './window-item';
import { LogManager } from '../log-manager';
import { LoginSubject } from '../login-subject';
import { WindowMap } from '@uptt/util/window-map';

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
      url: {
        pathname: './resource/index.html'
      },
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
    },
    {
      name: 'new-chat',
      url: {
        pathname: './resource/index.html',
        hash: '/main-window/new-chat'
      },
      window: null,
      options: {
        width: 350,
        height: 450,
        title: 'uPtt - 丟水球',
        icon: 'resource/assets/images/uptt.ico',
        webPreferences: {
          nodeIntegration: true,
        }
      }
    }
  ];

  private chatWindowPool: WindowMap = {};

  constructor(
    private logger: LogManager,
    private configManager: ConfigManager,
    private loginSubject: LoginSubject) { }

  public openLogin(): void {
    this.openWindow('login');
    this.loginSubject.isLogined.asObservable().subscribe(isLogined => {
      if (isLogined) {
        this.logger.debug(`login success, close login window...`);
        this.closeWindow('login');
      }
    });
  }

  public openNewChat(): void {
    this.openWindow('new-chat');
  }

  public openChat(pttId: string): void {
    if (pttId) {
      if (this.chatWindowPool[pttId]) {
        const windowItem = this.chatWindowPool[pttId];
        this.logger.debug(`chat window ${pttId} is exist.`);
        windowItem.window.show();
      } else {
        this.logger.debug(`chat window ${pttId} doesn't create yet, create window now...`);

        const windowItem: any = {
          name: `chat-${pttId}`,
          url: {
            pathname: './resource/index.html',
            hash: `/chat-window/${pttId}`
          },
          window: null,
          options: {
            width: 400,
            height: 700,
            title: `uPtt - ${pttId}`,
            icon: 'resource/assets/images/uptt.ico',
            webPreferences: {
              nodeIntegration: true,
            }
          }
        };
        windowItem.window = new BrowserWindow(windowItem.options);

        windowItem.window.loadURL(url.format({
          pathname: path.join(this.configManager.get('dirPath'), windowItem.url.pathname),
          protocol: 'file:',
          slashes: true,
          hash: windowItem.url.hash,
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
          return false;
        });

        this.chatWindowPool[pttId] = windowItem;
      }
    }
  }

  private openWindow(windowName: string): void {
    if (windowName) {
      const windowItem = this.windowPool.find((item) => item.name === windowName);
      if (windowItem) {
        if (windowItem.window === null) {
          this.logger.debug(`window ${windowName} doesn't create yet, create window now...`);
          windowItem.window = new BrowserWindow(windowItem.options);
          windowItem.window.loadURL(url.format({
            pathname: path.join(this.configManager.get('dirPath'), windowItem.url.pathname),
            protocol: 'file:',
            slashes: true,
            hash: windowItem.url.hash
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

  public closeWindow(windowName: string): void {
    if (windowName) {
      const windowItem = this.windowPool.find((item) => item.name === windowName);
      if (windowItem) {
        if (windowItem.window != null) {
          windowItem.window.close();
        }
      }
    }
  }

}
