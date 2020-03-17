import log from 'electron-log';

export class LogManager {

  constructor() {}

  public error(logContent: string): void {
    log.error(logContent);
  }

  public warn(logContent: string): void {
    log.warn(logContent);
  }

  public info(logContent: string): void {
    log.info(logContent);
  }

  public verbose(logContent: string): void {
    log.verbose(logContent);
  }

  public debug(logContent: string): void {
    log.debug(logContent);
  }

  public silly(logContent: string): void {
    log.silly(logContent);
  }

}
