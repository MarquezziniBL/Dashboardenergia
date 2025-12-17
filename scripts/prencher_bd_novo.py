import streamlit as st
from sqlalchemy import text
import sqlitecloud as sqlc
import datetime
import calendar

class Banco_dados():
    def __init__(self):
        lista_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO",
    "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
        cnx = sqlc.connect("sqlitecloud://cavxhyjgvk.g5.sqlite.cloud:8860/2025.db?apikey=kprHqeImbmp0cV27OLeGB4eLhOU7P3e7PBb4z7kDFbY")
        

        dados = cnx.execute(f"select * from NOVEMBRO")
        cnx.commit()
        print(dados.fetchall())

Banco_dados()           