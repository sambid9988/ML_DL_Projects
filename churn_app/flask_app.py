# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 14:48:04 2020

@author: John
"""

#import os
#os.chdir('C://Users//John//Documents/churn_app/')

import pandas as pd

from flask import Flask, request
import numpy as np
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler



app=Flask(__name__)
Swagger(app)
pickle_in = open("classifier.pkl","rb")
classifier=pickle.load(pickle_in)

@app.route('/')
def welcome():
    return "Welcome All"


@app.route('/predict_file',methods=["POST"])
def predict_churn_file():
    """Let's find who is churning 
    This is using docstrings for specifications.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: The output values
        
    """
    
    df_test=pd.read_csv(request.files.get("file"))
    df_test["TotalCharges"] = pd.to_numeric(df_test["TotalCharges"], errors='coerce')
    df_test.dropna(inplace = True)
    df_test.drop("customerID",inplace=True,axis=1)
    df_test['Churn'].replace(to_replace='Yes', value=1, inplace=True)
    df_test['Churn'].replace(to_replace='No',  value=0, inplace=True)
    df_test1 = pd.get_dummies(df_test)
    df_test2 = df_test1.drop(columns = ['Churn'])
    scaler = MinMaxScaler(feature_range = (0,1))
    scaler.fit(df_test2)
    df_test3 = pd.DataFrame(scaler.transform(df_test2))
    prediction=classifier.predict(df_test3)
    
    return "The predicted values are"+str(list(prediction))


if __name__=='__main__':
    app.run()
  
