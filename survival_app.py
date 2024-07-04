# -*- coding: utf-8 -*-
"""survival_app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1C4LFy1q7JbeekbFr2ltKmysWbM4-W4Fh
"""

import numpy as np
import streamlit as st
import pickle
import warnings

warnings.filterwarnings("ignore")

# Load the saved model
try:
    with open('survival_prediction.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
except FileNotFoundError:
    st.error("Model file not found. Ensure 'survival_pred.sav' is in the same directory.")

def survival_prediction(input_data):
    input_data_as_np_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_np_array.reshape(1, -1)

    try:
        prediction = loaded_model.predict(input_data_reshaped)
        pred_proba = loaded_model.predict_proba(input_data_reshaped)
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None, None

    risk = pred_proba[:, 1]
    risk_percent = round(risk[0] * 100, 2)

    if prediction[0] == 0:
        return 'The person did not survive', risk_percent
    else:
        return 'The person survived', risk_percent

# User Interface
st.set_page_config(page_title="Titanic Survival Prediction", page_icon=':ship:', layout='centered')
st.title('Survival Risk Prediction')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

Pclass = st.selectbox('Pclass', [1, 2, 3])
Age = st.slider('Age', 0, 80, 30)
SibSp = st.number_input('SibSp', 0, 10, 0)
Parch = st.number_input('Parch', 0, 10, 0)
Fare = st.number_input('Fare', 0, 500, 0)
male = st.selectbox('Male', [0, 1])
female = st.selectbox('Female', [0, 1])
Embarked_c = st.selectbox('Embarked_C', [0, 1])
Embarked_q = st.selectbox('Embarked_Q', [0, 1])
Embarked_s = st.selectbox('Embarked_S', [0, 1])

input_data = [Pclass, Age, SibSp, Parch, Fare, male, female, Embarked_c, Embarked_q, Embarked_s]

# Prediction
if st.button('Risk Prediction'):
    diagnosis, risk_percent = survival_prediction(input_data)
    if diagnosis:
        st.write(diagnosis)
        st.write(f"Risk Percentage: {risk_percent}%")

if st.button('Percentage of Risk'):
    _, risk_percent = survival_prediction(input_data)
    if risk_percent is not None:
        st.write(f"Risk Percentage: {risk_percent}%")