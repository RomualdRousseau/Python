import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import * as auth0 from 'auth0-js';

// check this: https://github.com/aws/aws-amplify/issues/678#issuecomment-389106098
(window as any).global = window;

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    auth0 = new auth0.WebAuth({
        clientID: 'jhndeVKASVxksZZiLzHoLKGr3zGzXsew',
        domain: 'dev-8m6tfj-3.us.auth0.com',
        responseType: 'token',
        redirectUri: 'http://localhost:4200/',
        scope: 'openid email'
    });

    accessToken: String | null;
    expiresAt: Number | null;

    constructor(public router: Router) {}

    public handleAuthentication(): void {
        this.auth0.parseHash((err, authResult) => {
            if (authResult && authResult.accessToken) {

                this.auth0.client.userInfo(authResult.accessToken, function(err: any, user: any) {
                    console.log(user);
                });

                window.location.hash = '';
                this.accessToken = authResult.accessToken;
                this.expiresAt = ((authResult.expiresIn||0) * 1000) + new Date().getTime();
            } else {
                this.login();
            }
        });
    }

    public login(): void {
        this.auth0.authorize();
    }

    public logout(): void {
        this.accessToken = null;
        this.expiresAt = null;
        this.auth0.logout({
            clientID: 'jhndeVKASVxksZZiLzHoLKGr3zGzXsew'
        });
    }

    public isAuthenticated(): boolean {
        return new Date().getTime() < (this.expiresAt||0);
    }
}
