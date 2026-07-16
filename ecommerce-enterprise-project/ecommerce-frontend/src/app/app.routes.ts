import { Routes } from '@angular/router';

import { Login } from './pages/login/login';
import { Register } from './pages/register/register';
import { Products } from './pages/products/products';
import { Cart } from './pages/cart/cart';

export const routes: Routes = [

  {
    path:'login',
    component:Login
  },

  {
    path:'register',
    component:Register
  },

  {
    path:'products',
    component:Products
  },

  {
    path:'',
    redirectTo:'login',
    pathMatch:'full'
  },

{
  path:'cart',
  component:Cart
}

];