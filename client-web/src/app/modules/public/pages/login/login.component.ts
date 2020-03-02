import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { ElectronService } from 'src/app/modules/shared/services/electron.service';
import { PublicService } from '../../services/public.service';
import { Observable, Subscription } from 'rxjs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {

  private loginSubscription: Subscription ;
  loginForm: FormGroup;
  loginFail = false;

  constructor(
      private electronService: ElectronService,
      private fb: FormBuilder,
      private router: Router,
      private publicService: PublicService) {
    this.loginForm = this.fb.group({
      pttId: [''],
      pwd: ['']
    });
  }

  ngOnInit() {
  }

  ngOnDestroy() {
    this.loginSubscription.unsubscribe();
  }

  login() {
    this.loginSubscription = this.publicService.login(this.loginForm.value).subscribe({
      next: resp => {
        if (this.electronService.isElectron) {
          this.electronService.ipcRenderer.send('login-success', { pttId: this.loginForm.get('pttId').value, token: resp.token });
        } else {
          this.router.navigate(['/main-window']);
        }
      },
      error: error => {
        // TODO: error handle
        this.loginForm.reset({pttId: this.loginForm.get('pttId').value});
        this.loginFail = true;
      }
    });
  }
}

