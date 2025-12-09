import streamlit as st
from sqlalchemy import text
import datetime
import calendar

class Banco_dados():
    def __init__(self):
        cnx = st.connection("2026", type="sql", url = "sqlite:///Database/bd_sec/2026.db")
        
        ano = 2026
        mes = 9
        l = ["","JAN","FEV","MAR","ABR","MAIO","JUN","JUL","AGO","SETE","OUT","NOV","DEZ"]
        
        while mes < 13:
            num_d = calendar.monthrange(ano,mes)[1]
            for dia in range(1,num_d+1 ):
                data = datetime.date(ano,mes,dia)
                dataf = data.strftime("%d/%m/%Y")
                with cnx.session as con:
                    con.execute(
                        text(f"insert into {l[mes]} (Data) VALUES (:Data)"), 
                        params={"Data":dataf})
                    con.commit()
            mes += 1