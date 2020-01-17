import { Injectable } from '@angular/core';
import { ipcRenderer, webFrame, remote } from 'electron';

@Injectable()
export class ElectronService {

  ipcRenderer: typeof ipcRenderer;
  webFrame: typeof webFrame;
  remote: typeof remote;
  // childProcess: typeof childProcess;
  // fs: typeof fs;

  constructor() {
    if (this.isElectron) {
      this.ipcRenderer = window.require('electron').ipcRenderer;
      this.webFrame = window.require('electron').webFrame;
      this.remote = window.require('electron').remote;
      // this.childProcess = window.require('child_process');
      // this.fs = window.require('fs');
    }
  }

  get isElectron(): boolean {
    return window && window.process && window.process.type;
  }

}
