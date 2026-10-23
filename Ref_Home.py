from scripts import bdlanc as bdl

import PIL.Image
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from datetime import date
import pathlib
import locale
import base64
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

class Container_titulo():
    
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
    
    def __init__(self, master, **kwargs):
        super().__init__()
        versao = " Desenvolvedor: 2º Sgt Eng Marquezzini - Versão: 2.0.1.3"
        atualizacoes = """ V2.0.1.3 - 26/02/2026
- Lançamento dos dados de FEV/26"""
        
        with st.container(border=False, key= "container_0"):
                st.markdown("<h1 class = h1_header>Dashboard Controle de Energia</h1>", unsafe_allow_html=True)
    
        with st.container(border=False, key= "container_1"):
            st.text(versao,help=atualizacoes)
        
        self.local_css(pathlib.Path("assets//style.css"))

class Sidebar():
    # Implementação do CSS
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
    def __init__(self, master, **kwargs):
        super().__init__()
        with st.sidebar:
            #st.page_link('Home.py', label= "Home")
            st.page_link('pages/lançamentos.py', label= "Lançamentos", disabled= True)
            st.write("Links Importantes")
            st.page_link("https://www.cemig.com.br", label="CEMIG")
            st.page_link("https://atende.cemig.com.br/Login", label="CEMIG Login")

        self.local_css(pathlib.Path("assets//style.css"))    

class App():
    # Implementação do CSS
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
    def __init__(self):
        super().__init__()
        self.titulo_pagina = st.set_page_config(page_title="Dashboard", layout="wide",
            initial_sidebar_state="collapsed")
         

        #Tirar anchor de elementos
        st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

        Sidebar(master = self)
        Container_titulo(master =self)
        
        self.local_css(pathlib.Path("assets//style.css"))
if __name__ == "__main__":
    App()