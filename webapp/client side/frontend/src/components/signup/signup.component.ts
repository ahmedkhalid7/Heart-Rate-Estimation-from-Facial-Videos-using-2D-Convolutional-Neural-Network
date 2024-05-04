import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { UserService } from '../../user.service';
import { passwordMatchValidator } from '../password-match.directive';
import { MessageService } from 'primeng/api';
import { User } from '../../user';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {
  registerForm = this.fb.group({
    fullName: ['', [Validators.required, Validators.pattern(/^[a-zA-Z]+(?: [a-zA-Z]+)*$/)]],
    sex: ['', Validators.required], // Added sex control
    age: ['', [Validators.required, Validators.min(1)]], // Added age control with minimum age validation
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required],
    confirmPassword: ['', Validators.required]
  }, {
    validators: passwordMatchValidator
  })

  constructor(
    private fb: FormBuilder,
    private authService: UserService,
    private messageService: MessageService,
    private router: Router,
  ) { }

  get fullName() {
    return this.registerForm.controls['fullName'] as FormControl;
  }

  get sex() {
    return this.registerForm.controls['sex'] as FormControl;
  }

  get age() {
    return this.registerForm.get('age') as FormControl;
  }

  get email() {
    return this.registerForm.controls['email'] as FormControl;
  }

  get password() {
    return this.registerForm.controls['password'] as FormControl;
  }

  get confirmPassword() {
    return this.registerForm.controls['confirmPassword'] as FormControl;
  }

  submitDetails() {
    if (this.registerForm.valid) {
      const user: User = {
        fullName: this.fullName.value,
        sex: this.sex.value,
        age: Number(this.age.value), 
        email: this.email.value,
        password: this.password.value
      };
      console.log(user);
      this.authService.registerUser(user as User).subscribe(
        response => {
          console.log(response);
          this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Register successfully' });
          this.router.navigate(['login'])
        },
        error => {
          this.messageService.add({ severity: 'error', summary: 'Error', detail: 'Something went wrong' });
        }
      )
    }
  }
}