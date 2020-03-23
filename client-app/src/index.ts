import { App } from './app';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from './lib/window-manager';
import { IpcEventManager } from './lib/ipc-event-manager';

const logger = new LogManager();
const configManager = new ConfigManager();
const windowManager = new WindowManager(logger, configManager);
const ipcEventManager = new IpcEventManager(logger);

const upttClient = new App(logger, configManager, windowManager);
upttClient.start();
