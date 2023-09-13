import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from config import Config
import re

app = Flask(__name__)
app.config.from_object(Config)
this_config = Config()

app.secret_key= 'kelazz'


def calculate_bmr(gender,weight, height, age):
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "female":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    return bmr


def calculate_daily_calories(bmr, activity_level):
    activity_factors = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
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

@app.route("/profile")
def profile():
    # return render_template('profile.html')
    pass


@app.route('/calculate')
def calculate():
    return render_template('calculate.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/daily_meals', methods=['POST', 'GET'])
def daily_meals():

    if request.method == 'POST':
        print('jalan')
        timeFrame = request.form.getlist('timeFrame')
        targetCalories = request.form.getlist('targetCalories')
        diet = request.form.getlist('diet')
        exclude = request.form.getlist('exclude')
        print("ini request form ", timeFrame, targetCalories, diet, exclude)

        check = True
        if timeFrame == '' or not timeFrame:
            flash("Time frame couldn't be empty!", 'danger')
            check = False

        if targetCalories == '' or not targetCalories:
            flash("Target calories couldn't be empty", 'danger')
            check = False

        if not check:
            return redirect(url_for('daily_meals'))

        # datas = get_meal_plan(timeFrame,targetCalories,diet, exclude)
        return redirect(url_for('get_meal', timeFrame=timeFrame, targetCalories=targetCalories, diet=diet, exclude=exclude))
    
    return render_template('daily_meals.html')

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

@app.route('/temp')
def temp():
    page = url_for('main_routes')
    return f'<a href="{page}">AAAA</a>'

@app.route('/workout')
def workout():
    return render_template('muscle.html')

@app.route('/womoves')
def womoves():
    return render_template('womoves.html')


if __name__ == '__main__':
    app.run(debug=True, port=8800)



'''
nano ..\..\..\webEnv\Scripts\activate.bat
ctrl + x lalu y untuk save.
deactivate
lalu 
..\..\..\webEnv\Scripts\activate
'''
