import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../user.service';
import { FormBuilder, Validators } from '@angular/forms';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
    loginForm = this.fb.group({
        email: ['', [Validators.required, Validators.email]],
        password: ['', Validators.required]
      })

    constructor(    
        private fb: FormBuilder,
        private authService: UserService,
        private router: Router,
        private msgService: MessageService
    ) { }

    get email() {
        return this.loginForm.controls['email'];
    }
    
    get password() { 
        return this.loginForm.controls['password']; 
    }
    
    loginUser() {
        const { email, password } = this.loginForm.value;

        this.authService.getUserByEmail(email as string).subscribe(
            response => {
                if (response.length > 0 && response[0].password === password) {
                    sessionStorage.setItem('email', email as string);
                    this.router.navigate(['']);
                } else {
                    this.msgService.add({ severity: 'error', summary: 'Error', detail: 'email or password is wrong' });
                }
            },
            error => {
                this.msgService.add({ severity: 'error', summary: 'Error', detail: 'Something went wrong' });
            }
        )
    }
}
