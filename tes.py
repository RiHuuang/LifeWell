import os

api_key = os.environ.get('API_KEY')

if api_key is None:
    raise ValueError("API_KEY environment variable is not set.")

# Now you can use the API_KEY in your code
print(f"API_KEY: {api_key}")

# # Get the current working directory (where your Python script is located)
# current_directory = os.path.dirname(os.path.realpath(__file__))

# # Your Flask app's root directory is usually one level above the current directory
# root_directory = os.path.abspath(os.path.join(current_directory, '..'))

# print("Root directory:", root_directory)

"""
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


@app.route("/", methods=['POST', 'GET'])
def generate_meal():
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
        print(timeFrame, targetCalories, diet, exclude)
        # datas = get_meal_plan(timeFrame,targetCalories,diet, exclude)
        check = True
        if timeFrame == '' or not timeFrame:
            flash("Time frame couldn't be empty!", 'danger')
            check = False

        if targetCalories == '' or not targetCalories:
            flash("Target calories couldn't be empty", 'danger')
            check = False

        if not check:
            return redirect(url_for('static'))

        return redirect(url_for('get_meal'), timeFrame=timeFrame, targetCalories=targetCalories, diet=diet, exclude=exclude)

    return render_template('dailyMeals.html')


@app.route("/get_meal", methods=['POST', 'GET'])
def get_meal(timeFrame, targetCalories, diet, exclude):
    # datas = get_meal_plan(
    #     timeFrame=timeFrame, targetCalories=targetCalories, diet=diet, exclude=exclude)
    # return render_template('get_meal.html', datas=datas)
    pass

"""