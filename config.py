import os


class Config:
    def __init__(self):
        self.API_KEY = os.environ.get('API_KEY')
        self.URL_SEARCH_RECIPE = 'https://api.spoonacular.com/recipes/complexSearch'
        self.URL_DETAIL_RECIPE = 'https://api.spoonacular.com/recipes/{id}/information'
        self.URL_GENERATE_MEAL_PLAN = 'https://api.spoonacular.com/mealplanner/generate'
        self.X_API_KEY = os.environ.get('X_API_KEY')
        self.URL_NPL_NINCAL = 'https://api.calorieninjas.com/v1/nutrition?query='
