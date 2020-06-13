let token = null;
let user = null;

window.onload = function () {
    user = localStorage.getItem("user");
    token = localStorage.getItem("token");
};

function expand_debts(element, to_user_id) {
    $.ajax({
        url: "/api/debts/list/" + to_user_id,
        type: "post",
        headers: {"Authorization": "Token " + token},
        beforeSend: function(){
          let divs = document.getElementsByClassName("debts_list");
          let users = document.getElementsByClassName("users_list")[0].getElementsByTagName("a");
          for (let i = 0; i < users.length; i++){
              users[i].setAttribute("class", "list-group-item list-group-item-action");
              let to_user = users[i].parentNode.id.split(':')[1];
              users[i].setAttribute("onclick", "expand_debts(this, " + to_user + ")");
              hide_debts(users[i], to_user);
          }
        },
        success: function (data) {
            let debts_list = document.getElementById("debt_user:" + to_user_id).getElementsByClassName("debts_list")[0];
            debts_list.innerHTML = "";
            let debts = data.debts;
            for (let i = 0; i < data.debts.length; i++){
                let debt_text = debts[i].text;
                let debt_date = get_django_date(debts[i].created_at);
                let debt_price = debts[i].price;
                let debt_div = document.createElement("div");
                debt_div.setAttribute("class", "container");
                let sign = "-";
                if (debts[i].is_positive){
                    sign = "+";
                }
                debt_div.innerHTML = "<div class='row'><div class='col-sm'>" + debt_text + "</div>" + "<div class='col-sm'>" + sign + debt_price + "</div>" + "<div class='col-sm'>" + debt_date.toISOString().split('T')[0] + "</div></div>";
                debts_list.appendChild(debt_div);
            }
            debts_list.style.border = "1px solid #007bff";
            debts_list.style.borderRadius = "0.25rem";
            element.setAttribute("onclick", "hide_debts(this, " + to_user_id + ")");
            element.setAttribute("class", "list-group-item list-group-item-action active")
        }
    })
}

function hide_debts(element, to_user_id) {
    let debts_list = document.getElementById("debt_user:" + to_user_id).getElementsByClassName("debts_list")[0];
    debts_list.innerHTML = "";
    debts_list.style.border = "none";

    element.setAttribute("onclick", "expand_debts(this, " + to_user_id + ")");
    element.setAttribute("class", "list-group-item list-group-item-action");
}

function show_add_form() {
    let form = document.getElementById("add_form");
    form.style.display = "block";
    let btn = document.getElementById("btn_add_form");
    btn.setAttribute("onclick", "hide_add_form()");
}

function hide_add_form() {
    let form = document.getElementById("add_form");
    form.style.display = "none";
    let btn = document.getElementById("btn_add_form");
    btn.setAttribute("onclick", "show_add_form()");
}

function add_debt () {
    let text = document.getElementById("text_input").value;
    let price = document.getElementById("price_input").value;
    let to_user = document.getElementById("to_user_input").value;
    $.ajax({
        url: "/api/debts/add",
        type: "post",
        headers: {"Authorization": "Token " + token},
        data: {text: text, price: price, to_user: to_user},
        success: function (data) {
            window.location.reload();
        }
    })
}