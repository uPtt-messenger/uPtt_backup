import { LogManager } from '../log-manager';
import { LoginSubject } from '../login-subject';
import { Tray, Menu, app } from 'electron';

export class TrayManager {

  private TRAY_ICO = 'resource/assets/images/uptt.ico';
  private tray: Tray;

  constructor(
    private logger: LogManager,
    private loginSubject: LoginSubject) { }

  public initTray(): void {
    this.logger.debug('init tray');
    // 建立 System Tray
    this.tray = new Tray(this.TRAY_ICO);
    const contextMenu = Menu.buildFromTemplate([
      { label: '關於', type: 'normal' },
      {
        label: '結束',
        type: 'normal',
        click: () => {
          // app.isQuiting = true;
          this.logger.debug('tray trigger exit');
          app.quit();
        }
      },
    ]);
    this.tray.setToolTip('uPtt');
    this.tray.setContextMenu(contextMenu);

    this.loginSubject.isLogined.asObservable().subscribe(isLogined => {
      if (isLogined) {
        this.tray.setContextMenu(
          Menu.buildFromTemplate([
            { label: '丟水球', type: 'normal' },
            { label: '設定', type: 'normal' },
            { label: '關於', type: 'normal' },
            { label: '登出', type: 'normal' },
            {
              label: '結束',
              type: 'normal',
              click: () => {
                // app.isQuiting = true;
                this.logger.debug('tray trigger exit');
                app.quit();
              }
            },
          ])
        );
      }
    });
  }

}
