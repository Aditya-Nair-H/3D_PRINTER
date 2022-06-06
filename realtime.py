# importing the libraries
#from tkinter.font import names
import streamlit as st # for web application
import numpy as np # for mathematical calculations
import time # for time loop
import pandas as pd # for dataframe
import plotly
import plotly.express as px # for interactive charts
import pickle
from xgboost import XGBRegressor

#importing cdata for getting sql data
#import cdata.sql as mod
#conn = mod.connect("User=user@domain.com; Password=password;")
 
#Create cursor and iterate over results
#cur = conn.cursor()
#cur.execute("SELECT * FROM SQLTable")
#rs = cur.fetchall()
#for row in rs:
#print(row)


def main():
    df = pd.read_csv("C:/Users/ADITYA NAIR H/Desktop/PROJECT/datasets/Data2.csv")
    regressor2 = pickle.load(open('C:/Users/ADITYA NAIR H/Downloads/pima.pickle(1).dat', 'rb'))

    #Renaming columns
    df = df.rename(columns={'Extruder ActualTemperature': 'Extruder_Actual_Temperature'})


    st.set_page_config(
        page_title = '3D PRINTER DEMO-DASHBOARD',
        layout = 'wide'
        )

    st.title('3D PRINTER DEMO-DASHBOARD')

    # input variable variables
    FeedRateInMMperMin_filter = st.selectbox('Select the FeedRateInMMperMin', pd.unique(df['FeedRateInMMperMin']))
    XPositionInMM_filter = st.selectbox('Select the XPositionInMM', pd.unique(df['XPositionInMM']))
    YPositionInMM_filter = st.selectbox('Select the YPositionInMM', pd.unique(df['YPositionInMM']))
    ZPositionInMM_filter = st.selectbox('Select the ZPositionInMM', pd.unique(df['ZPositionInMM']))
    Extruder_DesiredTemperature_filter = st.selectbox('Select the Extruder DesiredTemperature', pd.unique(df['Extruder DesiredTemperature']))
    HeaterDutyCycle_filter = st.selectbox('Select the HeaterDutyCycle', pd.unique(df['HeaterDutyCyle']))
    #Chamber_ActualTemperature_filter = st.selectbox('Select the Chamber ActualTemperature', pd.unique(df['Chamber ActualTemperature']))
    ChamberTemp_filter = st.selectbox('Select the ChamberTemp', pd.unique(df['ChamberTemp']))

    #RANGE SELECTION OF TEMPERERATURE
    df=df.query("Extruder_Actual_Temperature> 180 ")
    df=df.query("Extruder_Actual_Temperature<  230")


    placeholder = st.empty


    fig1 = px.violin(df[df['FeedRateInMMperMin']== FeedRateInMMperMin_filter], x = 'ChamberTemp', y= 'Extruder_Actual_Temperature', title = 'Target variable spread along ChamberTemp @constant Feedrate')
    st.plotly_chart(fig1)

    fig2 = px.violin(df[df['XPositionInMM']== XPositionInMM_filter], x = 'YPositionInMM', y= 'Extruder_Actual_Temperature', title = 'Target variable vs Y position @constant X position')
    st.plotly_chart(fig2)

    fig3 = px.pie(df[df['HeaterDutyCyle']== HeaterDutyCycle_filter], names= 'Extruder_Actual_Temperature', title = 'Distribution of Target variable along HeaterDutyCycle', hole = 0.5)
    st.plotly_chart(fig3)

    # run prediction model
    if st.button('Predict'):
        makeprediction = regressor2.predict([[FeedRateInMMperMin_filter, XPositionInMM_filter, YPositionInMM_filter, ZPositionInMM_filter, HeaterDutyCycle_filter, ChamberTemp_filter]])
        output = round(makeprediction[0], 1)
        st.success('The predicted extruder actual temperature is {}'.format(output))
if __name__ == '__main__':
    main()
