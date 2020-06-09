import { LogManager } from '../log-manager';
import { LoginSubject } from '../login-subject';
import { ipcMain } from 'electron';
import { map } from 'rxjs/operators';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { WindowManager } from '../window-manager';
import { ChatIpc } from './chat-ipc';
(global as any).WebSocket = require('ws');

export class IpcEventManager {

  private publicWs: WebSocketSubject<unknown>;

  constructor(
    private logger: LogManager,
    private loginSubject: LoginSubject,
    private windowManager: WindowManager,
    private chatIpc: ChatIpc) {
    this.publicWs = webSocket({ url: 'ws://localhost:50732/uptt/public' });
  }

  public initPublic(): void {
    ipcMain.on('login', (event, data) => {
      this.logger.debug('event: login');
      this.logger.debug(data);
      this.publicWs.multiplex(
          () => ({ operation: 'login', payload: { pttId: data.pttId, pwd: data.pwd } }),
          () => ({ type: 'unsubscribe', tag: 'login' }),
          (resp: any) => resp.operation === 'login'
        ).pipe(
          map((resp: any) => {
            // event.reply('login-resp', resp);
            // this.logger.debug('login-resp: ' + data);
            if (resp.code === 0) {
              this.loginSubject.setUser({ pttId: data.pttId, token: resp.payload.token });
              this.chatIpc.init();
              return resp;
            } else {
              throw resp;
            }
          })
        ).subscribe({
            next: (resp: any) => {
              this.logger.debug('login-resp: ' + data);
              if (resp.code === 0) {
                this.loginSubject.setUser({ pttId: data.pttId, token: resp.payload.token });
              }
              event.reply('login-resp', resp);
            },
            error: e => this.logger.error(e)
        });
    });

    ipcMain.on('login-success', (event, data) => {
      this.windowManager.hideWindow('login');
      this.initPrivate();
    });
  }

  private initPrivate(): void {
    this.logger.debug('init private ipc');
    ipcMain.on('new-chat', (event, data) => {
      this.logger.debug('event: new-chat');
      this.logger.debug(data);
      this.windowManager.openChat(data.pttId);
    });
  }

}
