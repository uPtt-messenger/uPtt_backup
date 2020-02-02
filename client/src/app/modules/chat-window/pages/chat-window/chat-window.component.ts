import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl } from '@angular/forms';
import { ChatMessage } from 'src/app/modules/shared/models/chat-message';

@Component({
  selector: 'app-chat-window',
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.scss']
})
export class ChatWindowComponent implements OnInit {

  chatMsgList: ChatMessage[] = [
    { msgType: 2, msgTime: '2020/02/02 01:16:25', sender: 'CodingMan', msgContent: '測試測試測試測試' },
    { msgType: 1, msgTime: '2020/02/02 01:16:35', sender: 'mobi76', msgContent: '測試測試測試測試測試測試測試測試測試測試' },
    { msgType: 1, msgTime: '2020/02/02 01:16:52', sender: 'mobi76', msgContent: '測試測試測試' },
    { msgType: 2, msgTime: '2020/02/02 01:17:01', sender: 'CodingMan', msgContent: '測試測試測試測試' },
    { msgType: 1, msgTime: '2020/02/02 01:17:16', sender: 'mobi76', msgContent: '測試測試測試測試測試測試測試' }
  ];

  chatMsgLen = 0;
  chatForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.chatForm = this.fb.group({
      chatMsg: []
    });
    this.chatForm.controls.chatMsg.valueChanges.subscribe(value => {
      this.chatMsgLen = (value) ? value.length : 0;
    });
  }

  ngOnInit() {

  }

  submitMsg(event) {
    event.preventDefault();
    const chatMsg = this.chatForm.get('chatMsg').value;
    if (chatMsg) {
      // TODO: call api
      this.chatMsgList.push({ msgType: 1, msgTime: '2020/02/03 00:30:16', sender: 'mobi76', msgContent: chatMsg });
      this.chatForm.reset();
    }
  }

}
