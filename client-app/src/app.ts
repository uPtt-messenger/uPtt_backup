import { app } from 'electron';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from './lib/window-manager';
import { IpcEventManager } from './lib/ipc-event-manager';

export class App {

  constructor(
      private logger: LogManager,
      private configManager: ConfigManager,
      private windowManager: WindowManager,
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
        this.windowManager.openLogin();
      });
    }
  }

}
