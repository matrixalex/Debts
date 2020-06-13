function login() {
    let email = document.getElementById("email_input").value;
    let password = document.getElementById("password_input").value;

    $.ajax({
        url: "/auth/login",
        type: "post",
        data: {email: email, password: password},
        success: function (data) {
            if (data.status) {
                console.log('logged');
                console.log(data);
                localStorage.setItem("token", data.token);
                localStorage.setItem("user", data.user);
                console.log(localStorage.getItem("token"));
                console.log(localStorage.getItem("user"));
                window.location.href = "/debts"
            } else {
                console.log('error');
                console.log(data);
                alert(data.message);
            }
        }
    })
}