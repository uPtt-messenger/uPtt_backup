import { App } from './app';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from './lib/window-manager';
import { LoginSubject } from './lib/login-subject';
import { IpcEventManager } from './lib/ipc-event-manager';

const logger = new LogManager();
const configManager = new ConfigManager();
const windowManager = new WindowManager(logger, configManager);
const loginSubject = new LoginSubject();
const ipcEventManager = new IpcEventManager(logger, loginSubject, windowManager);

const upttClient = new App(logger, configManager, windowManager, ipcEventManager);
upttClient.start();
