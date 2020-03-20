import { app } from 'electron';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from './lib/window-manager';

const DEBUG_MODE = true;

export class App {

  constructor(
      private logger: LogManager,
      private configManager: ConfigManager,
      private windowManager: WindowManager) {

    this.logger.debug('uptt-client start');
    this.configManager.init();
  }

  public start(): void {
    if ( app.isReady() ) {
      // TODO:
    } else {
      app.on('ready', () => {
        console.log('app ready');
        this.windowManager.openLogin();
      });
    }
  }

}
