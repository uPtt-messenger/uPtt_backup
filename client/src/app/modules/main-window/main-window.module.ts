import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MainWindowRoutingModule } from './main-window-routing.module';
import { MainWindowComponent } from './main-window.component';


@NgModule({
  declarations: [MainWindowComponent],
  imports: [
    CommonModule,
    MainWindowRoutingModule
  ]
})
export class MainWindowModule { }
