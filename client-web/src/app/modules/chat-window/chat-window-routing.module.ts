import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ChatWindowComponent } from './pages/chat-window/chat-window.component';

const routes: Routes = [
  {
    path: ':pttId',
    component: ChatWindowComponent,
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ChatWindowRoutingModule { }
