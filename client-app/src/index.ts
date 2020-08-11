import { App } from './app';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from './lib/window-manager';
import { LoginSubject } from './lib/login-subject';
import { IpcEventManager } from './lib/ipc-event-manager';
import { TrayManager } from './lib/tray-manager';
import { ChatIpc } from './lib/ipc-event-manager/chat-ipc';

const logger = new LogManager();
const configManager = new ConfigManager();
const loginSubject = new LoginSubject();
const windowManager = new WindowManager(logger, configManager, loginSubject);
const chatIpc = new ChatIpc(logger, loginSubject, windowManager);
const ipcEventManager = new IpcEventManager(logger, loginSubject, windowManager, chatIpc);
const trayManager = new TrayManager(logger, loginSubject, windowManager);

const upttClient = new App(logger, configManager, windowManager, trayManager, ipcEventManager);
upttClient.start();
