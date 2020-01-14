import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MainWindowRoutingModule } from './main-window-routing.module';
import { MainWindowComponent } from './main-window.component';
import { HeaderComponent } from './components/header/header.component';


@NgModule({
  declarations: [MainWindowComponent, HeaderComponent],
  imports: [
    CommonModule,
    MainWindowRoutingModule
  ]
})
export class MainWindowModule { }
