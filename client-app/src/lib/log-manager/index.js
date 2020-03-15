/**
 * External Dependencies
 */
const log = require('electron-log');

export function error(logContent){
  log.error(logContent);
}

export function warn(logContent){
  log.warn(logContent);
}

export function info(logContent){
  log.info(logContent);
}

export function verbose(logContent){
  log.verbose(logContent);
}

export function debug(logContent){
  log.debug(logContent);
}

export function silly(logContent){
  log.silly(logContent);
}
