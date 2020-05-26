import { app } from 'electron';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from '@uptt/window/window-manager';
import { IpcEventManager } from './lib/ipc-event-manager';
import { TrayManager } from './lib/tray-manager';

export class App {

  constructor(
      private logger: LogManager,
      private configManager: ConfigManager,
      private windowManager: WindowManager,
      private trayManager: TrayManager,
      private ipcEventManager: IpcEventManager) {

    this.logger.debug('uptt-client start');
    this.configManager.init();
  }

  public start(): void {
    if ( app.isReady() ) {
      // TODO:
    } else {
      app.on('ready', () => {
        this.logger.debug('app ready');
        this.ipcEventManager.initPublic();
        this.trayManager.initTray();
        this.windowManager.openLogin();
      });
      app.on('window-all-closed', () => {
        this.logger.debug('app window-all-closed');
        // On OS X it is common for applications and their menu bar
        // to stay active until the user quits explicitly with Cmd + Q
        if (process.platform !== 'darwin') {
          app.quit();
        }
      });
    }
  }

}
