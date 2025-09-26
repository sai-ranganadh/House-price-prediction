from flask import Flask,redirect,render_template,request
import os,binascii
from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField,SelectField
from wtforms.validators import ValidationError
from wtforms.validators import input_required,NumberRange
import joblib

class Infoform(FlaskForm):
    bedrooms = IntegerField("Enter no. of bedrooms: ",validators = [input_required(),NumberRange(min=0,message="Value should be minimum 0")])
    totalrooms = IntegerField("Enter total no. of rooms: ",validators = [input_required()])
    age = IntegerField("Enter age of the house: ",validators = [input_required()])
    ocean_proximity = SelectField('Choose Ocean Proximity', choices = [(0, 'INLAND'), (1, '<1H OCEAN'), (2, 'NEAR OCEAN'),(3, 'NEAR BAY'),(4, 'ISLAND')])
    submit = SubmitField("Predict")

app = Flask(__name__)
app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))

@app.route('/',methods=['GET','POST'])
def calculate_price():
    form = Infoform()
    if form.validate_on_submit():
        bedrooms = int(request.form['bedrooms'])
        totalrooms = int(request.form['totalrooms'])
        age = int(request.form['age'])
        ocean_proximity = int(request.form['ocean_proximity'])
        predicted_price = predict(bedrooms,totalrooms,age,ocean_proximity)
        predicted_price = abs(round(predicted_price[0],2))
        return render_template("display_form.html",form=form,price=predicted_price)

    return render_template("display_form.html", form=form)

def predict(bedrooms,totalrooms,age,ocean_proximity):
    longitude = -118.49
    latittude = 34.26
    population = 1166
    households = 409
    income = 3.53
    households_rooms = totalrooms/households
    bedroom_ratio = bedrooms/totalrooms
    features = [longitude, latittude, age, totalrooms, bedrooms, population, households, income, ocean_proximity, households_rooms, bedroom_ratio]
    model = joblib.load('linear_regression_model.pkl')
    predicted_price = model.predict([features])
    return predicted_price

def new_house():
    return "New House"

if __name__ == "__main__":
    app.run()

