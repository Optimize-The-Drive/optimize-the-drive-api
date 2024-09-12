import { Routes } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { MainComponent } from './main/main.component';

export const routes: Routes = [
    { path: 'login', component: LoginComponent, title: 'Optimize The Drive' },
    { path: '', component: MainComponent, title: 'Optimize The Drive' },
    { path: '**', redirectTo: '/', title: 'Optimize The Drive' }
];
