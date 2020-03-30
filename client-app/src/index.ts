import { App } from './app';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from './lib/window-manager';
import { StorageManager } from './lib/storage-manager';
import { IpcEventManager } from './lib/ipc-event-manager';

const logger = new LogManager();
const configManager = new ConfigManager();
const windowManager = new WindowManager(logger, configManager);
const storageManager = new StorageManager();
const ipcEventManager = new IpcEventManager(logger, storageManager);

const upttClient = new App(logger, configManager, windowManager, ipcEventManager);
upttClient.start();
