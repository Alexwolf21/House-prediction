import streamlit as st
import pandas as pd
import pickle

@st.cache
def load_model():
    with open('finalized_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model


def predict(longitude, latitude, housing_median_age,
            total_rooms, total_bedrooms, population,
            households, median_income, ocean_pro):
    ocean = 0 if ocean_pro == '<1H OCEAN' else 1 if ocean_pro == 'INLAND' else 2 if ocean_pro == 'ISLAND' else 3 if ocean_pro == 'NEAR BAY' else 4
    med_income = median_income / 5
    input_data = pd.DataFrame({
        'Longitude': [longitude],
        'Latitude': [latitude],
        'Housing age': [housing_median_age],
        'Total rooms': [total_rooms],
        'Total bedrooms': [total_bedrooms],
        'Population': [population],
        'Households': [households],
        'Median income': [median_income],
        'Ocean Proximity': [ocean_pro]
    })
    return model.predict(input_data)[0]

model = load_model()

def main():
    style = """<div style='background-color:pink; padding:12px'>
              <h1 style='color:black'>House Price Prediction App</h1>
       </div>"""
    st.markdown(style, unsafe_allow_html=True)
    left, right = st.columns((2, 2))
    longitude = left.number_input('Enter the Longitude in negative number',
                                  step=1.0, format="%.2f", value=-21.34)
    latitude = right.number_input('Enter the Latitude in positive number',
                                  step=1.0, format='%.2f', value=35.84)
    housing_median_age = left.number_input('Enter the median age of the building',
                                           step=1.0, format='%.1f', value=25.0)
    total_rooms = right.number_input('How many rooms are there in the house?',
                                     step=1.0, format='%.1f', value=56.0)
    total_bedrooms = left.number_input('How many bedrooms are there in the house?',
                                       step=1.0, format='%.1f', value=15.0)
    population = right.number_input('Population of people within a block',
                                    step=1.0, format='%.1f', value=250.0)
    households = left.number_input('Population of a household', step=1.0,
                                   format='%.1f', value=43.0)
    median_income = right.number_input('Median_income of a household in Dollars',
                                       step=1.0, format='%.1f', value=3000.0)
    ocean_proximity = st.selectbox('How close to the sea is the house?',
                                   ('<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND'))
    button = st.button('Predict')

    # if button is pressed
    if button:
        # make prediction
        result = predict(longitude, latitude, housing_median_age,
                         total_rooms, total_bedrooms, population,
                         households, median_income, ocean_proximity)
        st.success(f'The value of the house is ${result}')