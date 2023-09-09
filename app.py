import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from config import Config
import re

app = Flask(__name__)
app.config.from_object(Config)
this_config = Config()

app.secret_key= 'kelazz'


def get_meal_plan(timeFrame, targetCalories, diet, exclude):
    params = {
        'apiKey': this_config.API_KEY,
        'timeFrame': timeFrame,
        'targetCalories': targetCalories,
        'diet': diet,
        'exclude': exclude
    }
    BASE_URL = this_config.URL_GENERATE_MEAL_PLAN
    response = requests.get(BASE_URL, params=params).json()

    return response

@app.route("/")
def main_routes():
    return render_template('home.html')

@app.route("/profile")
def profile():
    # return render_template('profile.html')
    pass


@app.route('/calculate')
def calculate():
    return render_template('calculate.html')


@app.route('/daily_meals', methods=['POST', 'GET'])
def daily_meals():

    if request.method == 'POST':
        print('jalan')
        timeFrame = request.form.get('timeFrame')
        targetCalories = request.form.get('targetCalories')
        diet = request.form.get('diet')
        exclude = request.form.get('exclude')
        # kalo multiple exclude pake (',')
        # list(map(str, userPreference.allergies.data.split(',')))

        timeFrame = request.args.getlist('timeFrame')
        targetCalories = request.args.getlist('targetCalories')
        diet = request.args.getlist('diet')
        exclude = request.args.getlist('exclude')
        datas = get_meal_plan(timeFrame,targetCalories,diet, exclude)
        print(timeFrame,targetCalories,diet,exclude)

        check = True
        if timeFrame == '' or not timeFrame:
            flash("Time frame couldn't be empty!", 'danger')
            check = False

        if targetCalories == '' or not targetCalories:
            flash("Target calories couldn't be empty", 'danger')
            check = False

        if not check:
            return redirect(url_for('daily_meals'))

        return redirect(url_for('get_meal', timeFrame=timeFrame, targetCalories=targetCalories, diet=diet, exclude=exclude))
    
    return render_template('daily_meals.html')

@app.route("/get_meal", methods=['POST', 'GET'])
def get_meal(timeFrame, targetCalories, diet, exclude):
    datas = get_meal_plan(
        timeFrame=timeFrame, targetCalories=targetCalories, diet=diet, exclude=exclude)
    return render_template('get_meal_plan.html', datas=datas)

@app.route('/summary')
def summary():
    return render_template('summary.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
