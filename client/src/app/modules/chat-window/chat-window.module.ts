import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatWindowComponent } from './pages/chat-window/chat-window.component';
import { ChatWindowRoutingModule } from './chat-window-routing.module';
import { ReactiveFormsModule } from '@angular/forms';



@NgModule({
  declarations: [ChatWindowComponent],
  imports: [
    CommonModule,
    ChatWindowRoutingModule,
    ReactiveFormsModule
  ]
})
export class ChatWindowModule { }
