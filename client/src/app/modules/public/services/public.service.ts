import { Injectable } from '@angular/core';
import { Observable, throwError, Subject } from 'rxjs';
import { map,  } from 'rxjs/operators';
import { ElectronService } from '../../shared/services/electron.service';

@Injectable()
export class PublicService {

  // private ws = webSocket({
  //   url: 'ws://localhost:50732/uptt/public',
  //  // openObserver: open$
  // });

  constructor(private electronService: ElectronService) { }

  login(loginCredentials: { pttId: string, pwd: string }): Observable<any> {
    const rtnSubject = new Subject<any>();
    this.electronService.ipcRenderer.send('login', loginCredentials);
    this.electronService.ipcRenderer.once('login-resp', (event, resp) => {
      console.log(resp);
      rtnSubject.next(resp);
    });
    return rtnSubject.asObservable().pipe(
      map(resp => {
        if (resp.code === 0) {
          return resp.payload;
        } else {
          throw resp;
        }
      })
    );

    // return this.ws.multiplex(
    //   () => ({ operation: 'login', payload: { pttId: loginCredentials.pttId, pwd: loginCredentials.pwd } }),
    //   () => ({ type: 'unsubscribe', tag: 'login' }),
    //   (resp: {operation: string}) => resp.operation === 'login'
    // ).pipe(
    //   map(resp => {
    //     if (resp.code === 0) {
    //       return resp.payload;
    //     } else {
    //       throw resp;
    //     }
    //   })
    //   // catchError
    // );
  }

}
