import { Component, OnInit } from '@angular/core';
import { ElectronService } from 'src/app/modules/shared/services/electron.service';
import { Router } from '@angular/router';
import { FormGroup, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-new-chat',
  templateUrl: './new-chat.component.html',
  styleUrls: ['./new-chat.component.scss']
})
export class NewChatComponent implements OnInit {

  newChatForm: FormGroup;

  constructor(
      private electronService: ElectronService,
      private fb: FormBuilder,
      private router: Router) {
    this.newChatForm = this.fb.group({
      pttId: ['']
    });
  }

  ngOnInit() {
  }

  submitForm() {
    if (this.electronService.isElectron) {
      this.electronService.ipcRenderer.send('new-chat', { pttId: this.newChatForm.get('pttId').value });
    } else {
      // TODO: Web new chat
      this.router.navigate(['/chat-window']);
    }
  }
}
