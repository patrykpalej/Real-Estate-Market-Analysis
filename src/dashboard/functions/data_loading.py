import pandas as pd
import streamlit as st
import multiprocessing
import concurrent.futures

from dashboard.functions.lots import preprocess_lots
from dashboard.functions.houses import preprocess_houses
from dashboard.functions.apartments import preprocess_apartments

from utils.storage import (get_credentials, generate_psql_connection_string,
                           read_from_db)


pd.options.mode.chained_assignment = None

preprocess_funcs_dict = {"lots": preprocess_lots, "houses": preprocess_houses,
                         "apartments": preprocess_apartments}

sql_queries_dict = {"lots": "SELECT * FROM otodom_lots",
                    "houses": "SELECT * FROM otodom_houses",
                    "apartments": "SELECT * FROM otodom_apartments"}

connection_string = generate_psql_connection_string(*get_credentials())


def fetch_and_preprocess(property_type):
    preprocess_func = preprocess_funcs_dict[property_type]
    sql_query = sql_queries_dict[property_type]

    return (property_type,
            preprocess_func(read_from_db(sql_query, connection_string)))


def load_data_concurrently(threading):
    if threading:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_and_preprocess, prop)
                       for prop in ["lots", "houses", "apartments"]]
            concurrent.futures.wait(futures)

            for future in futures:
                result = future.result()
                st.session_state.data[result[0]] = result[1]
    else:
        with multiprocessing.Pool() as pool:
            results_raw = pool.starmap(
                fetch_and_preprocess,
                [(prop,) for prop in ["lots", "houses", "apartments"]])

            for result in results_raw:
                st.session_state.data[result[0]] = result[1]