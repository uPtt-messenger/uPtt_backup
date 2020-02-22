import { Injectable } from '@angular/core';
import { ErrorContext } from '../models/error.context';
import { throwError } from 'rxjs';

@Injectable()
export class ErrorService {

  constructor( ) { }

  public handleError(errorContext: ErrorContext) {

    if (Array.isArray(errorContext)) {
      return throwError(errorContext);
    } else {
      if (errorContext.status !== undefined) {
        if (errorContext.status < 500) {
          return throwError(errorContext);
        } else {
          // TODO: router not work
          return throwError(errorContext);
        }
      } else {
        // TODO: router not work
        // timeout and server error
        return throwError(errorContext);
      }
    }
  }
}
