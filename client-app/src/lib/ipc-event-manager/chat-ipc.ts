import { LogManager } from '../log-manager';
import { LoginSubject } from '../login-subject';
import { ipcMain } from 'electron';
import { map } from 'rxjs/operators';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { WindowManager } from '../window-manager';
(global as any).WebSocket = require('ws');

export class ChatIpc {

    private privateWs: WebSocketSubject<unknown>;

    constructor(
        private logger: LogManager,
        private loginSubject: LoginSubject,
        private windowManager: WindowManager) {
        loginSubject.getUser.subscribe(user => {
            this.privateWs = webSocket({ url: 'ws://localhost:50732/uptt/private?token=' + user.token });
        });
    }

    public init(): void {
        this.logger.debug('init chat ipc...');
        ipcMain.on('post-chat', (event, data) => {
            this.logger.debug('event: post-chat');
            this.logger.debug(data);
            this.privateWs.multiplex(
                () => ({ operation: 'sendwaterball', payload: { pttId: data.pttId, content: data.msgContent } }),
                () => ({ type: 'unsubscribe', tag: 'sendwaterball' }),
                (resp: any) => {
                    console.log('gggggggggggggggg');
                    console.log(resp);
                    return resp.operation === 'sendwaterball';
                }
              ).subscribe({
                  next: (resp: any) => {
                    this.logger.debug('event: post-chat-resp');
                    event.reply('post-chat-resp', resp);
                    this.logger.debug('post-chat-resp: ' + data);
                    // if (resp.code === 0) {
                    //   this.loginSubject.setUser({ pttId: data.pttId, token: resp.payload.token });
                    // }
                    // event.reply('login-resp', resp);
                  },
                  error: e => this.logger.error(e)
              });
        });
    }

}
