
import seaborn as sns  # pip install seaborn
import statsmodels.api as sm  # pip install statsmodels
from authent_streamlit_doc import check_password
from logout_button import logout_button
import hmac
import streamlit as st
import pandas as pd
import numpy as np
import json
import random
# import mysqlclient  # pip install mysqlclient (hard to work with this pacakge)
# import PIL
from PIL import Image
# import pymysql  # pip install pymysql
import io
from io import BytesIO
import base64
from datetime import date
import pdfkit  # pip install pdfkit
# pip install Jinja2
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import time
from time import sleep
# import streamlit_authenticator as stauth  # pip install streamlit-authenticator
# import mysql.connector  # pip install mysql-connector-python
# from mysql.connector import FieldType  # pip install mysql-connector-python
from sqlalchemy.sql import text  # pip install SQLAlchemy
import sqlite3  # pip install db-sqlite3
import sys
import os
# import toml
# from streamlit_drawable_canvas import st_canvas
# from fn_drawables import process_canvas
from fn_fileupload import process_image
from menu import menu_with_redirect
import sqlalchemy.exc

# Redirect to Login.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if "username" not in st.session_state or st.session_state.username == '' or st.session_state.username == None:
    st.warning("You haven't logged in; Please login.")

elif "course" not in st.session_state or st.session_state.course == '' or st.session_state.course == None or st.session_state.course != "Econ3333":
    st.warning(
        "You are not allowed to access this courese with the credentials you submitted.")


else:
    st.title("Econ 3333 Regression Analysis")
    # st.subheader("Regression Analysis Using Python & Streamlit")
    logout_button()

    # sqlite database connection (local and unique to the user)
    # conn = st.connection('students', type='sql', ttl=60)
    conn = st.connection('students_db', type='sql', ttl=0)
    tablename = "Econ3333_pset03e"
    username = st.session_state.username

    # 2. Upload Dataset
    upload = st.file_uploader("Upload Your Dataset (In CSV Format) here")
    if upload is not None:
        data = pd.read_csv(upload)
        # st.stop()
    else:
        st.warning("Please Upload Dataset")

    # # 3. Show Dataset
    # if upload is not None:
    #     if st.checkbox("Preview Dataset"):
    #         if st.button("Head"):
    #             st.write(data.head())
    #         if st.button("Tail"):
    #             st.write(data.tail())

    # # 4. Check DataType of Each Column
    # if upload is not None:
    #     if st.checkbox("DataType of Each Column"):
    #         st.text("DataTypes")
    #         st.write(data.dtypes)

    # # 5. Find Shape of Our Dataset (Number of Rows And Number of Columns)
    # if upload is not None:
    #     data_shape = st.radio("What Dimension Do You Want To Check?", ('Rows',
    #                                                                    'Columns'))
    #     if data_shape == 'Rows':
    #         st.text("Number of Rows")
    #         st.write(data.shape[0])
    #     if data_shape == 'Columns':
    #         st.text("Number of Columns")
    #         st.write(data.shape[1])

    # # 6. Find Null Values in The Dataset
    # if upload is not None:
    #     test = data.isnull().values.any()
    #     if test == True:
    #         if st.checkbox("Null Values in the dataset"):
    #             sns.heatmap(data.isnull())
    #             st.pyplot()
    #     else:
    #         st.success("There are no Missing Values in the dataset")

    # # 7. Find Duplicate Values in the dataset
    # if upload is not None:
    #     test = data.duplicated().any()
    #     if test == True:
    #         st.warning("This Dataset Contains Some Duplicate Values")
    #         dup = st.selectbox("Do You Want to Remove Duplicate Values?",
    #                            ("Select One", "Yes", "No"))
    #         if dup == "Yes":
    #             data = data.drop_duplicates()
    #             st.text("Duplicate Values are Removed")
    #         if dup == "No":
    #             st.text("Ok No Problem")

    # if st.button('Save DataFrame'):
    #     open('C:/Users/data_streamlit.csv', 'w').write(data.to_csv())
    #     st.text("Saved To local Drive")

    # 8. Get Overall Statistics
    if upload is not None:
        if st.checkbox("Summary of The Dataset"):
            st.write(data.describe(include='all'))

    # 9. Multiple Regression Analysis

    if upload is not None:
        if st.checkbox("Perform Multiple Regression Analysis"):
            st.text("Dependent Variable")
            dependent_var = st.selectbox(
                "Select the dependent variable", data.columns)
            st.text("Independent Variables")
            independent_vars = st.multiselect(
                "Select the independent variables", data.columns)

            if len(independent_vars) > 0 and dependent_var:
                X = data[independent_vars]
                y = data[dependent_var]

                # Drop rows with missing values
                X = X.dropna()
                y = y.loc[X.index]

                X = sm.add_constant(X)  # adding a constant

                model = sm.OLS(y, X).fit()
                predictions = model.predict(X)

                st.text("Model Summary")
                st.write(model.summary())


# conda activate  cvenv309
# streamlit run Econ3333-regression.py
