function toggleSenha() {
    const icon = document.getElementById('iconSenha'); 
    const input = document.getElementById('password');

    if (input.type === 'password') {
        input.type = 'text'; // mostra a senha
        icon.classList.remove('bi-eye'); // remove o olho aberto
        icon.classList.add('bi-eye-slash'); // adiciona olho fechado
    } else {
        input.type = 'password'; // esconde a senha
        icon.classList.remove('bi-eye-slash'); // remove olho fechado
        icon.classList.add('bi-eye'); // adiciona olho aberto
    }
}

function toggleSenha1(){
    const icon = document.getElementById('iconSenha1');
    const input = document.getElementById('password1');

    if (input.type === 'password'){
        input.type = 'text'
        icon.classList.remove('bi-eye'); // remove o olho aberto
        icon.classList.add('bi-eye-slash'); // adiciona olho fechado
    } else{
        input.type = 'password'; // esconde a senha
        icon.classList.remove('bi-eye-slash'); // remove olho fechado
        icon.classList.add('bi-eye'); // adiciona olho aberto
    }
}

function toggleSenha2(){
    const icon = document.getElementById('iconSenha2');
    const input = document.getElementById('password2');

    if (input.type === 'password'){
        input.type = 'text'
        icon.classList.remove('bi-eye'); // remove o olho aberto
        icon.classList.add('bi-eye-slash'); // adiciona olho fechado
    } else{
        input.type = 'password'; // esconde a senha
        icon.classList.remove('bi-eye-slash'); // remove olho fechado
        icon.classList.add('bi-eye'); // adiciona olho aberto
    }
}
