const bmiText = document.getElementById('bmi');
const descText = document.getElementById('desc');
const weightInput = document.getElementById('weight');
const heightInput = document.getElementById('height');

form.addEventListener('submit', onFormSubmit);
form.addEventListener('reset', onFormReset);

weightInput.addEventListener('focus', function () {
    if (this.value == '0') {
        this.value = '';
    }
});

heightInput.addEventListener('focus', function () {
    if (this.value == '0') {
        this.value = '';
    }
});

function onFormReset() {
    bmiText.textContent = 0;
    bmiText.className = "";
    descText.textContent = "N/A";
}