import pickle
import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt

st.write("""
# Boston House Price Prediction App
""")

st.markdown("---")

df = pd.read_csv("boston.csv")

st.sidebar.header('User Input Parameters')

def input_features():
    CRIM = st.sidebar.slider('CRIM', min_value=0.0063, max_value=88.9762, value=3.6135)
    ZN = st.sidebar.slider('ZN', min_value=0.0, max_value=100.0, value=11.3636)
    INDUS = st.sidebar.slider('INDUS', min_value=0.46, max_value=27.74, value=11.1368)
    CHAS = st.sidebar.slider('CHAS', min_value=0.0, max_value=1.0, value=0.0692)
    NOX = st.sidebar.slider('NOX', min_value=0.385, max_value=0.871, value=0.5547)
    RM = st.sidebar.slider('RM', min_value=3.561, max_value=8.78, value=6.2846)
    AGE = st.sidebar.slider('AGE', min_value=2.9, max_value=100.0, value=68.5749)
    DIS = st.sidebar.slider('DIS', min_value=1.1296, max_value=12.1265, value=3.795)

    RAD = st.sidebar.slider('RAD', min_value=1, max_value=24, value=9)
    TAX = st.sidebar.slider('TAX', min_value=187, max_value=711, value=408)

    PTRATIO = st.sidebar.slider('PTRATIO', min_value=12.6, max_value=22.0, value=18.4555)
    B = st.sidebar.slider('B', min_value=0.32, max_value=396.9, value=356.674)
    LSTAT = st.sidebar.slider('LSTAT', min_value=1.73, max_value=37.97, value=12.6531)

    data = {
        'CRIM':CRIM,
        'ZN':ZN,
        'INDUS':INDUS,
        'CHAS':CHAS,
        'NOX':NOX,
        'RM':RM,
        'AGE':AGE,
        'DIS':DIS,
        'RAD':RAD,
        'TAX':TAX,
        'PTRATIO':PTRATIO,
        'B':B,
        'LSTAT':LSTAT
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Getting the user inputs
input_df = input_features()

# Showing the input df
st.subheader('User Input Parameters')
st.dataframe(input_df)

# Importing the model
load_clf = pickle.load(open('boston_model.pkl','rb'))
prediction = load_clf.predict(input_df)

# Showing the Prediction
st.subheader('Prediction of MEDV')
st.dataframe(prediction)

st.markdown("---")
st.subheader('Feature Importance')
importance = load_clf.feature_importances_
feature_names = df.columns[:-1]
df_imp = pd.DataFrame(importance, index=feature_names, columns=['Importance'])
st.dataframe(df_imp.sort_values(by=['Importance'], ascending=False))

