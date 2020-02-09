import { Injectable } from '@angular/core';
import { webSocket } from 'rxjs/webSocket';

@Injectable()
export class PublicService {

  private ws = webSocket({
    url: 'ws://localhost:50732/uptt/public',
   // openObserver: open$
  });

  login$ = this.ws.multiplex(
    () => ({ type: 'subscribe', tag: 'login' }),
    () => ({ type: 'unsubscribe', tag: 'login' }),
    (resp: {operation: string}) => resp.operation === 'login'
  );

  constructor() { }

  login(loginCredentials: { pttId: string, pwd: string }): void {
    this.ws.next({
      operation: 'login',
      payload: {
        pttId: loginCredentials.pttId,
        pwd: loginCredentials.pwd
      }
    });
  }


}
