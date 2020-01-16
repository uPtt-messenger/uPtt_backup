import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IpcService } from './services/ipc.service';

@NgModule({
  declarations: [],
  imports: [
    CommonModule
  ],
  providers: [
    IpcService
  ]
})
export class SharedModule { }
