const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector('.invalid_feedback');
const usernameSuccess =document.querySelector('.usernameSuccess');
const emailField = document.querySelector('#emailField');
const passwordField =document.querySelector('#passwordField')
const emailFeedbackArea = document.querySelector('.invalid_email_feedback');
const showPasswordToggle =document.querySelector('.showPasswordToggle');
const btSubmit = document.querySelector('.btn-submit');



const handleToggleClickEvent =(e)=>{
    if(showPasswordToggle.textContent ==="SHOW"){
        showPasswordToggle.textContent ="HIDE";
        passwordField.setAttribute("type","text");
    }else{
        showPasswordToggle.textContent ="SHOW";
        passwordField.setAttribute("type","password");

    }
};
showPasswordToggle.addEventListener("click", handleToggleClickEvent);

emailField.addEventListener ('keyup', (e)=>{
    const userEmailVal =e.target.value;

    emailField.classList.remove("is-invalid")
    emailFeedbackArea.style.display ='none';

    if(userEmailVal.length > 0){
        fetch("/authentication/validate_email",{
            body:JSON.stringify({email:userEmailVal}),
            method:"POST",
        })
        .then((res)=> res.json())
        .then((data)=>{
            console.log("data:",data);

            if(data.email_error){
                emailField.classList.add("is-invalid")
                emailFeedbackArea.style.display ='block';
                emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                btSubmit.disabled = true;
            }else{
                btSubmit.removeAttribute("disabled");
            }

        });
    
    }
    


})

usernameField.addEventListener('keyup',(e)=>{

    const usernameVal =e.target.value;

    usernameSuccess.style.display = 'block';

    usernameSuccess.textContent = `Checking ${usernameVal}`

    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display ='none';

    if(usernameVal.length > 0){
        fetch("/authentication/validate_username",{
            body:JSON.stringify({username:usernameVal}),
            method:"POST",
        })
        .then((res)=> res.json())
        .then((data)=>{
            console.log("data:",data);
            usernameSuccess.style.display = 'none';


            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedbackArea.style.display ='block';
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                btSubmit.disabled =true;
            }
            else{
                btSubmit.removeAttribute("disabled");
            }

        });
    
    }
   
});