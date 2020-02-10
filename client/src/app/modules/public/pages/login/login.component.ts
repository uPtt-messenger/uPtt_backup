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

  constructor(
      private electronService: ElectronService,
      private fb: FormBuilder,
      private router: Router,
      private publicService: PublicService) {
    this.loginForm = this.fb.group({
      loginPttId: [''],
      loginPwd: ['']
    });
  }

  ngOnInit() {
  }

  login() {
    console.log('login');
    // TODO: call login API
    this.publicService.login(this.loginForm.value);
    this.publicService.login$.subscribe(message => console.log(message));

    // if (this.electronService.isElectron) {
    //   this.electronService.ipcRenderer.send('login-success', this.loginForm.value);
    // } else {
    //   this.router.navigate(['/main-window']);
    // }
  }
}
