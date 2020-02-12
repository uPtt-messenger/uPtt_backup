import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

@Injectable()
export class PublicService {

  private ws = webSocket({
    url: 'ws://localhost:50732/uptt/public',
   // openObserver: open$
  });

  constructor() { }

  login(loginCredentials: { pttId: string, pwd: string }): Observable<any> {
    console.log(loginCredentials);
    return this.ws.multiplex(
      () => ({ operation: 'login', payload: { pttId: loginCredentials.pttId, pwd: loginCredentials.pwd } }),
      () => ({ type: 'unsubscribe', tag: 'login' }),
      (resp: {operation: string}) => resp.operation === 'login'
    ).pipe(
      map(resp => {
        if (resp.code === 0) {
          return resp.payload;
        } else {
          throw resp;
        }
      })
      // catchError
    );
  }


}
