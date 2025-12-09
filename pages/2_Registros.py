import streamlit as st
import pathlib
from sqlalchemy import text
import pandas as pd
from datetime import date
import calendar
from scripts import bdlanc as bdl

lista_anos = [2024,2025,2026]
ano_atual= lista_anos.index(date.today().year)

lista_meses = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO",
    "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

lista_bandeira = ["Verde", "Amarela", "Vermelha P1", "Vermelha P2"]

class Lanc():

    # Implementação do CSS
    def local_css(self,filename):
        with open(filename) as fn:
            st.markdown(f"<style>{fn.read()}</style>", unsafe_allow_html=True)
    
    def update_df0(self):
        st.cache_data.clear()
        return bdl.Banco_dados(self.selecao_opcoes_ano).select(self.selecao_opcoes_mes)
    
    def update_df1(self):
        st.cache_data.clear()
        return bdl.Banco_dados(self.selecao_opcoes_ano).select("GASTOMENSAL")
    
    def update_df2(self):
        st.cache_data.clear()
        return bdl.Banco_dados("bandeiras_mes").select_bandeira(self.selecao_opcoes_ano,self.selecao_opcoes_mes)
    
    def __init__(self):
        
        self.titulo_pagina = st.set_page_config(page_title="Dashboard", layout="wide",
            initial_sidebar_state="collapsed")

        #Tirar anchor de elementos
        st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")
        
        with st.sidebar:
            st.write("Links Importantes")
            st.page_link("https://www.cemig.com.br", label="CEMIG")
            st.page_link("https://atende.cemig.com.br/Login", label="CEMIG Login")  
        
        with st.container(border=False, key="container_1"):
            with st.container(border=False, key="container_1_1"):
                st.markdown("<h1 class =h1_header_lanc>Selecione:</h1>", unsafe_allow_html=True)

            st.markdown("<h5 class =h5_header_lanc> Registros </h5>", unsafe_allow_html=True)
            with st.container(border=False, key="container_1_2"):
                    self.selecao_opcoes_ano = st.selectbox("Ano",options= lista_anos,index=ano_atual, key="container_1_1_select_ano")
                    self.selecao_opcoes_mes = st.selectbox("Mês",options= lista_meses, key="container_1_1_select_mes")
                    df0 = pd.DataFrame(self.update_df0()) 
                    df1 = pd.DataFrame(self.update_df1()) 
                    df2 = pd.DataFrame(self.update_df2())
            
            tab1, tab2, tab3 = st.tabs(["Consumo","Gasto Mensal", "Bandeira"])
            with tab1:
                if st.button("Recarregar", icon= ":material/autorenew:"):
                        df0 = pd.DataFrame(self.update_df0())      
                st.dataframe(df0, hide_index=True)
            
            with tab2:
                if st.button(" Recarregar ", icon= ":material/autorenew:"):
                    df1 = pd.DataFrame(self.update_df1())   
                st.dataframe(df1, hide_index=True)
            
            with tab3:
                if st.button(" Recarregar  ", icon= ":material/autorenew:"):
                    df1 = pd.DataFrame(self.update_df2())   
                st.dataframe(df2, hide_index=True)
        
        with st.container(border=False, key="container_2"):
            
            st.markdown("<h5 class =h5_header_lanc> Lançamentos </h5>", unsafe_allow_html=True)
            
            tab4, tab5, tab6 = st.tabs(["Consumo","Gasto Mensal", "Bandeira"])
            with tab4:
                
                with st.container(border=False, key="container_2_0"):
                    self.selecao_ano0 = st.selectbox("  Ano  ",options= lista_anos,index=ano_atual)
                    self.selecao_mes0 = st.selectbox("  Mês  ",options= lista_meses)
                    df3 = bdl.Banco_dados(self.selecao_ano0).select(self.selecao_mes0)
                    self.selecao_opcoes_dia = st.selectbox("Dia",options= df3["Data"], key="container_2_select_dia")
                    df4 = bdl.Banco_dados(self.selecao_ano0).select_consumo_dia(self.selecao_mes0,"Data",self.selecao_opcoes_dia)
                with st.container(border=False, key="container_2_1"):
                    sede_hfp = st.number_input("Sede HFP:",min_value= 0.0 ,value = df4["SEDE-HFP"][0], format="%.2f")
                    sede_hp = st.number_input("Sede HP:",min_value= 0.0 ,value = df4["SEDE-HP"][0], format="%.2f")
                
                with st.container(border=False, key="container_2_2"):
                    hts_hfp = st.number_input("HTS HFP:",min_value= 0.0 ,value = df4["HTS-HFP"][0], format="%.2f")
                    hts_hp = st.number_input("HTS HP:",min_value= 0.0 ,value = df4["HTS-HP"][0], format="%.2f")
                    hto_hfp = st.number_input("HTO HFP:",min_value= 0.0 ,value = df4["HTO-HFP"][0], format="%.2f")
                    hto_hp = st.number_input("HTO HP:",min_value= 0.0 ,value = df4["HTO-HP"][0], format="%.2f")
                    
                with st.container(border=False, key="container_2_3"):
                    alqq_hfp = st.number_input("ALQQ HFP:",min_value= 0.0 ,value = df4["ALQQ-HFP"][0], format="%.2f")
                    alqq_hp = st.number_input("ALQQ HP:",min_value= 0.0 ,value = df4["ALQQ-HP"][0], format="%.2f")
                    usina_hfp = st.number_input("USINA/CICRIN HFP:",min_value= 0.0 ,value = df4["USINA/CICRIN-HFP"][0], format="%.2f")
                    usina_hp = st.number_input("USINA/CICRIN HP:",min_value= 0.0 ,value = df4["USINA/CICRIN-HP"][0], format="%.2f")
                
                with st.container(border=False, key="container_2_4"):
                    fador_hfp = st.number_input("FADOR HFP:",min_value= 0.0 ,value = df4["FADOR-HFP"][0], format="%.2f")
                    fador_hp = st.number_input("FADOR HP:",min_value= 0.0 ,value = df4["FADOR-HP"][0], format="%.2f")
                    ciafv01_hfp = st.number_input("CIAFV01 HFP:",min_value= 0.0 ,value = df4["CIAFV01-HFP"][0], format="%.2f")
                    ciafv01_hp = st.number_input("CIA01 HP:",min_value= 0.0 ,value = df4["CIAFV01-HP"][0], format="%.2f")
                
                with st.container(border=False, key="container_2_5"):
                    self.atividades = st.text_input("Atividades", value = df4["ATIVIDADES"][0],placeholder= "Reunião Adm, Reunião de Obras, etc...")
                
                if st.button("Atualizar"):
                    try:
                        
                        if bdl.Banco_dados(self.selecao_ano0).update_consumo(
                        self.selecao_mes0,"Data" ,self.selecao_opcoes_dia,
                        sedehfp = sede_hfp, sedehp = sede_hp,
                        htshfp = hts_hfp, htshp = hts_hp,
                        htohfp = hto_hfp, htohp = hto_hp,
                        alqqhfp = alqq_hfp, alqqhp = alqq_hp,
                        usinahfp = usina_hfp, usinahp = usina_hp,
                        fadorhfp = fador_hfp, fadorhp = fador_hp,
                        ciafv01hfp = ciafv01_hfp, ciafv01hp = ciafv01_hp, atividades = self.atividades):
                            st.success("Atualização concluída com sucesso, recarregue a tabela para vizualizar as alterações!")
                    except BaseException:
                        st.toast("Erro ao conectar com Banco de Dados!")
            
            with tab5:
                with st.container(border=False, key="container_2_6"):
                    self.selecao_mes = st.selectbox("Mês", options= lista_meses )
                    v_sede_hfp = st.number_input("  Sede HFP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_sede_hp = st.number_input("  Sede HP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                
                with st.container(border=False, key="container_2_7"):
                    v_hts_hfp = st.number_input("  HTS HFP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_hts_hp = st.number_input("  HTS HP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_hto_hfp = st.number_input("  HTO HFP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_hto_hp = st.number_input("  HTO HP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    
                with st.container(border=False, key="container_2_8"):
                    v_alqq_hfp = st.number_input("  ALQQ HFP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_alqq_hp = st.number_input("  ALQQ HP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_usina_hfp = st.number_input("  USINA/CICRIN HFP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_usina_hp = st.number_input("  USINA/CICRIN HP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                
                with st.container(border=False, key="container_2_9"):
                    v_fador_hfp = st.number_input("  FADOR HFP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_fador_hp = st.number_input("  FADOR HP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_ciafv01_hfp = st.number_input("  CIAFV01 HFP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                    v_ciafv01_hp = st.number_input(" CIA01 HP:",min_value= 0.0 ,value = 0.0, format="%.2f")
                
                if st.button("Atualizar "):
                    try:
                        
                        if bdl.Banco_dados(self.selecao_opcoes_ano).update_valor(
                        "GASTOMENSAL","mes" ,self.selecao_mes,
                        sedehfp = v_sede_hfp, sedehp = v_sede_hp,
                        htshfp = v_hts_hfp, htshp = v_hts_hp,
                        htohfp = v_hto_hfp, htohp = v_hto_hp,
                        alqqhfp = v_alqq_hfp, alqqhp = v_alqq_hp,
                        usinahfp = v_usina_hfp, usinahp = v_usina_hp,
                        fadorhfp = v_fador_hfp, fadorhp = v_fador_hp,
                        ciafv01hfp = v_ciafv01_hfp, ciafv01hp = v_ciafv01_hp):
                            st.success("Atualização concluída com sucesso, recarregue a tabela para vizualizar as alterações!")
                    
                    except BaseException:
                        st.toast("Erro ao conectar com Banco de Dados!")
            with tab6:
                with st.container(border=False, key="container_2_10"):  
                    self.selecao_ano1 = st.selectbox(" Ano ", options= lista_anos, index= ano_atual) 
                    self.selecao_mes1 = st.selectbox(" Mês ", options= lista_meses)
                    self.selecao_bandeira = st.selectbox(" Bandeira ", options= lista_bandeira)
                    valor = bdl.Banco_dados("bandeiras_mes").select_valor_bandeira("valor_bandeiras",self.selecao_bandeira)
                    self.valor_bandeira = st.number_input("Valor da Bandeira", min_value= 0.0,
                        value= valor["VALOR"][0], disabled= True ,format="%.2f")
                
                if st.button(" Atualizar "):
                    try:
                        if bdl.Banco_dados("bandeiras_mes").update_bandeira(self.selecao_ano1,bandeira = self.selecao_bandeira,
                            valor = self.valor_bandeira,mes = self.selecao_mes1):
                            st.success("Atualização concluída com sucesso, recarregue a tabela para vizualizar as alterações!")
                    
                    except BaseException:
                        st.toast("Erro ao conectar com Banco de Dados!")
                    
        self.local_css(pathlib.Path("assets//style2.css"))
Lanc()