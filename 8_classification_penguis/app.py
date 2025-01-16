import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier


def input_features():
    island = st.sidebar.selectbox('Island', ('Biscoe', 'Dream', 'Torgersen'))
    sex = st.sidebar.selectbox('Sex', ('MALE', 'FEMALE'))
    bill_length_mm = st.sidebar.slider('Bill Length (mm)', 32.10, 43.9,59.60)
    bill_depth_mm = st.sidebar.slider('Bill Depth (mm)', 13.10, 17.16, 21.50)
    flipper_length_mm = st.sidebar.slider('Flipper Length (mm)', 172.0, 200.96, 231.0)
    body_mass_g = st.sidebar.slider('Body Mass (gram)', 2700.0, 4207.0, 6300.0)

    data = {
        'island': island,
        'sex': sex,
        'bill_length_mm': bill_length_mm,
        'bill_depth_mm': bill_depth_mm,
        'flipper_length_mm': flipper_length_mm,
        'body_mass_g': body_mass_g
    }

    features = pd.DataFrame(data, index= [0])

    return features

st.write("""
# Penguis Prediction App
This Streamlit app predicts **Penguis** species
""")

st.sidebar.header("Input Features")
st.sidebar.markdown("""
[Example CSV Input](https://github.com/usman619/datascience_projects/tree/main/8_classification_penguis/example_penguins_input.csv)
""")

uploaded_file = st.sidebar.file_uploader("Upload your Input CSV file here",type=['csv'])

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    input_df = input_features()

penguins_raw = pd.read_csv('penguins_cleaned.csv')
penguins = penguins_raw.drop(columns=['species'])

df = pd.concat([input_df, penguins], axis=0)

encode = ['sex', 'island']

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]

# Show the first row by default
df = df[:1]

if uploaded_file is not None:
    st.write(df)    # Replace with user input
else:
    st.write('Update the input features. Showing example Input Features')
    st.write(df)

# Import Penguin Classification Model
load_clf = pickle.load(open('penguin_clf.pkl','rb'))

# Apply the model on the user input
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

st.subheader('Prediction')
penguis_species = np.array(['Adelie', 'Chinstrap', 'Gentoo'])
st.write(penguis_species[prediction])

st.subheader('Probability')
st.write(prediction_proba)