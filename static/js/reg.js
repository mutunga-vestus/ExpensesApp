const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid-feedback");

const emailField = document.querySelector("#emailField");
const emailfeedbackArea = document.querySelector('.emailfeedbackArea');
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");

const ShowPassword = document.querySelector(".ShowPassword");
const passwordField = document.querySelector("#passwordField")

const submitBtn = document.querySelector(".submit-btn")

const HandleToggleInput = (e) => {
    if (ShowPassword.textContent === 'SHOW'){

        passwordField.setAttribute('type', 'text');
        ShowPassword.textContent = 'HIDE';
    }else{
        passwordField.setAttribute('type', 'password');
        ShowPassword.textContent = 'SHOW'
    }
}

ShowPassword.addEventListener("click", HandleToggleInput)

emailField.addEventListener('keyup', (e) => {
    console.log('2221',2221);
    const emailVal= e.target.value;

    emailSuccessOutput.style.display = "block";

    emailSuccessOutput.textContent = `Checking ${emailVal}`;

    emailField.classList.remove('is-invalid');
    emailfeedbackArea.style.display = "none";

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({email: emailVal}),
            method:"POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            emailSuccessOutput.style.display = "none";

            if (data.email_error){
                submitBtn.disabled = true;
                emailField.classList.add('is-invalid');
                emailfeedbackArea.style.display = "block";
                emailfeedbackArea.innerHTML = `<p>${(data.email_error)}<p>`;
            }else{
                submitBtn.removeAttribute("disabled")
            }
        });
    }

});

usernameField.addEventListener('keyup', (e) => {
    console.log('2222',2222);
    const usernameVal= e.target.value;

    usernameSuccessOutput.style.display = "block";

    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display = "none";

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}),
            method:"POST",
        })
        .then((res) => res.json())
        .then((data) => {
            
            usernameSuccessOutput.style.display = "none";

            if (data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = "block";
                feedbackArea.innerHTML = `<p>${(data.username_error)}<p>`;
                submitBtn.disabled = true;
            }else{
                submitBtn.removeAttribute("disabled")
            }
        });
    }

});
