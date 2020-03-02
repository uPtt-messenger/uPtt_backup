export class ErrorContext {
  constructor(errorCode: number, errorMessage: string) {
    this.errorCode = errorCode;
    this.errorMessage = errorMessage;
  }
  name: string;
  appId: string;
  user: string;
  time: number;
  url: string;
  status: number;
  errorCode: number;
  errorMessage: string;
  targetId: number;
  targetName: string;
}
