import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatWindowComponent } from './pages/chat-window/chat-window.component';
import { ChatWindowRoutingModule } from './chat-window-routing.module';
import { ReactiveFormsModule } from '@angular/forms';
import { ChatService } from './services/chat.service';



@NgModule({
  declarations: [ChatWindowComponent],
  imports: [
    CommonModule,
    ChatWindowRoutingModule,
    ReactiveFormsModule
  ],
  providers: [
    ChatService
  ]
})
export class ChatWindowModule { }
