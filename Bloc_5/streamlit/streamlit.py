import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests

### CONFIG
st.set_page_config(
    page_title="Getaround Dashboard",
    page_icon="💸", 
    layout="wide"
  )

### TITLE AND TEXT
st.title("Getaround Rental Car Dashboard  🎨")

st.markdown("""
    Welcome to the Getaround Rental Car Dashboard!

    Here, you can access valuable information about previous rental cars and even get 
    predictions about rental car prices. We aim to provide you with a comprehensive and 
    user-friendly experience to make informed decisions.
""")

### LOAD AND CACHE DATA
DATA_EDA_URL = ('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx' )

@st.cache_data # this lets the 
def load_data_eda(nrows):
    data = pd.read_excel(DATA_EDA_URL, nrows=nrows)
    return data

data_eda_load_state = st.text('Loading data...')
data_eda = load_data_eda(1000)
data_eda_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data for eda'):
    st.subheader('Raw data for eda')
    st.write(data_eda) 




### LOAD AND CACHE DATA
DATA_ML_URL = ('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv')

@st.cache_data # this lets the 
def load_data_ml(nrows):
    data = pd.read_csv(DATA_ML_URL, nrows=nrows)
    data.drop('Unnamed: 0', axis=1, inplace=True)
    return data

data_ml_load_state = st.text('Loading data...')
data_ml = load_data_ml(1000)
data_ml_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data for pricing'):
    st.subheader('Raw data for pricing')
    st.write(data_ml) 


### SHOW GRAPH STREAMLIT

# Add a plot section
st.header('Check-in Type Count')
st.markdown("""
    the majority of drivers and owners need to meet each other for renting a car
""")
st.set_option('deprecation.showPyplotGlobalUse', False)

prop_HF = data_eda["checkin_type"].value_counts(normalize=True).reset_index()
prop_HF.columns = ["checkin_type", "proportion"]
# Create the plot
plt.figure(figsize=(15, 6))
ax = sns.countplot(data=data_eda, x='checkin_type')

# Add number and proportion of each category
for p, prop, count in zip(ax.patches, prop_HF["proportion"], data_eda["checkin_type"].value_counts().sort_values(ascending=False)):
    ax.annotate(f'({count}, {prop:.0%})', (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')

# Display the plot using Streamlit
st.pyplot()








# Add a plot section
st.header('State Type Count')
st.markdown("""
    A significant number of rental car reservations remain uncancelled
""")
st.set_option('deprecation.showPyplotGlobalUse', False)


prop_HF = data_eda["state"].value_counts(normalize=True).reset_index()
prop_HF.columns = ["state", "proportion"]


plt.figure(figsize=(15,6))
ax = sns.countplot(data=data_eda, x='state')

# Add number and proportion of each category
for p, prop, count in zip(ax.patches, prop_HF["proportion"].sort_values(), data_eda["state"].value_counts().sort_values()):
    ax.annotate(f'({count}, {prop:.0%})', (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')




# Display the plot using Streamlit
st.pyplot()








# Add a plot section
st.header('Delay checkin')
st.markdown("""
    Drivers who choose the mobile check-in option tend to experience larger delays during the checkout process
""")
st.set_option('deprecation.showPyplotGlobalUse', False)

mask_is_null = data_eda['delay_at_checkout_in_minutes'].isnull() 
data_eda['delay_means'] = data_eda[~mask_is_null]['delay_at_checkout_in_minutes'].apply(lambda x: 
                                                                         'At time' if x<=0
                                                                         else 'late of 0-30' if x<30
                                                                         else 'late of 30-60' if 30<x<60                                                                
                                                                         else 'late of 60-120' if 60<x<120
                                                                         else 'Very late')
# Create the plot
plt.figure(figsize=(15,6))
sns.countplot(data=data_eda, x='checkin_type', hue='delay_means')
plt.show()
# Display the plot using Streamlit
st.pyplot()






#### CREATE TWO COLUMNS
col1, col2 = st.columns(2)

with col1:
        st.markdown("**1️⃣ drivers's number impacted by fixing a certain time delta with previous rental **")
        dt_fixe = st.number_input("Select a fixe time delta in min")
        

        
        def drivers_numbers_impacted(df, col, delta_t):
            mask = df.loc[:, col] < delta_t 
            return len(df.loc[mask])


        delta_t = np.arange(0, 721, 30)

        total_number_drivers = [drivers_numbers_impacted(data_eda, 'time_delta_with_previous_rental_in_minutes', i) for i in delta_t]
        connect_number_drivers = [drivers_numbers_impacted(data_eda[data_eda.checkin_type=='connect'], 'time_delta_with_previous_rental_in_minutes', i) for i in delta_t]
        mobile_number_drivers = [drivers_numbers_impacted(data_eda[data_eda.checkin_type=='mobile'], 'time_delta_with_previous_rental_in_minutes', i) for i in delta_t]

        nb_total_dt_fixe = drivers_numbers_impacted(data_eda, 'time_delta_with_previous_rental_in_minutes', dt_fixe)
        nb_connect_dt_fixe = drivers_numbers_impacted(data_eda[data_eda.checkin_type=='connect'], 'time_delta_with_previous_rental_in_minutes', dt_fixe)
        nb_mobile_dt_fixe = drivers_numbers_impacted(data_eda[data_eda.checkin_type=='mobile'], 'time_delta_with_previous_rental_in_minutes', dt_fixe)
        
        st.markdown(f"** drivers's number impacted by fixing dt ={dt_fixe} min for connect checkin-type  is : {nb_connect_dt_fixe} **")
        st.markdown(f"** drivers's number impacted by fixing dt ={dt_fixe} min for mobile checkin-type  is : {nb_mobile_dt_fixe} **")
        st.markdown(f"** drivers's number impacted by fixing dt ={dt_fixe} min for all checkin-type  is : {nb_total_dt_fixe } **")
        
        plt.figure(figsize=(12, 8)) 
        plt.plot(delta_t, total_number_drivers, label='Total')
        plt.plot(delta_t, connect_number_drivers, label='Connect')
        plt.plot(delta_t, mobile_number_drivers, label='Mobile')
        plt.xlabel('threshold delta t (min)')
        plt.ylabel('number_drivers')
        plt.title('drivers\'s number impacted by fixing a certain time delta with previous rental')
        plt.legend()

        st.pyplot()

with col2:
    st.markdown("**2️⃣ Get amount of money loss due to cancellation or delays**")

    with st.form("Get_amount_of_money_loss"):
        mean_rental_time = st.number_input("Define a mean rental car time in minute")
        start_delay = st.number_input("Define a munite's number from which delay start")
        submit = st.form_submit_button("submit")

        if submit:
            
            mask_12h = (data_eda['delay_at_checkout_in_minutes']> -720) & (data_eda['delay_at_checkout_in_minutes']< 720)

            #Removing outliers
            mask_price = (data_ml['rental_price_per_day'] > data_ml['rental_price_per_day'].mean()-3*data_ml['rental_price_per_day'].std()) \
                & (data_ml['rental_price_per_day'] < data_ml['rental_price_per_day'].mean()+3*data_ml['rental_price_per_day'].std())


            # amount of money loss due to cancelation
            mask_c = data_eda['state'] == 'canceled'

            number_of_cancels = len(data_eda.loc[mask_c, :])
            mean_min = mean_rental_time
            mean_rental_price_per_min = (data_ml.loc[mask_price, 'rental_price_per_day'].mean()/24)/60
            cancel_money_loss_per_min = number_of_cancels*mean_rental_price_per_min*mean_min


            # amount of money loss due to delays
            # if any cancelation is due to any delays
            mask_l = (data_eda[mask_12h]['delay_at_checkout_in_minutes'] >start_delay) 
            total_number_late = len(data_eda[mask_12h].loc[mask_l, :])
            total_minute_late = data_eda[mask_12h].loc[mask_l, 'delay_at_checkout_in_minutes'].sum()
            total_money_loss_due_to_delays = total_minute_late*cancel_money_loss_per_min



            st.metric("The amount of money loss due to cancelation per minute is :", np.round(cancel_money_loss_per_min, 2))
            st.metric("The amount of money loss per minute due to delays if any cancelation is due to any delays  is :", np.round(total_money_loss_due_to_delays, 2))








st.markdown("---")

#### CREATE TWO COLUMNS
col1, col2 = st.columns(2)

with col1:
        st.markdown("**1️⃣ Distibution of mileage by respect of fuel type **")
        fuel_type = st.selectbox("Select a fuel type you want to see distribution", data_ml["fuel"].sort_values().unique())
        
        fuel_df = data_ml[data_ml["fuel"]==fuel_type]
        fig = px.histogram(fuel_df, x="car_type", y="mileage")
        fig.update_layout(bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**2️⃣ Get mean of mileage by respect of fuel type**")

    with st.form("Get_mean_of_mileage"):
        fuel_type = st.selectbox("Select a fuel type you want to see distribution", data_ml["fuel"].sort_values().unique())
        start_mileage = st.number_input("Select a minimum mileage")
        end_mileage = st.number_input("Select a maximum mileage")
        submit = st.form_submit_button("submit")

        if submit:
            avg_mileage = data_ml[(data_ml["fuel"]==fuel_type)]
            start_mileage, end_mileage = start_mileage, end_mileage
            mask = (avg_mileage["mileage"] > start_mileage) & (avg_mileage["mileage"] < end_mileage)
            avg_mileage = avg_mileage.loc[mask, "mileage"].mean()
            st.metric("Average mileage", round(avg_mileage, 2))





# Add a plot section
st.header('Price\'s rental car prediction')
st.markdown("""
    Please select car's features:
""")
with st.form("Get_prediction"):
    model_key = st.selectbox("Select a model_key", data_ml.model_key.sort_values().unique())
    mileage = st.number_input("Enter a mileage")
    engine_power = st.number_input("Enter an engine_power")
    fuel = st.selectbox("Select a fuel type", data_ml.fuel.sort_values().unique())
    paint_color = st.selectbox("Select a paint_color", data_ml.paint_color.sort_values().unique())
    car_type = st.selectbox("Select a car_type", data_ml.car_type.sort_values().unique())
    # Define the list of boolean options
    boolean_options = [True, False]
    private_parking_available = st.selectbox("Select if you want private parking available", boolean_options)

    has_gps = st.selectbox("Select if you want gps", boolean_options)
    has_air_conditioning = st.selectbox("Select if you want air conditioning", boolean_options)
    automatic_car = st.selectbox("Select if you want automatic car", boolean_options)
    has_getaround_connect = st.selectbox("Select if it is by getaround connect", boolean_options)
    has_speed_regulator = st.selectbox("Select if it has speed regulator", boolean_options)
    winter_tires = st.selectbox("Select if you want winter_tires", boolean_options)

    submit = st.form_submit_button("submit")

    if submit:
        

        url = 'https://chris-getaround-api.herokuapp.com/predict_price'
        request_pred = requests.post(url, json={ "model_key": model_key, 
                                                "mileage": mileage, 
                                                "engine_power": engine_power, 
                                                "fuel": fuel, 
                                                "paint_color": paint_color, 
                                                "car_type": car_type, 
                                                "private_parking_available": private_parking_available, 
                                                "has_gps": has_gps, 
                                                "has_air_conditioning": has_air_conditioning, 
                                                "automatic_car": automatic_car, 
                                                "has_getaround_connect": has_getaround_connect, 
                                               "has_speed_regulator": has_speed_regulator, 
                                               "winter_tires": winter_tires })
        
        st.metric("Rental price prediction for this car", round(request_pred.json()['prediction'],2), "$")

