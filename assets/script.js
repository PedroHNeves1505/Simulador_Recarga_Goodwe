const btnSignIn = document.getElementById('show_signin');
const btnSignUp = document.getElementById('show_signup');
const containerInputsSignIn = document.querySelector('.input_signin');
const containerInputsSignUp = document.querySelector('.input_signup');
const Title = document.getElementById('title');

btnSignIn.addEventListener('click', function() {
    containerInputsSignIn.classList.remove('hidden');
    containerInputsSignUp.classList.add('hidden');
    Title.textContent = 'Sign in';
});

btnSignUp.addEventListener('click', function() {
    containerInputsSignIn.classList.add('hidden');
    containerInputsSignUp.classList.remove('hidden');
    Title.textContent = 'Sign up';
});