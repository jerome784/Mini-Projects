import streamlit as st
import pandas as pd
import joblib

model=joblib.load('titanic_model.pkl');

st.title("Titanic Survival Predictor")

pclass=st.selectbox("Passenger Class(Pclass)",[1,2,3])
age=st.slider("Age",0,80,25)
fare=st.slider("Fare",0,500,50)

if st.button("Predict Survival"):
    input_df=pd.DataFrame([[pclass,age,fare]],columns=["Pclass","Age","Fare"])
    prediction=model.predict(input_df)[0]
    if prediction==1:
        st.success("Survived")
    else:
        st.error("Did not Survive")