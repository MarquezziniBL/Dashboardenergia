import pandas as pd
import numpy as np
from datetime import date
import calendar
from scripts import consulta_bd as consbd

class Calc ():

    # fUNÇÕES PARA BUSCAR DADOS NO BD
    def dados_selectbox(self):
        ano_atual = date.today().year
        lista_anos = list(range(2024,date.today().year+1))
        lista_meses = list(calendar.month_name)[1:]
        lista_dependencias = ["SEDE","HTS", "HTO", "ALQQ", "USINA/CICRIN", "FADOR", "CIAFV01"]

        return lista_anos,lista_meses, lista_dependencias
    
    def dados_consumo(self):
        lista_anos,lista_meses, lista_dependencias = self.dados_selectbox()
        dict_dados = {}
        
        for i in lista_anos:
            dict_dados[f"{i}"] = {}
            for j in lista_meses:
                dados = consbd.Banco_dados(i).select_dados(j.upper())
                dict_dados[f"{i}"][f"{j}"] = dados
        return dict_dados
    
    def dados_bandeiras(self): 
        lista_anos,lista_meses, lista_dependencias = self.dados_selectbox()
        lista_anos.append("valor_bandeiras")
        dict_dados = {}
        
        
        for i in lista_anos:
            dados = consbd.Banco_dados("bandeiras_mes").select_dados(i)
            dict_dados[f"{i}"] = dados

        return dict_dados

    def dados_gastomensal(self):
        lista_anos,lista_meses, lista_dependencias = self.dados_selectbox()
        dict_dados = {}
        for i in lista_anos:   
            dados = consbd.Banco_dados(i).select_dados("GASTOMENSAL")
            dict_dados[f"{i}"] = dados
        
        return dict_dados
    #FUNÇÕES DE TRATAMENTO DE DADOS
    def soma_geral_consumo(self, df, ano, mes):
        lista_somas_consumo = []
        lista_dependencias = ["SEDE","HTS", "HTO", "ALQQ", "USINA/CICRIN", "FADOR", "CIAFV01"]
        df = df[str(ano)][mes]
        for i in lista_dependencias:
            x = df[i+"-HP"]
            y = df[i+"-HFP"]
            res = sum(filter(lambda x: not np.isnan(x) and x >= 0, x))+sum(filter(lambda x: not np.isnan(x) and x >= 0, y))
            lista_somas_consumo.append(float(f"{res:.0f}"))

        soma_total = 0
        for x in list(lista_somas_consumo):
            soma_total += x

        return lista_somas_consumo, soma_total

    def soma_geral_valor(self,df, ano, dependencia):
        l_soma_hfp_hp = []
        l_hfp = df[f"{ano}"][f"{dependencia}-HFP"]
        l_hp = df[f"{ano}"][f"{dependencia}-HP"]

        for i,j in zip(l_hfp, l_hp):
           l_soma_hfp_hp.append(i+j)
        
        return l_soma_hfp_hp,l_hfp,l_hp

    def __init__(self):
        super().__init__()
        pass