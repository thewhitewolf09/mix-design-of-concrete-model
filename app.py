import flask
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

@app.route('/')
def hero():
    return render_template("hero.html")

@app.route('/predict', methods=['GET', 'POST'])
def index():
    prediction = [""] 
    if request.method == 'POST':
        cement = request.form.get('cement')
        slag = request.form.get('slag')
        ash = request.form.get('ash')
        water = request.form.get('water')
        superplastic = request.form.get('superplastic')
        coarseagg = request.form.get('coarseagg')
        fineagg = request.form.get('fineagg')
        age = request.form.get('age')
        
        if cement and slag and ash and water and superplastic and coarseagg and fineagg and age:
            rfr_model = pickle.load(open('rfr_concrete_data.pkl','rb'))
            prediction = rfr_model.predict([[float(cement), float(slag), float(ash), float(water), float(superplastic), float(coarseagg), float(fineagg), float(age)]])
        else:
            prediction = ["Please fill all the fields"]
        
    return render_template('index.html', prediction_text=f"Strength: {prediction[0]}")

if __name__ == '__main__':
    app.run(debug=True)