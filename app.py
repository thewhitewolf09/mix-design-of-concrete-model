import flask
from flask import Flask, render_template, request, flash
import pickle

app = Flask(__name__)
app.secret_key = "dfgjhklihfcggvhbkjnjklhugfcg56789"

@app.route('/')
def hero():
    return render_template("hero.html")

@app.route('/predict', methods=['GET', 'POST'])
def index():
    results = {
        "ratio": "",
        "strength_7_days": "",
        "strength_28_days": "",
        "strength_entered_age": ""
    }
    
    
    if request.method == 'POST':
        
        type_of_cement = request.form.get("type_of_cement")
        cement_type_supported = ['OPC', 'PPC', 'Others']
        if type_of_cement not in cement_type_supported:
            results["strength_entered_age"] = "Invalid cement type. Must be OPC, PPC, or Others"
            return render_template('index.html', **results)
        
        cement = request.form.get('cement')
        slag = request.form.get('slag')
        ash = request.form.get('ash')
        
        water = request.form.get('water')
        superplastic = request.form.get('superplastic')
        
        coarseagg = request.form.get('coarseagg')
        fineagg = request.form.get('fineagg')
        age = request.form.get('age')
        
        
        grade_of_concrete = request.form.get('grade_of_concrete')

        if grade_of_concrete and not grade_of_concrete.startswith('M'):
            results["strength_entered_age"] = "Grade must start with 'M' (e.g., M20, M25)"
            return render_template('index.html', **results)
        
        
        if cement and slag and ash and water and superplastic and coarseagg and fineagg and age and grade_of_concrete:
            try:
                cement_val = float(cement)
                water_val = float(water)
                fineagg_val = float(fineagg)
                coarseagg_val = float(coarseagg)
                slag_val = float(slag)
                ash_val = float(ash)
                superplastic_val = float(superplastic)
                age_val = float(age)

                if cement_val > 0:
                    ratio = (
                        round(water_val / cement_val, 2),
                        1,
                        round(fineagg_val / cement_val, 2),
                        round(coarseagg_val / cement_val, 2)
                    )
                    results["ratio"] = f"Ratio (water:cement:FA:CA): {ratio[0]}:1:{ratio[2]}:{ratio[3]}"
                else:
                    results["ratio"] = "Invalid cement value for ratio calculation"

                rfr_model = pickle.load(open('rfr_concrete_data.pkl', 'rb'))

                inputs = [
                    cement_val, slag_val, ash_val, water_val,
                    superplastic_val, coarseagg_val, fineagg_val
                ]
                

                days_7 = inputs + [7.0]
                days_7_pred = rfr_model.predict([days_7])[0]
                results["strength_7_days"] = f"Strength at 7 days: {days_7_pred:.2f} MPa"


                days_28 = inputs + [28.0]
                days_28_pred = rfr_model.predict([days_28])[0]
                results["strength_28_days"] = f"Strength at 28 days: {days_28_pred:.2f} MPa"
                age_entered = inputs + [age_val]
                custom_age_pred = rfr_model.predict([age_entered])[0]
                results["strength_entered_age"] = f"Strength at {age_val} days: {custom_age_pred:.2f} MPa"
            except ValueError:
                results["strength_entered_age"] = "Please enter valid numerical values"
                
        else:
            results["strength_entered_age"] = "All fields are mandatory"
            

    return render_template('index.html', **results)

if __name__ == '__main__':
    app.run(debug=True)