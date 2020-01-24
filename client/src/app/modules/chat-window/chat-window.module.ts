import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatWindowComponent } from './pages/chat-window/chat-window.component';
import { ChatWindowRoutingModule } from './chat-window-routing.module';



@NgModule({
  declarations: [ChatWindowComponent],
  imports: [
    CommonModule,
    ChatWindowRoutingModule
  ]
})
export class ChatWindowModule { }
