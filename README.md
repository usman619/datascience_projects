# datascience_projects
This repository contains data science projects implemented using Streamlit, a web application framework for Python. Each project is designed to demonstrate different data science concepts and techniques.

## 1. Simple Stock Price
This project displays the stock closing price and volume for Google (GOOGL) using the YFinance library.

- Install Streamlit and YFinance packages:
    ```bash
    pip install streamlit
    pip install yfinance
    ```
- Run the streamlit app using the following command:
    ```bash
    cd 1_simple_stock_price
    streamlit run app.py
    ```
## 2. Simple Bioinformatics DNA
This project counts the nucleotide composition of a query DNA sequence and visualizes the results using Altair.

- Run the streamlit app using the following command:
    ```bash
    cd 2_simple_bioinformatics_dna
    streamlit run app.py
    ```

## 3. EDA Basketball
This project performs exploratory data analysis (EDA) on NBA player statistics. It allows users to filter player stats by year, team, and position, and visualize the data using various charts and heatmaps.

- Run the Streamlit app using the following command:
    ```bash
    cd 3_eda_basketball
    streamlit run app.py
    ```

## 4. EDA Football
This project performs exploratory data analysis (EDA) on Football player statistics. It allows users to filter player stats by year, team, and position, and visualize the data using various charts and heatmaps.

- Run the Streamlit app using the following command:
    ```bash
    cd 4_eda_football
    streamlit run app.py
    ```

## 5. EDA S&P-500 Stock:

This project performs exploratory data analysis (EDA) on S&P 500 stock prices. It retrieves the list of S&P 500 companies, allows users to filter companies by sector, and visualizes the stock closing prices for the selected companies.

- Run the Streamlit app using the following command:
    ```bash
    cd 5_eda_sp500_stock
    streamlit run app.py
    ```

## 6. EDA Cryptocurrency

## 7. Classification Iris

This project demonstrates a classification model using the famous Iris dataset. The Iris dataset contains measurements of sepal length, sepal width, petal length, and petal width for three different species of iris flowers: setosa, versicolor, and virginica.

The application is built using Streamlit and allows users to input measurements for an iris flower. The model then predicts the species of the iris flower based on the input measurements and displays the prediction along with the prediction probabilities.

- Run the Streamlit app using the following command:
    ```bash
    cd 7_classification_iris
    streamlit run app.py
    ```

## 8. Classification Penguins

This project demonstrates a classification model using the Palmer Penguins dataset. The dataset contains measurements for three different species of penguins: Adelie, Chinstrap, and Gentoo. The features include bill length, bill depth, flipper length, body mass, sex, and island.

The application is built using Streamlit and allows users to input measurements for a penguin. The model then predicts the species of the penguin based on the input measurements and displays the prediction along with the prediction probabilities.

- For the "penguins_size.csv" datasets use the "data_cleaning.ipynb" jupyter notebook and run all the cells.

- Now, for creating the Penguin Classification Model use the following command on "model_building.py" file:
    ```bash
    python model_building.py
    ```

- Run the Streamlit app using the following command:
    ```bash
    cd 8_classification_penguis
    streamlit run app.py
    ```