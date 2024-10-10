import time

import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import paho.mqtt.client as mqtt

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

    chart = st.line_chart(pd.DataFrame(data, columns=['Humidity']))


    def temp_chart():
        new_data = pd.DataFrame(data, columns=['Object Temperature'])
        chart.add_rows(new_data)

    placeholder = st.empty()

    def temp():
        with placeholder.container():
            try:
                val = data.pop()
                st.metric(label="Temperature", value=f"{val}")
            except IndexError:
                pass


    with st.sidebar:
        st.title('🌡️Termonitor')

        mode_list = ["Humidity", "Ambient Temperature", "Object Temperature", "All"]

        selected_mode = st.selectbox('Select a mode', mode_list, index=len(mode_list) - 1)

        year_list = [1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907]

        selected_year = st.selectbox('Select a year', year_list, index=len(year_list) - 1)

        month_list = list(range(1,13))

        selected_month = st.selectbox('Select a month', month_list, index=len(month_list) - 1)

        day_list = list(range(1, days_in_month(selected_month, selected_year)))

        selected_day = st.selectbox('Select a day', day_list)

        real_time_check = st.checkbox("RTM", )


    if real_time_check:
        connect_mqtt()
        while real_time_check:
            temp_chart()
            temp()
            data.clear()
            time.sleep(1)


if __name__ == '__main__':
    main()