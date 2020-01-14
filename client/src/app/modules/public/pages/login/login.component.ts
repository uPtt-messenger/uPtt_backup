import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;

  constructor(
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
    this.router.navigate(['/main-window']);
  }
}