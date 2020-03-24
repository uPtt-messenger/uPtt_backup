import log from 'electron-log';

export class LogManager {

  private DEBUG_MODE = true;

  constructor() {}

  public error(logContent: string): void {
    if (this.DEBUG_MODE) {
      log.error(logContent);
    }
  }

  public warn(logContent: string): void {
    if (this.DEBUG_MODE) {
      log.warn(logContent);
    }
  }

  public info(logContent: string): void {
    if (this.DEBUG_MODE) {
      log.info(logContent);
    }
  }

  public verbose(logContent: string): void {
    if (this.DEBUG_MODE) {
      log.verbose(logContent);
    }
  }

  public debug(logContent: string): void {
    if (this.DEBUG_MODE) {
      log.debug(logContent);
    }
  }

  public silly(logContent: string): void {
    if (this.DEBUG_MODE) {
      log.silly(logContent);
    }
  }

}
