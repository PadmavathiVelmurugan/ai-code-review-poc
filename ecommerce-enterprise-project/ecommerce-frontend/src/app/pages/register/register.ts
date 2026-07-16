import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class Register {

  user = {
    name: '',
    email: '',
    password: '',
    role: 'USER'
  };

  constructor(private auth: AuthService) {}

  register() {
    this.auth.register(this.user).subscribe({
      next: () => {
        alert('Registration Successful');
      },
      error: (err) => {
        console.error(err);
        alert('Registration Failed');
      }
    });
  }
}