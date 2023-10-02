import React from 'react';
import { render } from '@testing-library/react';
import App from './App';
import { FacebookOauth2Service } from "./services/facebook-oauth2.service";

describe('App', () => {

  test('render login button correctly', () => {
    render(<App />);
    const loginBtn: HTMLButtonElement = document.querySelector('[data-test-id="login-btn"]');
    expect(loginBtn).toBeTruthy();
  });

  test('open oauth2 login tab when click login button', () => {
    render(<App />);
    const openLoginUrlSpy: jest.SpyInstance = jest.spyOn((FacebookOauth2Service as any), 'openLoginUrl');

    const loginBtn: HTMLButtonElement = document.querySelector('[data-test-id="login-btn"]');
    loginBtn.click();

    expect(openLoginUrlSpy).toHaveBeenCalled();
  });
});
