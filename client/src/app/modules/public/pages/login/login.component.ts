import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { ElectronService } from 'src/app/modules/shared/services/electron.service';

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
      private router: Router) {
    this.loginForm = this.fb.group({
      loginPttId: [''],
      loginPwd: ['']
    });
  }

  ngOnInit() {
  }

  login() {
    console.log('login');
    if (this.electronService.isElectron) {
      this.electronService.ipcRenderer.send('login-success');
    }
    this.router.navigate(['/main-window']);
  }
}
