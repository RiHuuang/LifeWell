const bmiText = document.getElementById('bmi');
const descText = document.getElementById('desc');
const form = document.querySelector('form');
const weightInput = document.getElementById('weight');
const heightInput = document.getElementById('height');

form.addEventListener('submit', onFormSubmit);
form.addEventListener('reset', onFormReset);

weightInput.addEventListener('focus', function(){
    if(this.value == '0'){
        this.value = '';
    }
});

heightInput.addEventListener('focus', function(){
    if(this.value == '0'){
        this.value = '';
    }
});

function onFormReset(){
    bmiText.textContent = 0;
    bmiText.className = "";
    descText.textContent = "N/A";
}

function onFormSubmit(e){
    e.preventDefault();

    const weight = parseFloat(form.weight.value);
    const height = parseFloat(form.height.value);

    if(isNaN(weight) || isNaN(height) || weight <= 0 || height <= 0){
        alert("Please enter a valid weight and height");
        return;
    }

    const heightInMeters = height/100;
    const bmi = weight/Math.pow(heightInMeters, 2);
    const desc = interpretBMI(bmi);

    bmiText.textContent = bmi.toFixed(2);
    // var desc = interpretBMI(bmi);
    bmiText.className = desc;
    descText.innerHTML = `You are <strong>${desc}</strong>`;
    }

    function interpretBMI(bmi){
        if(bmi < 18.5){
            return "UNDERWEIGHT";
        }else if(bmi < 25){
            return "HEALTHY";
        }else if(bmi < 30){
            return "OVERWEIGHT";
        }else{
            return "OBESE"
        }
    }
