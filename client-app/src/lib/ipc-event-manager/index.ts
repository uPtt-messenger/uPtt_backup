import { LogManager } from '../log-manager';
import { ipcMain } from 'electron';
import { map } from 'rxjs/operators';

export class IpcEventManager {

    constructor(private logger: LogManager) {
        ipcMain.on('login-success', (event, data) => {
            this.logger.debug('event: login-success');
            this.logger.debug(data);
            publicWs.multiplex(
                () => ({ operation: 'login', payload: { pttId: data.pttId, pwd: data.pwd } }),
                () => ({ type: 'unsubscribe', tag: 'login' }),
                (resp: any) => resp.operation === 'login'
            ).pipe(
                map(resp: any => {
                    event.reply('login-resp', resp);
                    if (resp.code === 0) {
                        upttData.user.pttId = data.pttId;
                        upttData.user.token = resp.payload.token;
                    }
                    //  else {
                    //   throw resp;
                    // }
                })
            ).subscribe(x: any => this.logger.debug(x));
        });
    }

}
