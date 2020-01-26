import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-chat-window',
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.scss']
})
export class ChatWindowComponent implements OnInit {

  chatMsgLen = 0;
  chatForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.chatForm = this.fb.group({
      chatMsg: []
    });
    this.chatForm.controls.chatMsg.valueChanges.subscribe(value => {
      this.chatMsgLen = value.length;
    });
  }

  ngOnInit() {

  }

}
