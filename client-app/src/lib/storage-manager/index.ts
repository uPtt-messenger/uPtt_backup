export class StorageManager {

    private user = new Map();

    constructor() {}

    public getUser(): any {
        return this.user;
    }

    public setUser(user: any): void {
        this.user = user;
    }

}
