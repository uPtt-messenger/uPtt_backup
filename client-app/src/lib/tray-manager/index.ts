import { LogManager } from '../log-manager';
import { LoginSubject } from '../login-subject';
import { Tray, Menu, app, dialog } from 'electron';
import { WindowManager } from '../window-manager';

export class TrayManager {

  private TRAY_ICO = 'resource/assets/images/uptt.ico';
  private tray: Tray;

  constructor(
    private logger: LogManager,
    private loginSubject: LoginSubject,
    private windowManager: WindowManager) { }

  public initTray(): void {
    this.logger.debug('init tray');
    // 建立 System Tray
    this.tray = new Tray(this.TRAY_ICO);
    const contextMenu = Menu.buildFromTemplate([
      {
        label: '關於',
        type: 'normal',
        click: () => {
          dialog.showMessageBox({
            message: 'uptt client 1.0.0-alpha 版'
          });
        }
      },
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
            {
              label: '丟水球',
              type: 'normal',
              click: () => {
                this.windowManager.openNewChat();
              }
            },
            {
              label: '關於',
              type: 'normal',
              click: () => {
                dialog.showMessageBox({
                  message: 'uptt client 1.0.0-alpha 版'
                });
              }
            },
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
