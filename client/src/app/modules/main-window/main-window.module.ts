import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MainWindowRoutingModule } from './main-window-routing.module';
import { MainWindowComponent } from './main-window.component';
import { HeaderComponent } from './components/header/header.component';
import { NewChatComponent } from './pages/new-chat/new-chat.component';


@NgModule({
  declarations: [MainWindowComponent, HeaderComponent, NewChatComponent],
  imports: [
    CommonModule,
    MainWindowRoutingModule
  ]
})
export class MainWindowModule { }
