import { isDevMode } from '@angular/core';
import { HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable()
/**
 * Intercepts the API request, adding the base url to the application.
 */
export class AuthInterceptor implements HttpInterceptor {


    intercept(req: HttpRequest<any>, next: HttpHandler) {
        // Get the auth token from the service.
        // const authToken = this.auth.getAuthorizationToken();

        // // Clone the request and replace the original headers with
        // // cloned headers, updated with the authorization.
        // const authReq = req.clone({
        //     headers: req.headers.set('Authorization', authToken)
        // });

        // // send cloned request with header to the next handler.
        // return next.handle(authReq);
        return next.handle(req);
    }
}