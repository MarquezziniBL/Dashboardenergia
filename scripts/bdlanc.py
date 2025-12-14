import streamlit as st
from sqlalchemy import text
import datetime
import calendar


class Banco_dados():
    def select_bandeira(self,tabela,id):
        dados = self.cnx.query(f"select * from '{tabela}' where MES =  '{id}'")
        return dados
    
    def select_valor_bandeira(self,tabela,id):
        return self.cnx.query(f"select VALOR from '{tabela}' where BANDEIRA =  '{id}'")
    
    def select(self,mes):
        dados = self.cnx.query(f"select * from {mes}")
        return dados
    
    def select_consumo_dia(self,tabela,coluna_bd, coluna):
        dados = self.cnx.query(f"select * from {tabela} where {coluna_bd} = '{coluna}'")
        return dados
    
    def update_consumo(self,tabela,coluna_bd, coluna, **kwargs):
        with self.cnx.session as cnx:
            update_text = text(f" update {tabela} set 'SEDE-HFP'= :sedehfp ,'SEDE-HP'= :sedehp, 'HTS-HFP'= :htshfp, 'HTS-HP'= :htshp, 'HTO-HFP'= :htohfp, 'HTO-HP'= :htohp, 'ALQQ-HFP'= :alqqhfp,'ALQQ-HP'= :alqqhp,'USINA/CICRIN-HFP'= :usinahfp,'USINA/CICRIN-HP'= :usinahp,'FADOR-HFP'= :fadorhfp,'FADOR-HP'= :fadorhp,'CIAFV01-HFP'=:ciafv01hfp, 'CIAFV01-HP'= :ciafv01hp, 'ATIVIDADES' = :atividades where {coluna_bd} = :coluna;")
            values = {"sedehfp":kwargs["sedehfp"],"sedehp":kwargs["sedehp"], "htshfp":kwargs["htshfp"], "htshp":kwargs["htshp"], "htohfp":kwargs["htohfp"], "htohp":kwargs["htohp"], "alqqhfp":kwargs["alqqhfp"], "alqqhp":kwargs["alqqhp"], "usinahfp":kwargs["usinahfp"], "usinahp":kwargs["usinahp"], "fadorhfp":kwargs["fadorhfp"], "fadorhp":kwargs["fadorhp"], "ciafv01hfp":kwargs["ciafv01hfp"], "ciafv01hp":kwargs["ciafv01hp"], "atividades":kwargs["atividades"], "coluna":coluna}
            cnx.execute(update_text, values)
            cnx.commit()
        return True
    
    def update_valor(self,tabela,coluna_bd, coluna, **kwargs):
        with self.cnx.session as cnx:
            update_text = text(f" update {tabela} set 'SEDE-HFP'= :sedehfp ,'SEDE-HP'= :sedehp, 'HTS-HFP'= :htshfp, 'HTS-HP'= :htshp, 'HTO-HFP'= :htohfp, 'HTO-HP'= :htohp, 'ALQQ-HFP'= :alqqhfp,'ALQQ-HP'= :alqqhp,'USINA/CICRIN-HFP'= :usinahfp,'USINA/CICRIN-HP'= :usinahp,'FADOR-HFP'= :fadorhfp,'FADOR-HP'= :fadorhp,'CIAFV01-HFP'=:ciafv01hfp, 'CIAFV01-HP'= :ciafv01hp where {coluna_bd} = :coluna;")
            values = {"sedehfp":kwargs["sedehfp"],"sedehp":kwargs["sedehp"], "htshfp":kwargs["htshfp"], "htshp":kwargs["htshp"], "htohfp":kwargs["htohfp"], "htohp":kwargs["htohp"], "alqqhfp":kwargs["alqqhfp"], "alqqhp":kwargs["alqqhp"], "usinahfp":kwargs["usinahfp"], "usinahp":kwargs["usinahp"], "fadorhfp":kwargs["fadorhfp"], "fadorhp":kwargs["fadorhp"], "ciafv01hfp":kwargs["ciafv01hfp"], "ciafv01hp":kwargs["ciafv01hp"], "coluna":coluna}
            cnx.execute(update_text, values)    
            cnx.commit()
        return True
    
    def update_bandeira(self,tabela, **kwargs):
        with self.cnx.session as cnx:
            update_text = text(f"update '{tabela}' set BANDEIRA = :bandeira, VALOR = :valor where MES = :mes")
            values = {"bandeira":kwargs["bandeira"], "valor": kwargs["valor"], "mes":kwargs["mes"]}
            cnx.execute(update_text,values)
            cnx.commit()
        return True
    
    def __init__(self,bd):
        self.cnx = st.connection(f"{bd}", type="sql", url = f"sqlite:///database/bd_sec/{bd}.db")


