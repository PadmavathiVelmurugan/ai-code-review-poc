import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {

  email = '';
  password = '';

  constructor(
    private auth: AuthService,
    private router: Router
  ) {}

  login() {

    this.auth.login({
      email: this.email,
      password: this.password
    }).subscribe({

      next: (response: any) => {

        console.log('Backend Response:', response);

        if (response === 'Login Success') {

          localStorage.setItem(
            'token',
            'dummy-token'
          );

          this.router.navigate([
            '/products'
          ]);

        } else {

          alert('Invalid Credentials');

        }

      },

      error: (error) => {

        console.error(error);

        alert('Login Failed');

      }

    });

  }

}