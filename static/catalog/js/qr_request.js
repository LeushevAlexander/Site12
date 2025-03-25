async function survey_site(intId) {
    let order_id = document.getElementById("order_id");
    let order_number = document.getElementById("order_number");
    let order_sum = document.getElementById("order_sum");

    //let url = "/qrgetstatus/" + order_id.innerText + "/" + order_number.innerText+ "/";
    let url = "/qrgetstatus/" + order_id.innerText + "/" + order_number.innerText+ "/" + order_sum.innerText+ "/";
    console.log(url);

    let response = await fetch(url, {referrerPolicy: "origin"});

    if(response.ok) {
        
        
        let resp_json = await response.json();

        if (resp_json.order_state == 'PAID')
        {
            var parent = document.getElementById("Quest"); 
            var child = document.getElementById("Pic"); 

            parent.removeChild(child);

            let paystatus = document.createElement("div");
            paystatus.innerHTML = `
            <p></p>
            <p></p>
            <p></p>
            <div style="text-align: center; 
			            color: rgb(255, 37, 226);
        			    font-size: 26px; 
			            font-weight: bold;">Заказ оплачен !!!
            </div>
            `;
            document.body.append(paystatus);
            clearInterval(intId);       
        }

        // let resp_json = await response.text();

        // let table = document.getElementById("myTable");
        // let t_body = document.getElementById("myTableBody");

        // let tr_element = document.createElement("tr");

        // let td_cell_one = document.createElement("td");
        // let now = new Date();
        // td_cell_one.innerHTML = now;

        // let td_cell_two = document.createElement("td");
        // td_cell_two.innerHTML = resp_json;

        // tr_element.appendChild(td_cell_one);
        // tr_element.appendChild(td_cell_two);

        // t_body.appendChild(tr_element);
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

window.onload = function() {
    let intId = setInterval(() => {survey_site(intId);}, 3000);
}
