import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { ElectronService } from 'src/app/modules/shared/services/electron.service';
import { PublicService } from '../../services/public.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

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

  login() {
    this.publicService.login(this.loginForm.value).subscribe(
      resp => {
        if (this.electronService.isElectron) {
          this.electronService.ipcRenderer.send('login-success', { token: resp.token });
        } else {
          this.router.navigate(['/main-window']);
        }
      },
      error => {
        // TODO: error handle
        this.loginFail = true;
      }
    );
  }
}
