# Core Pkgs
import streamlit as st
import scipy
import scipy.stats

# EDA Pkgs
import pandas as pd
import numpy as np

# Data Viz Pkg
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)
#st.dataframe(df.head())

class UiRender():

    def __init__(self):
        self.version = 1

    def nullstats(df) -> str:
        out = ""
        for column in df.columns:
            null_rate = df[column].isna().sum() / len(df) * 100
            if null_rate > 0:
                out +="{} null rate: {}%".format(column, round(null_rate, 2))
            else:
                out += "{} null rate: 0%".format(column)
        return out

    def summary(self,st,df):
        st.write(df.describe())

    def render(self):
        Options = ["Exploratory Analysis", "Univariate/Bivariate Analysis"]
        choice = st.sidebar.selectbox("Select the analysis", Options)
        st.subheader("Exploratory Data Analysis")
        data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])

        if choice == 'Exploratory Analysis':
            if data is not None:

                df = pd.read_csv(data)
                st.write('The Data is as follows \n' , df.head())

                checkboxes = {}
                checkboxes['Shape'] = st.sidebar.checkbox("Show Shape")
                checkboxes['Columns'] = st.sidebar.checkbox("Show Columns")
                checkboxes['Summary'] = st.sidebar.checkbox("Summary")
                checkboxes['Show Selected Columns'] = st.sidebar.checkbox("Show Selected Columns")
                checkboxes['Show Value Counts'] = st.sidebar.checkbox("Show Value Counts")
                checkboxes['Correlation Plot(Matplotlib)'] = st.sidebar.checkbox("Correlation Plot(Matplotlib)")
                checkboxes['Correlation Plot(Seaborn)'] = st.sidebar.checkbox("Correlation Plot(Seaborn)")
                checkboxes['Pie Plot'] = st.sidebar.checkbox("Pie Plot")

                all_columns = df.columns.to_list()
                if checkboxes['Shape']:
                    st.write(df.shape)

                if checkboxes['Columns']:
                    st.write(all_columns)

                if checkboxes['Summary']:
                    self.summary(st,df)

                if checkboxes['Show Selected Columns']:
                    selected_columns = st.multiselect("Select Columns for viewing", all_columns)
                    new_df = df[selected_columns]
                    st.dataframe(new_df)

                if checkboxes['Show Value Counts']:
                    selected_columns = st.selectbox("Select Columns for viewing", all_columns)
                    location = df.columns.get_loc(selected_columns)
                    st.write(df.iloc[:, int(location)].value_counts())

                if checkboxes['Correlation Plot(Matplotlib)']:
                    plt.matshow(df.corr())
                    st.pyplot()

                if checkboxes['Correlation Plot(Seaborn)']:
                    st.write(sns.heatmap(df.corr(), annot=True))
                    st.pyplot()

                if checkboxes['Pie Plot']:
                    all_columns = df.columns.to_list()
                    column_to_plot = st.selectbox("Select 1 Column", all_columns)
                    pie_plot = df[column_to_plot].value_counts().plot.pie(autopct="%1.1f%%")
                    st.write(pie_plot)
                    st.pyplot()

        elif choice == 'Univariate/Bivariate Analysis':
            if data is not None:
                df = pd.read_csv(data)
                st.dataframe(df.head())
                all_columns_names = df.columns.tolist()

                type_of_plot = st.sidebar.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
                selected_columns_names = st.sidebar.multiselect("Select Columns To Plot", all_columns_names)

                if st.sidebar.button("Generate Plot"):
                    st.sidebar.success("Generating Customizable Plot of {} for {}".format(type_of_plot, selected_columns_names))

                    # Plot By Streamlit
                    if type_of_plot == 'area':
                        cust_data = df[selected_columns_names]
                        st.area_chart(cust_data)

                    elif type_of_plot == 'bar':
                        cust_data = df[selected_columns_names]
                        st.bar_chart(cust_data)

                    elif type_of_plot == 'line':
                        cust_data = df[selected_columns_names]
                        st.line_chart(cust_data)

                    # Custom Plot
                    elif type_of_plot:
                        cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
                        st.write(cust_plot)
                        st.pyplot()

"""
# select = st.sidebar.text_input('Select rows:Select Columns', '0:,5:')
# indices = str(select).split(',')
# rows = str(indices[0]).split(':')
# columns = str(indices[1]).split(':')
"""