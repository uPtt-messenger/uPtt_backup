import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { FormBuilder, FormGroup, FormControl } from '@angular/forms';
import { ChatMessage } from 'src/app/modules/core/models/chat-message';
import { ActivatedRoute } from '@angular/router';
import { ElectronService } from 'src/app/modules/shared/services/electron.service';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-chat-window',
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.scss']
})
export class ChatWindowComponent implements OnInit, AfterViewChecked {

  @ViewChild('messageBox', {static: true}) private messageBoxRef: ElementRef;

  chatMsgList: ChatMessage[] = [
    { msgType: 2, msgTime: '2020/02/02 01:16:25', sender: 'CodingMan', msgContent: '測試測試測試測試' },
    { msgType: 1, msgTime: '2020/02/02 01:16:35', sender: 'mobi76', msgContent: '測試測試測試測試測試測試測試測試測試測試' },
    { msgType: 1, msgTime: '2020/02/02 01:16:52', sender: 'mobi76', msgContent: '測試測試測試' },
    { msgType: 2, msgTime: '2020/02/02 01:17:01', sender: 'CodingMan', msgContent: '測試測試測試測試' },
    { msgType: 1, msgTime: '2020/02/02 01:17:16', sender: 'mobi76', msgContent: '測試測試測試測試測試測試測試' }
  ];

  chatMsgLen = 0;
  chatForm: FormGroup;

  pttId: string;

  constructor(
      private route: ActivatedRoute,
      private fb: FormBuilder,
      private chatService: ChatService) {
    this.chatForm = this.fb.group({
      chatMsg: []
    });
    this.chatForm.controls.chatMsg.valueChanges.subscribe(value => {
      this.chatMsgLen = (value) ? value.length : 0;
    });
  }

  ngOnInit() {
    this.pttId = this.route.snapshot.paramMap.get('pttId');
    console.log('[chat-window] pttId: ' + this.pttId);
    this.scrollToBottom();
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  submitMsg(event) {
    event.preventDefault();
    const chatMsg = this.chatForm.get('chatMsg').value;
    if (chatMsg) {
      this.chatService.postChat({ pttId: this.pttId, msgContent: chatMsg }).subscribe({
        next: resp => {
          // TODO: get API response
          console.log('[submitMsg] get response ');
          this.chatMsgList.push({ msgType: 1, msgTime: '2020/02/03 00:30:16', sender: this.pttId, msgContent: chatMsg });
          this.chatForm.reset();
        },
        error: error => {
          console.error('submitMsg error', error);
          // TODO: handle error
        }
      });
    }
  }

  scrollToBottom(): void {
    try {
        this.messageBoxRef.nativeElement.scrollTop = this.messageBoxRef.nativeElement.scrollHeight;
    } catch (err) { }
  }

}
