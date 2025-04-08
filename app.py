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

    form_values = {
        "type_of_cement": "",
        "cement": "",
        "slag": "",
        "ash": "",
        "water": "",
        "superplastic": "",
        "coarseagg": "",
        "fineagg": "",
        "age": "",
        "grade_of_concrete": ""
    }

    if request.method == 'POST':
        # Grab all form values
        for key in form_values:
            form_values[key] = request.form.get(key, "")

        type_of_cement = form_values["type_of_cement"]
        cement_type_supported = ['OPC', 'PPC', 'Others']
        if type_of_cement not in cement_type_supported:
            results["strength_entered_age"] = "Invalid cement type. Must be OPC, PPC, or Others"
            return render_template('index.html', **results, form_values=form_values)

        grade_of_concrete = form_values["grade_of_concrete"]
        if grade_of_concrete and not grade_of_concrete.startswith('M'):
            results["strength_entered_age"] = "Grade must start with 'M' (e.g., M20, M25)"
            return render_template('index.html', **results, form_values=form_values)

        try:
            cement_val = float(form_values["cement"])
            slag_val = float(form_values["slag"])
            ash_val = float(form_values["ash"])
            water_val = float(form_values["water"])
            superplastic_val = float(form_values["superplastic"])
            coarseagg_val = float(form_values["coarseagg"])
            fineagg_val = float(form_values["fineagg"])
            age_val = float(form_values["age"])

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
            results["strength_7_days"] = f"Strength at 7 days: {rfr_model.predict([days_7])[0]:.2f} MPa"

            days_28 = inputs + [28.0]
            results["strength_28_days"] = f"Strength at 28 days: {rfr_model.predict([days_28])[0]:.2f} MPa"

            age_input = inputs + [age_val]
            results["strength_entered_age"] = f"Strength at {age_val} days: {rfr_model.predict([age_input])[0]:.2f} MPa"

        except ValueError:
            results["strength_entered_age"] = "Please enter valid numerical values"

    return render_template('index.html', **results, form_values=form_values)

if __name__ == '__main__':
    app.run(debug=True)
