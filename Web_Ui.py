import streamlit as st
import pickle
import numpy as np
# from PIL import Image 
import plotly.graph_objects as go


veri_status_mapping8 = {"Hero":0,"Honda":1,"TVS":2}
veri_status_mapping7 = {"M1":0,"M2":1,"M3":2,"M4":3}
with open('Models/cibil.pkl', 'rb') as f:
    model = pickle.load(f)
with open('Models/ClaimsH.pkl','rb') as f:
    model1 = pickle.load(f)
with open('Models/Closeprox.pkl','rb') as f:
    model2 = pickle.load(f)
with open('Models/DLrepeat.pkl','rb') as f:
    model3 = pickle.load(f)
with open('Models/FraudLingo.pkl','rb') as f:
    model4 = pickle.load(f)
with open('Models/Incosistency.pkl','rb') as f:
    model5 = pickle.load(f)
with open('Models/Inflaited.pkl','rb') as f:
    model6 = pickle.load(f)
with open('Models/Interprox.pkl','rb') as f:
    model7 = pickle.load(f)
with open('Models/MarketRoll.pkl','rb') as f:
    model8 = pickle.load(f)
with open('Models/Tampered.pkl','rb') as f:
    model9 = pickle.load(f)
# -------------------------------------------------------------------------------

st.title('Welcome to Iassist Motor Fraud Detection 🚗')
# -------------------------------------------------------------------------------

col1, col2 = st.columns(2)

col1a, col2a = st.columns(2)
with col1:
    map8_oem = st.selectbox(
        'Please select the company of your vecile',
        options=('Hero','Honda','TVS'),
        help='Please select the Brand of your vecile'
    )
    
with col2:
    model_nu = st.selectbox(
        'Please select the Model number of your vecile',
        options=('M1','M2','M3','M4'),
        help='Please select the Model number of there brand'
    )


in_age = st.slider(
    'Please enter the Age of the car',
    0,
    20,
    10,
    help='How old is your car? if you brought it in 2020 and currently 2023 is going on then enter 3'
) 


# owned property
with col1a:
    car_price = st.number_input(
        'What is orignal prize of vechile',
            0
    )

# owned property
with col2a:
    idv = st.number_input(
        'What is IDV of vecile',
            0
    )
    
date1, date2 = st.columns(2)

with date1:
    map4_policy_date = st.date_input(
        'When did you buyed the policy',
        help='Please select the date when you bought the policy'
    )
    
with date2:
    map4_accident_date = st.date_input(
        'When did you met up with accident',
        help='Please select when you met up with accident'
    )

map4_reporting_date = st.date_input(
    'When did you reported about accident',
    help='Please select when you reported about accident'
)


policacc = abs((map4_accident_date - map4_policy_date).days)
reportpoli = abs((map4_reporting_date - map4_policy_date ).days)
reportacc = abs((map4_reporting_date - map4_accident_date).days)
oem = veri_status_mapping8[map8_oem]
model_name = veri_status_mapping7[model_nu]
orig_price = abs(int(car_price))
idv_price = abs(int(idv))
age = abs(int(in_age))

# Now add a submit button to the form:
if st.button('Check my chances'):
    temp_li = np.array([oem,model_name,orig_price,age,idv_price,policacc,reportpoli,reportacc])
    total_perc = 0
    if(model.predict([temp_li]) == 1):
        total_perc += 18
    if(model1.predict([temp_li]) == 1):
        total_perc += 13
    if(model2.predict([temp_li]) == 1):
        total_perc += 8
    if(model3.predict([temp_li]) == 1):
        total_perc += 5.5
    if(model4.predict([temp_li]) == 1):
        total_perc += 10.5
    if(model5.predict([temp_li]) == 1):
        total_perc += 5.5
    if(model6.predict([temp_li]) == 1):
        total_perc += 8.0
    if(model7.predict([temp_li]) == 1):
        total_perc += 13
    if(model8.predict([temp_li]) == 1):
        total_perc += 10.5
    if(model9.predict([temp_li]) == 1):
        total_perc += 8.0
    if policacc < 8:
        total_perc += 100
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = total_perc,
        mode = "gauge+number+delta",
        title = {'text': "Risk Factor"},
        delta = {'reference': 55},
        gauge = {'axis': {'range': [None, 100]},
                'steps' : [
                    {'range': [0, 45], 'color': "lightgray"},
                    {'range': [45, 85], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}}))
    st.plotly_chart(fig, use_container_width=True)
    pass



