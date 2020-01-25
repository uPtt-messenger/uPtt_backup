import { Component, OnInit } from '@angular/core';
import { ElectronService } from 'src/app/modules/shared/services/electron.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-new-chat',
  templateUrl: './new-chat.component.html',
  styleUrls: ['./new-chat.component.scss']
})
export class NewChatComponent implements OnInit {

  constructor(
    private electronService: ElectronService,
    private router: Router
    ) { }

  ngOnInit() {
  }

  submitForm() {
    console.log('login');
    if (this.electronService.isElectron) {
      this.electronService.ipcRenderer.send('new-chat');
    } else {
      this.router.navigate(['/chat-window']);
    }
  }
}
