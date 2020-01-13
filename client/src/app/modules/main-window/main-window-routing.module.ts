import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { MainWindowComponent } from './main-window.component';

const routes: Routes = [{ path: '', component: MainWindowComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainWindowRoutingModule { }
