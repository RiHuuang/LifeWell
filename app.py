import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from config import Config
import re

app = Flask(__name__)
app.config.from_object(Config)
this_config = Config()

app.secret_key= 'kelazz'

def interpretBMI(bmi):
    if(bmi < 18.5):
        return "UNDERWEIGHT"
    elif(bmi < 25):
        return "HEALTHY"
    elif(bmi < 30):
        return "OVERWEIGHT"
    else:
        return "OBESE"

    

def calculate_bmi(height, weight):
    
    try:
        height_cm = float(height)
        weight_kg = float(weight)

        if height_cm <= 0 or weight_kg <= 0:
            return "Invalid input. Height and weight must be positive numbers."

        bmi = weight_kg / ((height_cm / 100) ** 2)
        return str(bmi)
    except ValueError:
        return "Invalid input. Height and weight must be numeric values."


def calculate_bmr(gender,weight, height, age):
    try:
        weight = float(weight)
        height = float(height)
        age = float(age)

        if gender == "male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == "female":
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            raise ValueError("Gender must be 'male' or 'female'")

        return bmr
    except ValueError:
        raise ValueError("Weight, height, and age must be numeric values")


def calculate_daily_calories(bmr, activity_level):
    activity_factors = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "active" : 1.65 ,
        "very_active": 1.725,
        "super_active": 1.9
    }

    if activity_level in activity_factors:
        daily_calories = bmr * activity_factors[activity_level]
        return daily_calories
    else:
        raise ValueError("Invalid activity level")



def get_meal_plan(timeFrame, targetCalories, diet, exclude):
    params = {
        'apiKey': this_config.API_KEY,
        'timeFrame': timeFrame,
        'targetCalories': targetCalories,
        'diet': diet,
        'exclude': exclude
    }
    # print("API KEY IS -> ",this_config.API_KEY)
    BASE_URL = this_config.URL_GENERATE_MEAL_PLAN
    response = requests.get(BASE_URL, params=params).json()

    return response

def meal_query(query):
    BASE_URL = this_config.URL_NPL_NINCAL
    response = requests.get(
        BASE_URL + query, headers={'X-Api-Key': this_config.X_API_KEY})

@app.route("/")
def main_routes():
    # referrer = request.headers.get('Referer')
    # if referrer:
    #     return redirect(url_for('loading'))
    return render_template('home.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route("/profile")
def profile():
    # return render_template('profile.html')
    pass


@app.route('/calculate', methods=['POST','GET'])
def calculate():
    print("Requests method",request.method)

    if request.method == 'POST':
        print('jalan')
        gender = "male"
        age = 19
        height = request.form.get('input_tinggi')
        weight = request.form.get('input_berat')
        activity = request.form.get('activity')

        print("ini request form ", height, weight, activity)

        bmi = float("{:.2f}".format(float(calculate_bmi(height, weight))))
        desc = interpretBMI(bmi)

        bmr = calculate_bmr(gender, weight, height, age)
        session['bmr'] = bmr
        session['activity'] = activity
        
        print("bmi desc bmr",bmi,desc,bmr)
        check = True
        if height == '' or not height:
            check = False

        if check == False :
            redirect(url_for('calculate'))

        return render_template('calculate.html', bmi=bmi, desc=desc, activity=activity)

    return render_template('calculate.html', bmi = 0, desc = 'N/A')


@app.route('/daily_meals', methods=['POST', 'GET'])
def daily_meals():
    bmr = session.get('bmr', None)
    activity = session.get('activity', None)

    if bmr is None or activity is None:
        flash("BMR or Activity not found in session", 'danger')
        return redirect(url_for('calculate'))
    
    calories = float("{:.2f}".format(float(calculate_daily_calories(bmr, activity))))

    formatted_calories = {
        "maintain": "{:.2f}".format(calories),
        "mildWeightLoss": "{:.2f}".format(calories * 0.9),
        "weightLoss": "{:.2f}".format(calories * 0.85),
        "extremeLoss": "{:.2f}".format(calories * 0.75),
        "mildWeightGain": "{:.2f}".format(calories * 1.1),
        "weightGain": "{:.2f}".format(calories * 1.3),
        "fastWeightGain": "{:.2f}".format(calories * 1.5)
    }
    options = [
        {"value": "maintain", "text": "Maintain Weight"},
        {"value": "mildWeightLoss", "text": "Mild Weight Loss"},
        {"value": "weightLoss", "text": "Weight Loss"},
        {"value": "extremeLoss", "text": "Extreme Weight Loss"},
        {"value": "mildWeightGain", "text": "Mild Weight Gain"},
        {"value": "weightGain", "text": "Weight Gain"},
        {"value": "fastWeightGain", "text": "Fast Weight Gain"}
    ]


    if request.method == 'POST':
        print('jalan')
        timeFrame = request.form.getlist('timeFrame')
        targetCalories = request.form.getlist('targetCalories')
        diet = request.form.getlist('diet')
        exclude = request.form.getlist('exclude')

        print("ini BMR ", bmr)
        print("ini Activity", activity)
        print(calories)
        print("data di daily meals ---->>>",
              timeFrame, targetCalories, diet, exclude)

        check = True
        if timeFrame == '' or not timeFrame:
            flash("Time frame couldn't be empty!", 'danger')
            check = False

        if targetCalories == '' or not targetCalories:
            flash("Target calories couldn't be empty", 'danger')
            check = False

        if not check:
            return redirect(url_for('daily_meals'))

        # datas = get_meal_plan(timeFrame, targetCalories, diet, exclude)
        return redirect(url_for('get_meal', timeFrame=timeFrame, targetCalories=targetCalories, diet=diet, exclude=exclude))

    return render_template('daily_meals.html', formatted_calories=formatted_calories, options=options)


@app.route("/get_meal", methods=['POST', 'GET'])
def get_meal():
    print("Masuk ke getmeal")
    timeFrame = request.args.getlist('timeFrame')
    targetCalories = request.args.getlist('targetCalories')
    diet = request.args.getlist('diet')
    exclude = request.args.getlist('exclude')

    datas = get_meal_plan(
        timeFrame=timeFrame, targetCalories=targetCalories, diet=diet, exclude=exclude)
    # print(datas)

    return render_template('get_meal_plan.html', datas=datas)

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/workout')
def workout():
    return render_template('muscle.html')
# punya ipenk
api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/cardio"  # Ganti dengan URL API yang sesuai

headers = {
	"X-RapidAPI-Key": "685949c1d7mshf77a8318efe0eb6p1fc458jsn4229e07c81e8",
	"X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
}
response = requests.get(api_url,headers=headers)

if response.status_code == 200:
    all_data = response.json()
    data = [exercise for exercise in all_data if exercise.get("equipment") == "body weight"][:8]
else:
    data = []  # Data kosong jika terjadi kesalahan

@app.route('/womoves')
def womoves():
    return render_template('womoves.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, port=8800)



'''
nano ..\..\..\webEnv\Scripts\activate.bat
ctrl + x lalu y untuk save.
deactivate
lalu 
..\..\..\webEnv\Scripts\activate
'''
