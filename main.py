import PIL.Image
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import PIL
from datetime import date
import pathlib
import locale

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

versao = " Versão: 1.4.17"

lista_anos = [2024,2025]

lista_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO",
    "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
lista_dependencias = ["SEDE","HTS", "HTO", "ALQQ", "USINA/CICRIN", "FADOR", "CIAFV 01"]
dict_dias_semana = {"0":"Seg","1":"Ter","2":"Qua","3":"Qui","4":"Sex","5":"Sáb","6":"Dom"}
colunas = ["Data","SEDE","HTS", "HTO", "ALQQ", "USINA/CICRIN", "FADOR", "CIAFV 01"]

class Dashboard():
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
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
    def consumo_total_dependecias(self,coluna):
        lista_soma = []
        self.planilha_consumo_total = pd.read_excel(f"medicao_energia_{self.selecao_opcoes_ano}.xlsx", sheet_name=lista_meses)
        for i in lista_meses:
            total = sum(filter(lambda x: not np.isnan(x),self.planilha_consumo_total[i][coluna+"-HFP"])) + sum(filter(lambda x: not np.isnan(x),self.planilha_consumo_total[i][coluna+"-HP"]))
            lista_soma.append(float(f"{total:.0f}"))
        return lista_soma
    def consumo(self,situacao,coluna):
        df = pd.DataFrame(self.planilha_medicao, columns=[coluna+"-HFP", coluna+"-HP"])
        
        if situacao == "analise":
            mes_posicao = lista_meses.index(self.selecao_opcoes_mes)
            self.planilha_medicao_analise = pd.read_excel(f"medicao_energia_{self.selecao_opcoes_ano}.xlsx", sheet_name=lista_meses[mes_posicao-1])
            try:    
                if self.selecao_opcoes_mes == "JANEIRO":
                    self.planilha_medicao_analise = pd.read_excel(f"medicao_energia_{self.selecao_opcoes_ano-1}.xlsx", sheet_name=lista_meses[mes_posicao-1])
            except FileNotFoundError:
                self.planilha_medicao_analise = self.planilha_medicao
                self.container3_2.error(f"Não existe arquivo para {self.selecao_opcoes_ano-1}", width=500)
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
    def valores(self,coluna):
        l_gasto_total = []
        l_gasto_mensal_hfp = []
        l_gasto_mensal_hp = []
        l_gasto_soma = []
        self.planilha_gasto = pd.read_excel(f"medicao_energia_{self.selecao_opcoes_ano}.xlsx", sheet_name="GASTOMENSAL")
        df1 = pd.DataFrame(self.planilha_gasto, columns=[coluna+"-HFP", coluna+"-HP"])
        
        dict_meses = {"JANEIRO":[df1[coluna+"-HFP"][0],df1[coluna+"-HP"][0]], "FEVEREIRO":[df1[coluna+"-HFP"][1],df1[coluna+"-HP"][1]],
            "MARÇO":[df1[coluna+"-HFP"][2],df1[coluna+"-HP"][2]], "ABRIL":[df1[coluna+"-HFP"][3],df1[coluna+"-HP"][3]],
            "MAIO":[df1[coluna+"-HFP"][4],df1[coluna+"-HP"][4]], "JUNHO":[df1[coluna+"-HFP"][5],df1[coluna+"-HP"][5]],
            "JULHO":[df1[coluna+"-HFP"][6],df1[coluna+"-HP"][6]], "AGOSTO":[df1[coluna+"-HFP"][7],df1[coluna+"-HP"][7]], 
            "SETEMBRO":[df1[coluna+"-HFP"][8],df1[coluna+"-HP"][8]],"OUTUBRO":[df1[coluna+"-HFP"][9],df1[coluna+"-HP"][9]], 
            "NOVEMBRO":[df1[coluna+"-HFP"][10],df1[coluna+"-HP"][10]], "DEZEMBRO":[df1[coluna+"-HFP"][11],df1[coluna+"-HP"][11]]}
        for i in dict_meses[self.selecao_opcoes_mes]:
            if np.isnan(i):
                i = 0
            l_gasto_total.append(i)
        for i in dict_meses.keys():
            if np.isnan(dict_meses[i][0]):
                dict_meses[i][0] = 0
            if np.isnan(dict_meses[i][1]):
                dict_meses[i][1] = 0
            l_gasto_mensal_hfp.append(dict_meses[i][0])
            l_gasto_mensal_hp.append(dict_meses[i][1])
            l_gasto_soma.append(dict_meses[i][0]+dict_meses[i][1])
        
        return list(filter(lambda x: not np.isnan(x) and x > 0,l_gasto_total)), list(filter(lambda x: not np.isnan(x) and x > 0,l_gasto_mensal_hfp)), list(filter(lambda x: not np.isnan(x) and x > 0,l_gasto_mensal_hp)), list(filter(lambda x: not np.isnan(x) and x > 0,l_gasto_soma))
    def analise_gemma (self):
        l_hfp_mes_ant,l_hp_mes_ant,l_soma_mes_ant = self.consumo("analise",self.selecao_opcoes_dependencia)
        lista_valores, lista_valores_hfp, lista_valores_hp,lista_valores_soma = self.valores(self.selecao_opcoes_dependencia)
        
        try:
            total_mes_atual = float(sum(self.l_consumo_soma))
            total_mes_ant = float(sum(l_soma_mes_ant))
            variacao = 0
            if total_mes_ant == 0:
                variacao = 0
            else:
                variacao = ((total_mes_atual/total_mes_ant)-1)*100
            
            hp_mes_atual = locale.format_string("%.0f",float(sum(self.l_hp)), grouping=True)
            hfp_mes_atual = locale.format_string("%.0f",float(sum(self.l_hfp)), grouping=True)
            v_hfp_mes_atual = locale.currency(float(self.l_custo[0]), grouping=True)
            v_hp_mes_atual = locale.currency(float(self.l_custo[1]), grouping=True)
            media_mensal_mes_atual = locale.format_string("%.0f",float(sum((self.l_consumo_soma))/len(self.l_consumo_soma)), grouping=True)
            valor_max_total_mes_atual = locale.format_string("%.0f",float(max(self.l_consumo_soma)), grouping=True)
            valor_min_total_mes_atual = locale.format_string("%.0f",float(min(self.l_consumo_soma)), grouping=True)
            
            tcma = locale.format_string("%.0f",total_mes_atual, grouping=True)
            tcmant = locale.format_string("%.0f",total_mes_ant, grouping=True)
            tvma = locale.currency(sum(self.l_custo), grouping=True)
            vari = locale.format_string("%.0f%%",variacao, grouping=True)
            with self.container3_2:
                    self.container3_2_1 = st.container(key="container_tres_dois_um") 
                    with self.container3_2_1:
                        st.title(f" Análise de dados da(o) {self.selecao_opcoes_dependencia}",anchor=False)
                        st.markdown(" <div style='text-align: center'> Mês Atual </div>",unsafe_allow_html=True)
                    self.col16,self.col17 = st.columns([1,1],gap="small", vertical_alignment="top" , border=True)
                    with self.col16:
                        st.text("Consumo")
                        st.text(f" Total:  {tcma} KWh -  dividido em HFP = {hfp_mes_atual} KWh e HP = {hp_mes_atual} KWh")
                        st.text(f" Maior Consumo:  {valor_max_total_mes_atual} KWh e Menor Consumo: {valor_min_total_mes_atual} KWh")
                        st.text(f" Média Mensal:  {media_mensal_mes_atual} KWh")
                    with self.col17:
                        st.text("Custo")
                        st.text(f"Total: {tvma} - dividido em HFP = {v_hfp_mes_atual}  e HP =  {v_hp_mes_atual}") 
                    self.container3_2_2 = st.container(key="container_tres_dois_dois", border=True) 
                    with self.container3_2_2:
                        st.markdown(" <div style='text-align: center'> Comparativos </div>",unsafe_allow_html=True)
                        st.text("Total")
                        st.text(f"  1) Mês atual =  {tcma} KWh -  Mês anterior = {tcmant} KWh, Variação de {vari}")
                    st.button("Fechar", on_click= lambda: self.container3_2.empty())
        except ZeroDivisionError:
                self.container3_2.error(f"Dados para o mês zerados", width=500)
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
        
        self.container = st.container(border=True, key="container")
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
                    st.write(f"Bandeira para o mês de {self.selecao_opcoes_mes}:  {df0['Bandeira'][0]}, valor a mais por 100 KWh : {locale.currency(df0["Valor"][0], grouping=True)}")
                try:
                    dados,soma_geral = self.info_centralizada()
                    fig = go.Figure(data=[go.Bar(x=lista_dependencias, y=dados, 
                        marker_color =["pink","red","blue","green","yellow","gray", "orange","white","purple"],
                        text=dados)])
                    fig.update_layout(
                            title=f"Consumo geral: {locale.format_string("%.0f",soma_geral, grouping=True)} KWh",
                            yaxis_title="Consumo",
                            height = 300
                            )
                    st.plotly_chart(fig, use_container_width=True)
                    self.container1 = st.container(key="container_um")
                    with self.container1:
                        st.text(f"Sede: {locale.format_string("%.2f%%",(dados[0]/soma_geral)*100)}    HTS: {locale.format_string("%.2f%%",(dados[1]/soma_geral)*100)}    HTO: {locale.format_string("%.2f%%",(dados[2]/soma_geral)*100)}    ALQQ: {locale.format_string("%.2f%%",(dados[3]/soma_geral)*100)}    USINA/CICRIN: {locale.format_string("%.2f%%",(dados[4]/soma_geral)*100)}    FADOR: {locale.format_string("%.2f%%",(dados[5]/soma_geral)*100)}    CIAFV 01: {locale.format_string("%.2f%%",(dados[6]/soma_geral)*100)}")
                except Exception:
                    st.error(f"Provavelmente a planilha do mês de {self.selecao_opcoes_mes} está vazia", width=500)

        self.container2 = st.container(key="container_dois")
        with self.container2:
            dict_dependencias = {}
            for i in lista_dependencias:
                z = self.consumo_total_dependecias(i)
                dict_dependencias[i] = z
            fig1 = go.Figure()
            for i in lista_dependencias:
                fig1.add_trace(go.Scatter(x=lista_meses,y=dict_dependencias[i], name=i, mode="markers", marker = dict(size=20)))
            fig1.update_layout(
                            title={"text":"Consumo anual das dependências","x":0.5,"y":0.9,"xanchor" : "center", "yanchor":"top"},
                            yaxis=dict(title = "Consumo", tickformat = ',.0f'),
                            xaxis_title="Data",
                            xaxis = dict(title="Meses"),
    
                            hovermode = "x"
                        )
            st.plotly_chart(fig1, use_container_width=True)
        self.container3 = st.container(key="container_tres") 
        with self.container3:
            df2 = pd.DataFrame(self.planilha_medicao)
            lista_x = self.dias_semana(df2["Data"])
            self.l_custo,self.l_custo_hfp,self.l_custo_hp, self.l_custo_soma = self.valores(self.selecao_opcoes_dependencia)
            self.l_hfp,self.l_hp,self.l_consumo_soma = self.consumo("normal",self.selecao_opcoes_dependencia)
            
            st.markdown(f"<h3 style='text-align: center'> Dados do(a) {self.selecao_opcoes_dependencia} </h3>",unsafe_allow_html=True)
            
            
            col12,col13 = st.columns([6,1],gap="small", vertical_alignment="center" )
            with col12:
                barra_custo_hfp = go.Bar(x=lista_meses, y=self.l_custo_hfp, name="HFP", marker_color = "#00a2ff")
                barra_custo_hp = go.Bar(x=lista_meses, y=self.l_custo_hp, name = "HP", marker_color = "#ff6600")
                linha_custo_soma = go.Scatter(x=lista_meses, y=self.l_custo_soma, name="HFP + HP" ,mode="markers+lines", 
                        marker=dict(size=6, symbol="circle"), line=dict(width=3,color="red"))
                self.fig_custo = go.Figure(data=[barra_custo_hfp,barra_custo_hp,linha_custo_soma])
                self.fig_custo.update_layout(
                                title={"text":f"Custo mensal",
                                    "x":0.1,"y":0.9,"xanchor" : "left", "yanchor":"top"},
                                yaxis = dict(title="Custo (R$)", tickformat=',.2f', tickprefix = "R$", separatethousands =True),
                                xaxis = dict(title="Meses"),
                                plot_bgcolor = "#b6d5ee",
                                paper_bgcolor = "#006494",
                                hovermode = "x",
                                )
                st.plotly_chart(self.fig_custo, use_container_width=True)
            
            with col13:
                pizza_custo = go.Pie(labels=["",""],values=[sum(self.l_custo_hfp), sum(self.l_custo_hp)], showlegend=False,
                            title="Percentual HFP x HP")
                fig_pizza_custo = go.Figure(data=[pizza_custo])
                fig_pizza_custo.update_traces(marker=dict(colors=["#00a2ff","#ff6600"],
                    line = dict(color = "#FFFFFF", width=1)), textfont_size = 12)
                fig_pizza_custo.update_layout(
                    paper_bgcolor = "#006494",
                )
                st.plotly_chart(fig_pizza_custo, key="pizza_custo")
            
            
            col14,col15 = st.columns([6,1],gap="small", vertical_alignment="center" )
            with col14:
                barra_consumo_hfp = go.Bar(x=lista_x, y=self.l_hfp, name="HFP", marker_color = "#00a2ff")
                barra_consumo_hp = go.Bar(x=lista_x, y=self.l_hp, name = "HP", marker_color = "#ff6600")
                linha_consumo_soma = go.Scatter(x=lista_x, y=self.l_consumo_soma, name="HFP + HP" ,mode="markers+lines", 
                    marker=dict(size=6, symbol="circle"), line=dict(width=3,color="red"))
                self.fig_consumo = go.Figure(data=[barra_consumo_hfp,barra_consumo_hp,linha_consumo_soma])
                self.fig_consumo.update_layout(
                            title={"text":f"Consumo diário de {str(self.selecao_opcoes_mes).lower()}",
                                "x":0.1,"y":0.9,"xanchor" : "left", "yanchor":"top"},
                            yaxis = dict(title="Consumo", tickformat=',.0f'),
                            xaxis = dict(title="Data"),
                            plot_bgcolor = "#b6d5ee",
                            paper_bgcolor = "#006494",
                            hovermode = "x",
                            )
                st.plotly_chart(self.fig_consumo, use_container_width=True)

            with col15:
                pizza_consumo = go.Pie(labels=["",""],values=[sum(self.l_hfp), sum(self.l_hp)], showlegend=False,
                            title="Percentual HFP x HP")
                fig_pizza_consumo = go.Figure(data=[pizza_consumo])
                fig_pizza_consumo.update_traces(marker=dict(colors=["#00a2ff","#ff6600"],
                    line = dict(color = "#FFFFFF", width=1)), textfont_size = 12)
                fig_pizza_consumo.update_layout(
                    paper_bgcolor = "#006494",
                )
                st.plotly_chart(fig_pizza_consumo, key="pizza_consumo")
                
            
            self.container3_1 = st.container(key="container_tres_um")
            with self.container3_1:
                st.button("Análise", on_click=self.analise_gemma)
            self.container3_2 = st.container(key="container_tres_dois") 
        
            self.container3_3 = st.container(key="container_tres_tres")
            with self.container3_3:
                fig6 = go.Figure()
                del colunas[0]
                for i in colunas:
                    fig6.add_trace(go.Scatter(x=lista_x,y=df2[i], name=i, mode="markers+lines"))
                fig6.update_layout(
                            title={"text":"Gráfico de medições","x":0.5,"y":0.9,"xanchor" : "center", "yanchor":"top"},
                            yaxis_title="Medição",
                            xaxis_title="Data",
                            xaxis = dict(title="Data",range = [0,31]),
                            hovermode = "x"
                        )
                #st.plotly_chart(fig6, use_container_width=True)
        self.local_css(pathlib.Path("assets//style.css"))
if __name__=="__main__":
    Dashboard()