const select2 = document.getElementById("id_select2");
const select3 = document.getElementById("id_select3");
const select4 = document.getElementById("id_select4");
const select5 = document.getElementById("id_select5");
const resultCarsElement = document.getElementById("resultcars");

const resultElement = document.getElementById("resultextras");
const resultTopElement = document.getElementById("resulttop");

select2.addEventListener("change", updateTotal);
select3.addEventListener("change", updateTotal);
select4.addEventListener("change", updateTotal);
select5.addEventListener("change", updateTotal);

const carPrice = parseFloat(resultCarsElement.getAttribute("value"));

function updateTotal() {
    const value2 = parseInt(select2.value);
    const value3 = parseInt(select3.value);
    const value4 = parseInt(select4.value);
    const value5 = parseInt(select5.value);

    const total = value2 + value3 + value4 + value5;
    const toplam = total  + carPrice ;

    resultTopElement.textContent = toplam.toFixed(2) + " ₺"; 
    resultElement.textContent = total + " ₺";

}