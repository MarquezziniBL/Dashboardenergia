import PIL.Image
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import PIL
import google.generativeai as genai
from datetime import date


genai.configure(api_key="")
modelo_ai = genai.GenerativeModel('gemini-1.5-flash')

versao = " Versão: 1.3.10"

lista_anos = [2024,2025]

lista_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO",
    "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
lista_dependencias = ["SEDE","HTS", "HTO", "ALQQ", "USINA/CICRIN", "FADOR", "CIAFV 01", "CIAFV 02", "CIAFV 03"]
dict_dias_semana = {"0":"Seg","1":"Ter","2":"Qua","3":"Qui","4":"Sex","5":"Sáb","6":"Dom"}
colunas = ["Data","SEDE","HTS", "HTO", "ALQQ", "USINA/CICRIN", "FADOR", "CIAFV 01", "CIAFV 02", "CIAFV 03"]

class Dashboard():
    def dias_semana (self,dicicionario):
            l_dias_semana = []
            try:
                for i in dicicionario:
                    data_editar = str(i).replace(" 00:00:00","")     
                    l_data= data_editar.split(sep ="-",maxsplit=3)
                    ano,mes,dia = l_data[0],l_data[len(l_data)//2],l_data[-1]
                    data = date(int(ano),int(mes),int(dia))
                    num = str(data.weekday())
                    edit = dict_dias_semana[num]
                    l_dias_semana.append( edit + "," + dia)
            except ValueError:
                pass
            return l_dias_semana
        
    def consumo(self,situacao,coluna):
        df = pd.DataFrame(self.planilha_medicao, columns=[coluna+"-HFP", coluna+"-HP"])
        if situacao == "analise":
            mes_posicao = lista_meses.index(self.selecao_opcoes_mes)
            self.planilha_medicao_analise = pd.read_excel(f"medicao_energia_{self.selecao_opcoes_ano}.xlsx", sheet_name=lista_meses[mes_posicao-1])
            try:    
                if self.selecao_opcoes_mes == "JANEIRO":
                    self.planilha_medicao_analise = pd.read_excel(f"medicao_energia_{self.selecao_opcoes_ano-1}.xlsx", sheet_name=lista_meses[mes_posicao-1])
            except FileNotFoundError:
                self.container5.write(f"Não encontrado arquivo para o ano de {self.selecao_opcoes_ano-1}")
                st.session_state["test"] = False
            df = pd.DataFrame(self.planilha_medicao_analise, columns=[coluna+"-HFP", coluna+"-HP"])
        
        self.lista_hfp = []
        self.lista_hp = []
        self.lista_soma = []
        
        for i,j in zip(df[coluna+"-HFP"], df[coluna+"-HP"]):
            if  i < 0:
                i = 0
            if j < 0:
                j = 0
            self.lista_hfp.append(float(f"{i:.0f}"))
            self.lista_hp.append(float(f"{j:.0f}"))
            self.lista_soma.append(float(f"{i:.0f}")+float(f"{j:.0f}"))

        return list(filter(lambda x: not np.isnan(x) and x > 0, self.lista_hfp)), list(filter(lambda x: not np.isnan(x) and x > 0, self.lista_hp)), list(filter(lambda x: not np.isnan(x) and x > 0, self.lista_soma))   
    def analise_gemma (self):
        l_hfp_mes_ant,l_hp_mes_ant,l_soma_mes_ant = self.consumo("analise",self.selecao_opcoes_dependencia)
        try:
            total_mes_atual = float(sum(self.l_soma))
            total_mes_ant = float(sum(l_soma_mes_ant))
            variacao = 0
            if total_mes_ant == 0:
                variacao = 0
            else:
                variacao = ((total_mes_atual/total_mes_ant)-1)*100
            
            
            hp_mes_atual = (f"{float(sum(self.l_hp)):.0f}").replace(".",",")
            hfp_mes_atual = (f"{float(sum(self.l_hfp)):.0f}").replace(".",",")
            media_mensal_mes_atual = (f"{float(sum((self.l_soma))/len(self.l_soma)):.0f}").replace(".",",")
            valor_max_total_mes_atual = (f"{max(self.l_soma):.0f}").replace(".",",")
            valor_min_total_mes_atual = (f"{min(self.l_soma):.0f}").replace(".",",")
            
            tma = (f"{(total_mes_atual):.0f}").replace(".",",")
            tmant = (f"{(total_mes_ant):.0f}").replace(".",",")
            vari = (f"{(variacao):.0f}").replace(".",",")
            if st.session_state["check"]:
                st.session_state["test"] = True
                l_analises = [
                    f"Análise de consumo da(o) {self.selecao_opcoes_dependencia}",
                    "<div style='text-align: center'> Mês Atual </div>"," ",
                    f"Total:  {tma} KWh -  dividido em HP = {hp_mes_atual} e HFP = {hfp_mes_atual}",
                    f"Maior Consumo:  {valor_max_total_mes_atual} KWh e Menor Consumo: {valor_min_total_mes_atual} KWh",
                    f"Média Mensal:  {media_mensal_mes_atual} KWh",
                    "<div style='text-align: center'> Comparativos </div>"," ",
                    f"Total:",
                    f"  1) Mês atual =  {tma} KWh -  Mês anterior = {tmant}, Variação de {vari}%"
                    ]
                
                for i in l_analises:
                    self.container5.markdown(i,unsafe_allow_html=True)
            else:
                st.session_state["test"] = False
                self.container5.write()
        except ZeroDivisionError:
                self.container
    def info_centralizada(self):
        df = pd.DataFrame(self.planilha_medicao)
        lista_somas_consumo = []
        colunas.remove("Data")
        for i in colunas:
            x = df[i+"-HP"]
            y = df[i+"-HFP"]
            res = sum(filter(lambda x: not np.isnan(x) and x >= 0, x))+sum(filter(lambda x: not np.isnan(x) and x >= 0, y))
            lista_somas_consumo.append(float(f"{res:.0f}"))

        
        soma_total = 0
        for x in list(lista_somas_consumo):
            soma_total += x
        
        return lista_somas_consumo, soma_total

    def __init__(self):    
        self.titulo_pagina = st.set_page_config(page_title="Dashboard", layout="wide",
            initial_sidebar_state="collapsed")
        
        with st.sidebar:
            st.write("Links Importantes")
            st.page_link("https://www.cemig.com.br", label="CEMIG")
            st.page_link("https://atende.cemig.com.br/Login", label="CEMIG Login")
        
        col1, col2, col3 = st.columns([1,2,1],gap="small")
        with col1:
            with st.columns(3)[1]:
                imagem = PIL.Image.open(r"Img/brasao2bfv.PNG")
                novo_tamanho = (77,100)
                st.image(imagem.resize(novo_tamanho))
        with col2:    
            st.header("Dashboard de Controle de Energia", anchor=False)
            col4, col5, col6 = st.columns([1,2,1],gap="small")
            with col5:
                st.write(versao)
        
        self.container = st.container(border=True)
        with self.container:
            col7, col8= st.columns([1,3],gap="small", vertical_alignment="center" )
            with col7:
                self.selecao_opcoes_ano = st.selectbox("Ano",options= lista_anos)
                self.selecao_opcoes_mes = st.selectbox("Mês",options= lista_meses)
                self.selecao_opcoes_dependencia = st.selectbox("Dependência",options= lista_dependencias)
            self.planilha_medicao = pd.read_excel(f"medicao_energia_{self.selecao_opcoes_ano}.xlsx", sheet_name=self.selecao_opcoes_mes)
            df0 = pd.DataFrame(self.planilha_medicao).reindex(columns=['Bandeira','Valor'])
            with col8:
                col9, col10, col11= st.columns([1,5,1],gap="small", vertical_alignment="center" )
                with col10:
                    st.write(f"Bandeira para o mês de {self.selecao_opcoes_mes}:  {df0['Bandeira'][0]}, valor a mais por 100 KWh : R$ {str(df0["Valor"][0]).replace(".",",")}")
                try:
                    dados,soma_geral = self.info_centralizada()
                    fig = go.Figure(data=[go.Bar(x=lista_dependencias, y=dados, 
                        marker_color =["pink","red","blue","green","yellow","gray", "orange","white","purple"],
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
            lista_x = self.dias_semana(df["Data"])
            del colunas[0]
            for i in colunas:
                fig.add_trace(go.Scatter(x=lista_x,y=df[i], name=i, mode="markers+lines"))
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
            self.l_hfp,self.l_hp,self.l_soma = self.consumo("normal",self.selecao_opcoes_dependencia)
            col12,col13 = st.columns([6,1],gap="small", vertical_alignment="center" )
            
            with col12:
                barra1 = go.Bar(x=lista_x, y=self.l_hfp, name="HFP", marker_color = "#00a2ff")
                barra2 = go.Bar(x=lista_x, y=self.l_hp, name = "HP", marker_color = "#ff6600")
                linha_soma = go.Scatter(x=lista_x, y=self.l_soma, name="HFP + HP" ,mode="markers+lines", 
                    marker=dict(size=6, symbol="circle"), line=dict(width=3,color="red"))
                self.fig2 = go.Figure(data=[barra1,barra2,linha_soma])
                self.fig2.update_layout(
                            title=f"Gráfico de Consumo Individualizado: {self.selecao_opcoes_dependencia}",
                            yaxis = dict(title="Consumo", tickformat='.0f'),
                            xaxis = dict(title="Data"),
                            plot_bgcolor = "#b6d5ee",
                            hovermode = "x",
                            )
                st.plotly_chart(self.fig2)

            with col13:
                pizza1 = go.Pie(labels=["",""],values=[sum(self.l_hfp), sum(self.l_hp)], showlegend=False,
                            title="Percentual HFP x HP")
                fig_pizza1 = go.Figure(data=[pizza1])
                fig_pizza1.update_traces(marker=dict(colors=["#00a2ff","#ff6600"],
                    line = dict(color = "#13293D", width=2)), textfont_size = 16)
                
                st.plotly_chart(fig_pizza1)
            
            self.container4 = st.container()
            with self.container4:
                if "test" not in st.session_state:
                    st.session_state["test"] = False
                self.analise_cons_ind = st.checkbox("Análise", value=st.session_state["test"],
                    key="check", on_change= self.analise_gemma)
            self.container5 = st.container() 
            
            with self.container5:
                st.write()
if __name__=="__main__":
    Dashboard()