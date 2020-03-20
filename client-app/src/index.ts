import { App } from './app';
import { LogManager } from './lib/log-manager';
import { ConfigManager } from './lib/config-manager';
import { WindowManager } from './lib/window-manager';

const logger = new LogManager();
const configManager = new ConfigManager();
const windowManager = new WindowManager(configManager);

const upttClient = new App(logger, configManager, windowManager);
upttClient.start();
