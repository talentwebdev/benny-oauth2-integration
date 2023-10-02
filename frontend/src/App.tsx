import React, { useEffect, useState } from 'react';
import './App.css';
import { FacebookOauth2Service, IUserInfo } from "./services/facebook-oauth2.service";

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [userInfo, setUserInfo] = useState<IUserInfo | null>(null);
    const [isLoginError, setIsLoginError] = useState<boolean>(false);

    const onLogin = async (): Promise<void> => {
        try {
            const userInfo: IUserInfo = await FacebookOauth2Service.openLoginUrl();
            setUserInfo(userInfo);
            setIsLoginError(false);
            setIsLoggedIn(true);
        } catch(e) {
            setIsLoginError(true);
            setIsLoggedIn(false);
        }
    }

    useEffect(() => {
        FacebookOauth2Service.checkSocialOAuth2Callback();
    }, []);

    return (
        <div>
            {!isLoggedIn && <button data-test-id={'login-btn'} onClick={onLogin}>Login</button>}
            {isLoggedIn && userInfo && <div>UserName: {userInfo.name}</div>}
            {isLoginError && <span style={{color: 'red'}}>Login failed</span>}
        </div>
    );
}

export default App;
