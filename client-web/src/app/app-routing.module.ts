import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


const routes: Routes = [
  { path: '', redirectTo: 'public', pathMatch: 'full' },
  { path: 'public', loadChildren: () => import('./modules/public/public.module').then(m => m.PublicModule) },
  { path: 'main-window', loadChildren: () => import('./modules/main-window/main-window.module').then(m => m.MainWindowModule) },
  { path: 'chat-window', loadChildren: () => import('./modules/chat-window/chat-window.module').then(m => m.ChatWindowModule) }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
