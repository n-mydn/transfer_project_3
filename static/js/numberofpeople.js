const value1Select = document.getElementById("id_adultnumber");
const value2Select = document.getElementById("id_childrennumber");
const resultElement = document.getElementById("result");

value1Select.addEventListener("change", updateTotal);
value2Select.addEventListener("change", updateTotal);

function updateTotal() {
    const value1 = parseInt(value1Select.value);
    const value2 = parseInt(value2Select.value);
    const total = value1 + value2 ;
    resultElement.textContent = total;
}

