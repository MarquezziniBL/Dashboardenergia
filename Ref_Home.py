from scripts import consulta_bd as consbd
from scripts import backend

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
import calendar


locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

class Sidebar():
    # Implementação do CSS
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
    def __init__(self, **kwargs):
        super().__init__()
        with st.sidebar:
            #st.page_link('Home.py', label= "Home")
            st.page_link('pages/lançamentos.py', label= "Lançamentos", disabled= True)
            st.write("Links Importantes")
            st.page_link("https://www.cemig.com.br", label="CEMIG")
            st.page_link("https://atende.cemig.com.br/Login", label="CEMIG Login")

        self.local_css(pathlib.Path("assets//style.css"))    

class Container_titulo():
    
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
    
    def __init__(self, **kwargs):
        super().__init__()
        versao = " Desenvolvedor: 2º Sgt Eng Marquezzini - Versão: 2.0.1.3"
        atualizacoes = """ V2.0.1.3 - 26/02/2026
- Lançamento dos dados de FEV/26"""
        
        with st.container(border=False, key= "container_0"):
                st.markdown("<h1 class = h1_header>Dashboard Controle de Energia</h1>", unsafe_allow_html=True)
    
        with st.container(border=False, key= "container_1"):
            st.text(versao,help=atualizacoes)
        
        self.local_css(pathlib.Path("assets//style.css"))

class Container_principal():
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
    
    def __init__(self, df_dados_bandeiras, df_dados_anos, df_dados_gastomensal):
        super().__init__()
        
        lista_anos,lista_meses, lista_dependencias = backend.Calc().dados_selectbox()
        
        # Container com Selectbox 
        self.container = st.container(border=True, key="container0")
        with self.container:
                with st.container(border=False, key="container0_1"):
                    col0, col1= st.columns([1,3],gap="small", vertical_alignment="center" )
                    with col0:
                        self.selecao_opcoes_ano = st.selectbox("Ano",options= lista_anos,index= lista_anos.index(date.today().year))
                        self.selecao_opcoes_mes = st.selectbox("Mês",options= lista_meses)
                        self.selecao_opcoes_dependencia = st.selectbox("Dependência",options= lista_dependencias)
                    with col1:
                        with st.container(border=False,key="container0_2"):

                            #Variáveis do container
                            indice = list(df_dados_bandeiras[f"{self.selecao_opcoes_ano}"]["MES"]).index(self.selecao_opcoes_mes.upper())
                            soma_consumo_dependencia, soma_consumo_todas_dependencias = backend.Calc().soma_geral_consumo(df_dados_anos,self.selecao_opcoes_ano,self.selecao_opcoes_mes)
                            
                            #Indicação da Bandeira do mês
                            st.write(f"Bandeira para o mês de {self.selecao_opcoes_mes.upper()}: {df_dados_bandeiras[f"{self.selecao_opcoes_ano}"]["BANDEIRA"][indice]} , valor a mais por 100 KWh: {locale.currency(df_dados_bandeiras[f"{self.selecao_opcoes_ano}"]["VALOR"][indice], grouping=True)}")
                             
                           
                            
                            # Plotagem
                            fig = go.Figure(data=[go.Bar(x=lista_dependencias, y=soma_consumo_dependencia, hoverinfo= "text",
                                            marker_color =["pink","red","blue","green","yellow","gray", "orange","white","purple"],
                                            text=soma_consumo_dependencia)])
                            fig.update_layout(
                                    title=f"Consumo geral: {locale.format_string("%.0f",soma_consumo_todas_dependencias, grouping=True)} KWh",
                                    title_x = 0.3,
                                    xaxis_title = "Dependências",
                                    yaxis_title="Consumo",
                                    height = 300
                                    )
                            st.plotly_chart(fig, width="stretch")

                            #Percentual representativo de cada dependência
                            texto = ""  
                            try:
                                for i, dependencia in enumerate(lista_dependencias):
                                    texto += f"{dependencia}: {locale.format_string("%.2f%%",(soma_consumo_dependencia[i]/ soma_consumo_todas_dependencias)*100)}   "
                                st.text(texto)
                            except Exception:
                                st.error(f"Provavelmente a planilha do mês de {self.selecao_opcoes_mes} está vazia", width=500)
        
        # Container para os dados de cada depedência
        self.container1 = st.container(key="container1") 
        with self.container1:
            #Variáveis do container
            dados_diarios_hfp = df_dados_anos[f"{self.selecao_opcoes_ano}"][f"{self.selecao_opcoes_mes}"][f"{self.selecao_opcoes_dependencia}-HFP"]
            dados_diarios_hp = df_dados_anos[f"{self.selecao_opcoes_ano}"][f"{self.selecao_opcoes_mes}"][f"{self.selecao_opcoes_dependencia}-HP"]
            l_data = backend.Calc().mudar_formato_data(df_dados_anos[f"{self.selecao_opcoes_ano}"][f"{self.selecao_opcoes_mes}"]["Data"])

            l_soma_hfp_hp,l_hfp,l_hp = backend.Calc().soma_geral_valor(df_dados_gastomensal,self.selecao_opcoes_ano,self.selecao_opcoes_dependencia)
            soma_diaria_hfp_hp = backend.Calc().soma_diaria_consumo(dados_diarios_hfp,dados_diarios_hp)
            
            
            st.markdown(f"<h3 style='text-align: center'> Dados do(a) {self.selecao_opcoes_dependencia} </h3>",unsafe_allow_html=True)
            
            # Gráfico de Gasto Mensal
            col2,col3 = st.columns([6,2],gap="small", vertical_alignment="center" )
            with col2:
                barra_custo_hfp = go.Bar(x=lista_meses, y=l_hfp, name="HFP", marker_color = "#00a2ff", hoverinfo= "text",
                                                hovertext=[locale.currency(n, grouping=True) for n in l_hfp])
                barra_custo_hp = go.Bar(x=lista_meses, y=l_hp, name = "HP", marker_color = "#ff6600", hoverinfo= "text",
                                                hovertext=[locale.currency(n, grouping=True) for n in l_hp])
                linha_custo_soma = go.Scatter(x=lista_meses, y=l_soma_hfp_hp, name="HFP + HP" ,mode="markers+lines", hoverinfo= "text",
                                marker=dict(size=8, symbol="circle", color = "red"), line=dict(width=3,color="#f15454", shape = "spline"), hovertext=[locale.currency(n, grouping=True) for n in l_soma_hfp_hp])
                self.fig_custo = go.Figure(data=[barra_custo_hfp,barra_custo_hp,linha_custo_soma])
                        
                self.fig_custo.update_layout(
                                        title={"text":f"Custo mensal",
                                            "x":0.1,"y":0.9,"xanchor" : "left", "yanchor":"top"},
                                        yaxis = dict(title="Custo (R$)"),
                                        xaxis = dict(title="Meses"),
                                        plot_bgcolor = "#b6d5ee",
                                        paper_bgcolor = "#006494",
                                        hovermode = "x unified",
                                        )
                st.plotly_chart(self.fig_custo, width="stretch")
                    
            with col3:
                pizza_custo = go.Pie(labels=["",""],values=[sum(l_hfp), sum(l_hp)], showlegend=False,
                                    title="Percentual HFP x HP", hoverinfo= "text",
                                    hovertext=[(locale.currency(sum(l_hfp), grouping=True)) , (locale.currency(sum(l_hp), grouping=True))])
                fig_pizza_custo = go.Figure(data=[pizza_custo])
                fig_pizza_custo.update_traces(marker=dict(colors=["#00a2ff","#ff6600"],
                            line = dict(color = "#FFFFFF", width=1)), textfont_size = 12)
                fig_pizza_custo.update_layout(
                            paper_bgcolor = "#006494",
                            hovermode = "x unified",
                        )
                st.plotly_chart(fig_pizza_custo)

            col4,col5 = st.columns([6,2],gap="small", vertical_alignment="center" )
            with col4:
                barra_consumo_hfp = go.Bar(x=l_data, y=dados_diarios_hfp, name="HFP", marker_color = "#00a2ff", hoverinfo= "text", 
                            hovertext=[locale.format_string("%.0f",n, grouping=True) for n in dados_diarios_hfp])
                barra_consumo_hp = go.Bar(x=l_data, y=dados_diarios_hp, name = "HP", marker_color = "#ff6600",  hoverinfo= "text",
                            hovertext=[locale.format_string("%.0f",n, grouping=True) for n in dados_diarios_hp])
                linha_consumo_soma = go.Scatter(x=l_data, y=soma_diaria_hfp_hp, name="HFP + HP" ,mode="markers+lines", hoverinfo= "text", 
                            hovertext=[locale.format_string("%.0f",n, grouping=True) for n in soma_diaria_hfp_hp],
                            marker=dict(size=6, symbol="circle", color = "red"), line=dict(width=3,color= "red"))
                fig_consumo = go.Figure(data=[barra_consumo_hfp,barra_consumo_hp,linha_consumo_soma])
                fig_consumo.update_layout(
                                    title={"text":f"Consumo diário de {str(self.selecao_opcoes_mes).lower()}",
                                        "x":0.1,"y":0.9,"xanchor" : "left", "yanchor":"top"},
                                    yaxis = dict(title="Consumo", tickformat=',.0f'),
                                    xaxis = dict(title="Data"),
                                    plot_bgcolor = "#b6d5ee",
                                    paper_bgcolor = "#006494",
                                    hovermode = "x unified",
                                    )
                st.plotly_chart(fig_consumo, width="stretch")

            with col5:
                pizza_consumo = go.Pie(labels=["",""],values=[sum(dados_diarios_hfp), sum(dados_diarios_hp)], showlegend=False,
                                    title="Percentual HFP x HP", hoverinfo= "text",
                                    hovertext=[(locale.format_string("%.0f",sum(dados_diarios_hfp), grouping=True)) , (locale.format_string("%.0f",sum(dados_diarios_hp), grouping=True))])
                fig_pizza_consumo = go.Figure(data=[pizza_consumo])
                fig_pizza_consumo.update_traces(marker=dict(colors=["#00a2ff","#ff6600"],
                            line = dict(color = "#FFFFFF", width=1)), textfont_size = 12)
                fig_pizza_consumo.update_layout(
                            paper_bgcolor = "#006494",
                        )
                st.plotly_chart(fig_pizza_consumo, key="pizza_consumo")
            
            self.container1_1 = st.container(key="container1_1", border=True)
            with self.container1_1:
                col6,col7 = st.columns([1,9],gap="small", vertical_alignment="center" )
                with col6:
                    self.selecao_dias_semana = st.selectbox("Dia da Semana",options= l_data,key="dias_semana")
                
                with col7:
                    #Variáveis do container
                    atividade = backend.Calc().atividades_mes_atual(l_data.index(self.selecao_dias_semana),df_dados_anos[f"{self.selecao_opcoes_ano}"][f"{self.selecao_opcoes_mes}"]["ATIVIDADES"])
                    st.markdown(f'<p style="text-align: left;">{atividade}</p>', unsafe_allow_html=True)
            
            self.container1_2 = st.container(key="container1_2")
            with self.container1_2:
                    with st.expander(label="Análise",expanded=False):
                        st.markdown(f'<p style="text-align: center;">{self.selecao_opcoes_dependencia}</p>', unsafe_allow_html=True)
        self.local_css(pathlib.Path("assets//style_copy.css"))
class App():
    # Implementação do CSS
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
    def __init__(self):
        super().__init__()
        

        df_dados_anos = {}
        df_dados_bandeiras = {}
        df_dados_gastomensal = {}

        #try:
        df_dados_consumo = backend.Calc().dados_consumo()
        df_dados_bandeiras = backend.Calc().dados_bandeiras()
        df_dados_gastomensal = backend.Calc().dados_gastomensal()
        #except Exception:
            #st.error("Erro ao conectar com Banco de Dados")
        
        self.titulo_pagina = st.set_page_config(page_title="Dashboard", layout="wide",
            initial_sidebar_state="collapsed")
        
        #Tirar anchor de elementos
        st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

        Sidebar()
        Container_titulo()
        Container_principal(df_dados_bandeiras, df_dados_consumo, df_dados_gastomensal)
        self.local_css(pathlib.Path("assets//style_copy.css"))
if __name__ == "__main__":
    App()