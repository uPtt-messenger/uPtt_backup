export class ConfigManager {

  private config = new Map();

  constructor() { }

  public init(): void {
    let dirPath = __dirname;
    dirPath = dirPath.substring(0, dirPath.indexOf('src'));
    this.add('dirPath', dirPath);
  }

  public get(configName: string): any {
    if (configName) {
      return this.config.get(configName);
    } else {
      return null;
    }
  }

  public add(configName: string, configValue: any): void {
    if (configName) {
      this.config.set(configName, configValue);
    }
  }

}
