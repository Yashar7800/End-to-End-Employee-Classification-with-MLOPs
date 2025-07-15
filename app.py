from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
from mlProject.pipeline.prediction import PredictionPipeline


app = Flask(__name__)

@app.route('/',methods = ['GET'])
def homepage():
    return render_template('index.html')


@app.route('/train',methods=['GET'])
def training():
    os.system('python main.py')
    return 'Training Successful'

@app.route("/predict", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
        try:
            # Read inputs from the form
            education = request.form["Education"]
            joining_year = int(request.form["JoiningYear"])
            city = request.form["City"]
            payment_tier = int(request.form["PaymentTier"])
            age = int(request.form["Age"])
            gender = request.form["Gender"]
            ever_benched = request.form["EverBenched"]
            experience = int(request.form["ExperienceInCurrentDomain"])
            
            # Compute Tenure
            tenure = 2025 - joining_year
            
            # Create DataFrame
            data = {
                "Education": education,
                "JoiningYear": joining_year,
                "City": city,
                "PaymentTier": payment_tier,
                "Age": age,
                "Gender": gender,
                "EverBenched": ever_benched,
                "ExperienceInCurrentDomain": experience,
                "Tenure": tenure
            }
            df = pd.DataFrame([data])
            
            # Predict using PredictionPipeline
            obj = PredictionPipeline()
            predict = obj.predict(df)
            
            # Map prediction to text
            result = "Will Leave" if predict[0] == 1 else "Will Stay"
            
            return render_template("results.html", prediction=result)
        
        except Exception as e:
            print(f"The Exception message is: {e}")
            return render_template("results.html", prediction="Error: Something went wrong. Please check your inputs.")
    
    # Handle GET requests (e.g., direct access to /predict)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)