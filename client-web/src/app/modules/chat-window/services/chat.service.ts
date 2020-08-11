import { Injectable } from '@angular/core';
import { Observable, throwError, Subject, BehaviorSubject } from 'rxjs';
import { map,  } from 'rxjs/operators';
import { ElectronService } from '../../shared/services/electron.service';

@Injectable()
export class ChatService {

  constructor(private electronService: ElectronService) { }

  postChat(chatObj: { pttId: string, msgContent: string }): Observable<any> {
    if (this.electronService.isElectron) {
      const rtnSubject = new Subject<any>();
      this.electronService.ipcRenderer.send('post-chat', chatObj);
      this.electronService.ipcRenderer.once('post-chat-resp', (event, resp) => {
        console.log('get post-chat-resp: ', resp);
        rtnSubject.next(resp);
      });
      return rtnSubject.asObservable().pipe(
        map(resp => {
          console.log('[ChatService][postChat] rtnSubject resp!');
          if (resp.code === 0) {
            return resp.payload;
          } else {
            throw resp;
          }
        })
      );
    } else {
      // TODO: is web mode
      console.log('is web mode');
    }
  }

}
