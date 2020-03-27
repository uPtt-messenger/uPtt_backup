import { LogManager } from '../log-manager';
import { ipcMain } from 'electron';
import { map } from 'rxjs/operators';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
(global as any).WebSocket = require('ws');

export class IpcEventManager {

    private publicWs: WebSocketSubject<unknown>;

    constructor(private logger: LogManager) {
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
                    event.reply('login-resp', resp);
                    this.logger.debug('login-resp: ' + data);
                    if (resp.code === 0) {
                        // upttData.user.pttId = data.pttId;
                        // upttData.user.token = resp.payload.token;
                    }
                    //  else {
                    //   throw resp;
                    // }
                })
            ).subscribe((x: any) => this.logger.debug(x));
        });
    }

}
