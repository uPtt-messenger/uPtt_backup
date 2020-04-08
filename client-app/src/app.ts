import { app } from 'electron';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from './lib/window-manager';
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
    }
  }

}
