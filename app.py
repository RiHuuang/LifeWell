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

def get_meal_image(query):
    params = {
        'apiKey': this_config.API_KEY,
        'query': query,
    }
    # print("API KEY IS -> ",this_config.API_KEY)
    BASE_URL = this_config.URL_SEARCH_RECIPE
    response = requests.get(BASE_URL, params=params).json()
    print("INI RESPONSE DARI GET_MEAL_IMAGE",response,"\n\n")
    return response['results'][0]['image']


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
    
    return response.text

@app.route("/", methods = ['POST', 'GET'])
def main_routes():
    if request.method == 'POST':
        nama = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        password = request.form.get("password")
        
        session['age'] = age
        session['gender'] = gender

        return redirect(url_for('home'))

    return render_template('login.html')

@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route("/profile")
def profile():
    # return render_template('profile.html')
    pass



# wdyey = what did you eat yesterday
@app.route("/wdyey", methods=['POST', 'GET'])
def wdyey():
    
    if request.method == 'POST':
        foodquery = request.form.get('foodquery')

        return redirect(url_for('NLP', foodquery = foodquery))
    return render_template('asking.html')


@app.route("/NLP", methods=['POST', 'GET'])
def NLP():
    foodquery = request.args.get('foodquery')
    print(foodquery)
    datas = meal_query(foodquery)
    print("INI SUGAR NYA YA",datas)
    return render_template('NLP.html', datas=datas)



@app.route('/calculate', methods=['POST','GET'])
def calculate():
    print("Requests method",request.method)

    if request.method == 'POST':
        # print('jalan')
        gender = session.get('gender', None)
        age = session.get('age', None)
        height = request.form.get('input_tinggi')
        weight = request.form.get('input_berat')
        activity = request.form.get('activity')

        # print("ini request form ", height, weight, activity)

        bmi = float("{:.2f}".format(float(calculate_bmi(height, weight))))
        desc = interpretBMI(bmi)

        bmr = calculate_bmr(gender, weight, height, age)
        session['bmr'] = bmr
        session['activity'] = activity
        
        # print("bmi desc bmr",bmi,desc,bmr)
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
        {"value": formatted_calories["maintain"], "text": "Maintain Weight",
            "formatted_calories": formatted_calories["maintain"]},
        {"value": formatted_calories["mildWeightLoss"], "text": "Mild Weight Loss",
            "formatted_calories": formatted_calories["mildWeightLoss"]},
        {"value": formatted_calories["weightLoss"], "text": "Weight Loss",
            "formatted_calories": formatted_calories["weightLoss"]},
        {"value": formatted_calories["extremeLoss"], "text": "Extreme Weight Loss",
            "formatted_calories": formatted_calories["extremeLoss"]},
        {"value": formatted_calories["mildWeightGain"], "text": "Mild Weight Gain",
            "formatted_calories": formatted_calories["mildWeightGain"]},
        {"value": formatted_calories["weightGain"], "text": "Weight Gain",
            "formatted_calories": formatted_calories["weightGain"]},
        {"value": formatted_calories["fastWeightGain"], "text": "Fast Weight Gain",
            "formatted_calories": formatted_calories["fastWeightGain"]}
    ]


    if request.method == 'POST':
        print('jalan')
        timeFrame = request.form.getlist('timeFrame')
        targetCalories = request.form.getlist('goals')
        diet = request.form.getlist('diet')
        exclude = request.form.getlist('exclude')

        # print("ini BMR ", bmr)
        # print("ini Activity", activity)
        # print(calories)
        # print("data di daily meals ---->>>",
        #       timeFrame, targetCalories, diet, exclude) 

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
    # print("->>>>> datas ",datas)
    
    image_datas = dict({})
    for meal in datas['meals']:
        title = meal['title']
        print("ini title", title)
        image_datas[meal['title']] = get_meal_image(title)
    

    return render_template('meals.html', datas=datas, image_datas=image_datas)


@app.route('/summary')
def summary():
    return render_template('summary.html')








@app.route('/muscle', methods=['GET','POST'])
def muscle():
    print("Requests method",request.method)
    if request.method == 'POST':
        muscle = request.form.get('muscleList')
        intensity = request.form.get('intensitylevel')
        print(muscle,intensity)
        
        return redirect(url_for('womoves', muscle=muscle, intensity=intensity))
        
    return render_template('muscle.html')

@app.route('/womoves', methods=['GET', 'POST'])
def womoves():
    print("Requests method",request.method)
    if request.method == 'GET':
        print("Ini udah masuk kedalam rute womoves")
        muscle = request.args.get('muscle')
        intensity = request.args.get('intensity')
        print(muscle,intensity)

    if muscle == "cardio":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/cardio"
    if muscle == "neck":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/neck"
    if muscle == "shoulders":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/shoulders"
    if muscle == "chest":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/chest"
    if muscle == "back":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/back"
    if muscle == "waist":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/waist"
    if muscle == "lower_arms":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/lower%20arms"
    if muscle == "lower_legs":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/lower%20legs"
    if muscle == "upper_arms":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/upper%20arms"
    if muscle == "upper_legs":
        api_url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/upper%20legs"

    headers = {
        'X-RapidAPI-Key': 'b958d466damsh993cd90275c9ef0p1de1f2jsnb9744cfaf79c',
        'X-RapidAPI-Host': 'exercisedb.p.rapidapi.com'

    }
    response = requests.get(api_url,headers=headers)
    
    if response.status_code == 200:
        all_data = response.json()
        if intensity == "Heavy" and muscle == "cardio":
            data = [exercise for exercise in all_data if exercise.get("equipment") != "body weight"]
        elif intensity == 'Moderate' and muscle == 'shoulders':
            data = [exercise for exercise in all_data if exercise.get("equipment") == "band"][:8]
        elif intensity == 'Heavy' and muscle == 'shoulders':
            data = [exercise for exercise in all_data if exercise.get("equipment") == "cable"][:8]
        elif intensity == "Heavy":
            data = [exercise for exercise in all_data if exercise.get("equipment") != "body weight"][:8]
        else:
            data = [exercise for exercise in all_data if exercise.get("equipment") == "body weight"][:8]
    else:
        data = []  # Data kosong jika terjadi kesalahann

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



'''

{
      "sugar_g": 13.3,
      "fiber_g": 4,
      "sodium_mg": 8,
      "potassium_mg": 99,
      "fat_saturated_g": 0.1,
      
      "fat_total_g": 0.5,
      "cholesterol_mg": 0,
      "protein_g": 3.9,
      "carbohydrates_total_g": 28.6
    }

<p>'Sugar (grams)' : <b>{{ items['sugar_g'] }}</b></p>
<p>'Fiber (grams)' : <b>{{ items['fiber_g'] }}</b></p>
<p>'Sodium (mg)' : <b>{{ items['sodium_mg'] }}</b></p>
<p>'Potassium (mg)' : <b>{{ items['potassium_mg'] }}</b></p>
<p>'Saturated Fat (grams)' : <b>{{ items['fat_saturated_g'] }}</b></p>
<p>'Total Fat (grams)' : <b>{{ items['fat_total_g'] }}</b></p>
<p>'Cholesterol (mg)' : <b>{{ items['cholesterol_mg'] }}</b></p>
<p>'Protein (grams)' : <b>{{ items['protein_g'] }}</b></p>
<p>'Total Carbohydrates (grams)' : <b>{{ items['carbohydrates_total_g'] }}</b></p>

'''