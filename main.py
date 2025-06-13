import PIL.Image
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_navigation_bar import st_navbar
import plotly.graph_objects as go
import PIL

lista_anos = [2025]
lista_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO",
    "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
lista_dependencias = ["HTS", "HTO", "ALQQ", "USINA/CICRIN", "FADOR", "CIAFV 01", "CIAFV 02", "CIAFV 03"]

colunas = ["Data","HTS", "HTO", "ALQQ", "USINA/CICRIN", "FADOR", "CIAFV 01", "CIAFV 02", "CIAFV 03"]


class Dashboard():
    def consumo(self,coluna):
        df = pd.DataFrame(self.planilha_medicao, columns=[coluna])
        self.dict_consumo = {coluna:[]}
        try:
            x = 0
            for i in df[coluna]:
                j = df[coluna][x+1] - df[coluna][x]
                self.dict_consumo[coluna].append(float(j))
                x += 1
        except KeyError:
            pass
        return self.dict_consumo
        
    def info_centralizada(self):
        df = pd.DataFrame(self.planilha_medicao)
        lista_somas_consumo = []
        for i in lista_dependencias:
            j = list(df[i])
            lista_sem_nan = list(filter(lambda x: not np.isnan(x), j))
            lista_somas_consumo.append(lista_sem_nan[-1]-lista_sem_nan[0])
        soma = 0
        for x in list(lista_somas_consumo):
            soma += x
        return list(lista_somas_consumo),soma
    def __init__(self):    
        self.titulo_pagina = st.set_page_config(page_title="Dashboard", layout="wide",
            initial_sidebar_state="collapsed")
        
        with st.sidebar:
            st.write("Links Importantes")
            st.page_link("https://atende.cemig.com.br/Login", label="CEMIG Login")
        
        col1, col2, col3 = st.columns([1,2,1],gap="small")
        with col1:
            with st.columns(3)[1]:
                imagem = PIL.Image.open(r"Img/brasao2bfv.PNG")
                novo_tamanho = (77,100)
                st.image(imagem.resize(novo_tamanho))
        with col2:    
            st.header("Dashboard de Controle de Energia", anchor=False)
        self.container = st.container(border=True)
        with self.container:
            col4, col5= st.columns([1,3],gap="small", vertical_alignment="center" )
            with col4:
                self.selecao_opcoes_ano = st.selectbox("Ano",options= lista_anos)
                self.selecao_opcoes_mes = st.selectbox("Mês",options= lista_meses)
                self.selecao_opcoes_dependencia = st.selectbox("Dependência",options= lista_dependencias)
            self.planilha_medicao = pd.read_excel("medicao_energia.xlsx", sheet_name=self.selecao_opcoes_mes)
            with col5:
                try:
                    dados,soma_geral = self.info_centralizada()
                    fig = go.Figure(data=[go.Bar(x=lista_dependencias, y=dados, 
                        marker_color =["red","blue","green","yellow","gray", "orange","white","purple"],
                        text=dados)])
                    fig.update_layout(
                            title=f"Consumo geral: {soma_geral} KWh",
                            yaxis_title="Consumo",
                            height = 300
                            )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.error(f"Provavelmente a planilha do mês de {self.selecao_opcoes_mes} está vazia", width=500)

        self.container1 = st.container()
        with self.container1:
            fig = go.Figure()
            df = pd.DataFrame(self.planilha_medicao)
            del colunas[0]
            for i in colunas:
                fig.add_trace(go.Scatter(x=df["Data"],y=df[i], name=i, mode="markers+lines"))
            fig.update_layout(
                        title=f"Gráfico de medições",
                        yaxis_title="Medição",
                        xaxis_title="Data",
                        xaxis = dict(title="Data",range = [0,31]),
                        hovermode = "x",
                    )
            st.plotly_chart(fig)
        self.container2 = st.container() 
        with self.container2:
            dados1 = self.consumo(self.selecao_opcoes_dependencia)
            df = pd.DataFrame(dados1)
            fig = go.Figure(data=[go.Scatter(x=list(range(0,31,1)),y=df[self.selecao_opcoes_dependencia],mode="markers+lines",
                        marker=dict(size=10, symbol="circle"),
                        line=dict(width=1,color="white"))])     
            fig.update_layout(
                        title=f"Gráfico de Consumo Individualizado: {self.selecao_opcoes_dependencia}",
                        yaxis_title="Consumo",
                        xaxis = dict(title="Data",range = [0,31]),
                        plot_bgcolor = "#3bbef7",
                        hovermode = "x",
                        )
            st.plotly_chart(fig)
            
        

if __name__=="__main__":
    Dashboard()