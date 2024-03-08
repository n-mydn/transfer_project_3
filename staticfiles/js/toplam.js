const value1Select = document.getElementById("resultcars");
const value2Select = document.getElementById("resultextras");

const resultElement = document.getElementById("resulttop");

value2Select.addEventListener("change", updateTotal);

function updateTotal() {
    const value1 = parseInt(value1Select.value);
    const value2 = parseInt(value2Select.value);
    const total = value1 + value2 ;
    resultElement.textContent = total;
}

