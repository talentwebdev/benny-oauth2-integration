export class RestBuilder {
    private _apiUrl: string;

    constructor() {
        this._apiUrl = '/api/';
    }

    public static create(): RestBuilder {
        const rest = new RestBuilder();
        return rest;
    }

    public social(provider: string): RestBuilder {
        this._apiUrl += `social/${provider}/`
        return this;
    }

    public authUrl(): RestBuilder {
        this._apiUrl += `auth_url/`
        return this;
    }

    public auth(): RestBuilder {
        this._apiUrl += `auth/`
        return this;
    }

    public get apiUrl(): string {
        return this._apiUrl;
    }
}
