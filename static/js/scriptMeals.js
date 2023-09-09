const form = document.querySelector('form');
const targetInput = document.getElementsByName("targetCalories");
const exclude = document.getElementById('allergy');

form.addEventListener('submit', onFormSubmit);
form.addEventListener('reset', onFormReset);

targetInput.addEventListener('focus', function(){
    if(this.value == '0'){
        this.value = '';
    }
});


function clearPlaceholder(element){
    element.placeholder = "";
}

function onFormSubmit(e){
    e.preventDefault();

    const allergy = document.getElementById('allergy').value;
    if(!isNaN(parseFloat(allergy))){
        alert("Please enter a valid allery (non numeric string)");
        return;
    }

    var inputCalories = document.getElementById("calories").value;
    if(inputCalories < 1200){
        alert("Calories must be >= 1200");
        return;
    }

    var rdb1 = document.getElementById("day");
    var rdb2 = document.getElementById("week");
        if(rdb1.checked == true){
            alert(rdb1.value)
        }else if(rdb2.checked == true){
            alert(rdb2.value)
        }else{
            alert("please select atleast one option");
        }

}

