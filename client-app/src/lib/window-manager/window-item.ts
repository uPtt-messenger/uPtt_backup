export class WindowItem {
    public name: string;
    public url: {
        pathname: string;
        hash?: string;
    };
    public window: any;
    public options: {
        width: number;
        height: number;
        title: string;
        icon: string;
        webPreferences: {
            nodeIntegration: boolean;
        }
    };
}
