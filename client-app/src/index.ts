import { App } from './app';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from '@uptt/window/window-manager';
import { LoginSubject } from './lib/login-subject';
import { IpcEventManager } from './lib/ipc-event-manager';
import { TrayManager } from './lib/tray-manager';

const logger = new LogManager();
const configManager = new ConfigManager();
const loginSubject = new LoginSubject();
const windowManager = new WindowManager(logger, configManager, loginSubject);
const ipcEventManager = new IpcEventManager(logger, loginSubject, windowManager);
const trayManager = new TrayManager(logger, loginSubject, windowManager);

const upttClient = new App(logger, configManager, windowManager, trayManager, ipcEventManager);
upttClient.start();
