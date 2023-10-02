import { RestBuilder } from "./rest-builder.service";

export interface IUserInfo {
    first_name: string;
    last_name: string;
    name: string;
    id: string;
}

export class FacebookOauth2Service {
    public static async openLoginUrl(): Promise<IUserInfo> {
        return new Promise<IUserInfo>((resolve, reject): void => {
            const apiUrl: string = RestBuilder.create().social('facebook').authUrl().apiUrl;

            fetch(apiUrl).then(async (response: Response): Promise<void> => {
                const url: string = await response.json();

                (window.location as any).onFacebookCallback = async (token: string): Promise<void> => {
                    try {
                        const userInfo: IUserInfo = await FacebookOauth2Service.getUserInfo(token);
                        resolve(userInfo);
                    } catch (e) {
                        reject(e);
                    }
                };
                window.open(url, "_blank");
            });
        });
    }

    public static async getUserInfo(code: string): Promise<IUserInfo> {
        const apiUrl: string = RestBuilder.create().social('facebook').auth().apiUrl;
        const response: Response = await fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify({
                code,
            }),
            headers: { 'Content-Type': 'application/json'}}
        );

        if (response.status !== 200) {
            throw Error;
        }

        return await response.json();
    }

    public static checkSocialOAuth2Callback(): void {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get("code");

        if (window.opener?.location && code) {
            window.opener?.location.onFacebookCallback && window.opener.location.onFacebookCallback(code);
            window.close();
        }
    }
}
