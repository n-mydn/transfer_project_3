const selectElements = document.querySelectorAll(".s-select");
const resultElement = document.querySelector(".resultsecilen");

selectElements.forEach(select => {
    select.addEventListener("change", function () {
        const selectedValues = Array.from(selectElements).map(select => select.value);
        resultElement.textContent = "Seçilen Değerler: " + selectedValues.join(", ");
    });
});