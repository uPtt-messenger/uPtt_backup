import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { MainWindowComponent } from './main-window.component';
import { NewChatComponent } from './pages/new-chat/new-chat.component';

const routes: Routes = [
  {
    path: '',
    component: MainWindowComponent,
    children: [
      {
        path: 'new-chat',
        component: NewChatComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainWindowRoutingModule { }
