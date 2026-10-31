import streamlit as st
from sqlalchemy import text
import datetime
import calendar


class Banco_dados():
    def select_dados(self,tabela):
        dados = self.cnx.query(f"select * from '{tabela}'")
        return dados
    
    def __init__(self,bd):
        self.cnx = st.connection(f"{bd}", type="sql", url = f"sqlite:///database/bd_sec/{bd}.db")


