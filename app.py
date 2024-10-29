import time
from random import random

import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import paho.mqtt.client as mqtt
import requests

from handlers import days_in_month
from mqtt_connection import get_data, connect_mqtt


def main():
    st.set_page_config(
        page_title="Termonitor",
        page_icon="🌡️",
        layout="wide",
        initial_sidebar_state="expanded")

    alt.themes.enable("dark")

    data = get_data()

    chart = st.line_chart(pd.DataFrame({'Environment Temperature' : [], 'Object Temperature' : []}))

    warning = st.empty()

    def temp_chart():
        if len(data) != 0:
            new_data = pd.DataFrame({'Environment Temperature' : [data[0][0]], 'Object Temperature' : [data[0][1]]})
            chart.add_rows(new_data)
        else:
            with warning.container():
                st.warning("Conexão instável ou nula")


    col1, col2 = st.columns(2)
    with col1:
        placeholder_env = st.empty()

    with col2:
        placeholder_obj = st.empty()

    def temp_metric():
        with placeholder_env.container():
            try:
                val = data[0][0]
                st.metric(label="Environment Temperature", value=f"{'{:.2f}'.format(val) + ' °C  '}")
            except IndexError:
                pass

        with placeholder_obj.container():
            try:
                val = data.pop()
                val = val[1]
                st.metric(label="Object Temperature", value=f"{'{:.2f}'.format(val) + ' °C  '}")
            except IndexError:
                pass


    def get_data_static():
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()  # Converte a resposta JSON em um dicionário Python
        else:
            print("Erro ao fazer a requisição:", response.status_code, response.text)
            exit()


    with st.sidebar:
        st.title('🌡️Termonitor')

        year_list = [2024]

        selected_year = st.selectbox('Select a year', year_list, index=len(year_list) - 1)

        month_list = list(range(1,13))

        selected_month = st.selectbox('Select a month', month_list, index=len(month_list) - 1)

        day_list = list(range(1, days_in_month(selected_month, selected_year)))

        selected_day = st.selectbox('Select a day', day_list)

        real_time_check = st.checkbox("RTM", )

    if real_time_check:
        connect_mqtt()
        time.sleep(1)
        while real_time_check:
            temp_chart()
            temp_metric()
            data.clear()
            data = get_data()
            time.sleep(1)
    else:
        url = 'http://localhost:8080'
        data.clear()
        params = {
            'param1': str(selected_day).zfill(2),  # Dia
            'param2': str(selected_month).zfill(2),  # Mês
            'param3': selected_year  # Ano
        }
        data = get_data_static()['data']
        chart.empty()
        st.line_chart(pd.DataFrame(data, columns=['Environment Temperature', 'Object Temperature']))


if __name__ == '__main__':
    main()