import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Iris Flower Prediction App
This streamlit app predicts the Iris Flowers
""")

st.sidebar.header('Input Parameters')

def input_features():
    sepal_length = st.sidebar.slider('sepal length', 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider('sepal width', 2.2, 4.4, 3.4)
    petal_length = st.sidebar.slider('petal length', 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('petal width', 0.1, 2.5, 0.2)

    data = {
        'sepal length (cm)': sepal_length,
        'sepal width (cm)' : sepal_width,
        'petal length (cm)' : petal_length,
        'petal width (cm)' : petal_width
    }
    features = pd.DataFrame(data, index=[0])
    return features

df = input_features()

st.subheader('Input Parameters')
st.dataframe(df)

iris = datasets.load_iris()

X = pd.DataFrame(iris.data, columns=iris.feature_names)
Y = iris.target

clf = RandomForestClassifier()
clf.fit(X,Y)

prediction = clf.predict(df)
prediction_prob = clf.predict_proba(df)

st.subheader('Class Labels')
st.write(iris.target_names)

st.subheader('Prediction')
st.write(iris.target_names[prediction])

st.subheader('Prediction Probability')
st.write(prediction_prob)