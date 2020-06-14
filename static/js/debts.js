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
        success: function (data) {
            console.log('expand');
            let debts_list = document.getElementById("debt_user:" + to_user_id).getElementsByClassName("accordion-item-content")[0];
            debts_list.innerHTML = "";
            console.log('debts_list', debts_list);
            let debts = data.debts;
            /*
            <div class="shortcut-row-header w-row">
              <div class='w-col w-col-4 w-col-small-4 w-col-tiny-4'><div class='text-block-107'>Табачок</div></div><div class='w-col w-col-4 w-col-small-4 w-col-tiny-4'><div class='text-block-107'>+150</div></div><div class='w-col w-col-4 w-col-small-4 w-col-tiny-4'><div class='text-block-107'>2020-06-12</div></div>
            </div>
             */
            for (let i = 0; i < data.debts.length; i++){
                let debt_text = debts[i].text;
                let debt_date = get_django_date(debts[i].created_at);
                let debt_price = debts[i].price;
                let debt_div = document.createElement("div");
                debt_div.setAttribute("class", "shortcut-row-header w-row");
                let sign = "-";
                if (debts[i].is_positive){
                    sign = "+";
                }
                debt_div.innerHTML = "<div class='w-col w-col-4 w-col-small-4 w-col-tiny-4'><div class='text-block-107'>" + debt_text + "</div></div><div class='w-col w-col-4 w-col-small-4 w-col-tiny-4'><div class='text-block-107'>" + sign + debt_price + "</div></div><div class='w-col w-col-4 w-col-small-4 w-col-tiny-4'><div class='text-block-107'>" + debt_date.toISOString().split('T')[0] + "</div></div>"
                // debt_div.innerHTML = "<div class='row'><div class='col-sm'>" + debt_text + "</div>" + "<div class='col-sm'>" + sign + debt_price + "</div>" + "<div class='col-sm'>" + debt_date.toISOString().split('T')[0] + "</div></div>";
                debts_list.appendChild(debt_div);
            }
            element.setAttribute("onclick", "hide_debts(this, " + to_user_id + ")");
            // element.setAttribute("class", "list-group-item list-group-item-action active")
        }
    })
}

function hide_debts(element, to_user_id) {
    let debts_list = document.getElementById("debt_user:" + to_user_id).getElementsByClassName("accordion-item-content")[0];
    debts_list.innerHTML = "";
    // debts_list.style.border = "none";

    element.setAttribute("onclick", "expand_debts(this, " + to_user_id + ")");
    // element.setAttribute("class", "list-group-item list-group-item-action");
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
    let is_common_debt = document.getElementById("is_common_debt").checked;
    console.log('is_common_debt', is_common_debt);
    $.ajax({
        url: "/api/debts/add",
        type: "post",
        headers: {"Authorization": "Token " + token},
        data: {text: text, price: price, to_user: to_user, is_common_debt: is_common_debt},
        success: function (data) {
            window.location.reload();
        }
    })
}

function handle_is_common_debt_checkbox_click() {
    let checkbox = document.getElementById("is_common_debt");
    let to_user = document.getElementById("to_user_input");
    to_user.disabled = checkbox.checked;
}