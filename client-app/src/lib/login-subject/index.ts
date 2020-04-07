import { BehaviorSubject } from 'rxjs';
import { User } from '../shared/model/user';

export class LoginSubject {

  public isLogined = new BehaviorSubject<boolean>(false);
  public getUser = new BehaviorSubject<User>({pttId: '', token: ''});

  constructor() {}

  public setUser(user: User): void {
    this.isLogined.next(true);
    this.getUser.next(user);
  }

}
