const usernameField = document.querySelector("#usernameField")
const feedbackArea = document.querySelector(".invalid-feedback")
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput")

const emailField = document.querySelector("#emailField")
const emailfeedbackArea = document.querySelector(".emailfeedbackArea")

const showPassword = document.querySelector(".showPassword")

const passwordField = document.querySelector("#passwordField")

const submitBtn = document.querySelector(".submit-btn")

const HandleToggleInput = (e) => {
  if(showPassword.textContent === 'SHOW'){
    showPassword.textContent = 'HIDE';
    passwordField.setAttribute("type", "text");
  }else{
    showPassword.textContent = 'SHOW';
    passwordField.setAttribute("type", "password");
  }
}

showPassword.addEventListener('click', HandleToggleInput)

emailField.addEventListener('keyup', (e) => {
  console.log("77775",77775);

  const emailVal = e.target.value;

  if (emailVal.length > 0){
        fetch("/authentication/validate-email",{
        body: JSON.stringify({email: emailVal}),
        method: "POST"
      })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data)
        if(data.email_error) {
            submitBtn.disabled = true;
            emailField.classList.add("is-invalid");
            emailfeedbackArea.style.display = 'block';
            emailfeedbackArea.innerHTML = `<p>${data.email_error}</p>`

        }else {
          submitBtn.removeAttribute("disabled");
        }
      });


      }

emailField.classList.remove("is-invalid");
emailfeedbackArea.style.display = "none";

});

usernameField.addEventListener('keyup', (e) =>{

      console.log("77777",77777);
      const usernameVal = e.target.value;
      usernameSuccessOutput.textContent = `Checking ${usernameVal}`;
      usernameSuccessOutput.style.display ='block';

      usernameField.classList.remove("is-invalid");
      feedbackArea.style.display = "none";

      if (usernameVal.length > 0){
        fetch("/authentication/validate-username",{
        body: JSON.stringify({username: usernameVal}),
        method: "POST",
      })
      .then((res) => res.json())
      .then((data) =>{
        console.log("data", data)
        usernameSuccessOutput.style.display ='none'
        if(data.username_error) {
            usernameField.classList.add("is-invalid");
            feedbackArea.style.display = 'block';
            feedbackArea.innerHTML = `<p>${data.username_error}</p>`
            submitBtn.disabled = true;

        }else {
          submitBtn.removeAttribute("disabled");
        }
      });


      }


      

});