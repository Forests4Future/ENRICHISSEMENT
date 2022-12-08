# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

df = pd.read_csv('data_especes_sodefor.csv',sep=";")
AgGrid(df)
