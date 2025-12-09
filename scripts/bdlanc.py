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
            cnx.execute(
                    text(f"update {tabela} set 'SEDE-HFP'={kwargs["sedehfp"]},'SEDE-HP'={kwargs["sedehp"]}, 'HTS-HFP'={kwargs["htshfp"]}, 'HTS-HP'={kwargs["htshp"]}, 'HTO-HFP'={kwargs["htohfp"]}, 'HTO-HP'={kwargs["htohp"]}, 'ALQQ-HFP'={kwargs["alqqhfp"]},'ALQQ-HP'={kwargs["alqqhp"]},'USINA/CICRIN-HFP'={kwargs["usinahfp"]},'USINA/CICRIN-HP'={kwargs["usinahp"]},'FADOR-HFP'={kwargs["fadorhfp"]},'FADOR-HP'={kwargs["fadorhp"]},'CIAFV01-HFP'={kwargs["ciafv01hfp"]}, 'CIAFV01-HP'={kwargs["ciafv01hp"]}, 'ATIVIDADES' = '{kwargs["atividades"]}' where {coluna_bd} = '{coluna}';"))
            cnx.commit()
            cnx.close()
        return True
    
    def update_valor(self,tabela,coluna_bd, coluna, **kwargs):
        with self.cnx.session as cnx:
            cnx.execute(
                    text(f"update {tabela} set 'SEDE-HFP'={kwargs["sedehfp"]},'SEDE-HP'={kwargs["sedehp"]}, 'HTS-HFP'={kwargs["htshfp"]}, 'HTS-HP'={kwargs["htshp"]}, 'HTO-HFP'={kwargs["htohfp"]}, 'HTO-HP'={kwargs["htohp"]}, 'ALQQ-HFP'={kwargs["alqqhfp"]},'ALQQ-HP'={kwargs["alqqhp"]},'USINA/CICRIN-HFP'={kwargs["usinahfp"]},'USINA/CICRIN-HP'={kwargs["usinahp"]},'FADOR-HFP'={kwargs["fadorhfp"]},'FADOR-HP'={kwargs["fadorhp"]},'CIAFV01-HFP'={kwargs["ciafv01hfp"]}, 'CIAFV01-HP'={kwargs["ciafv01hp"]} where {coluna_bd} = '{coluna}';"))
            cnx.commit()
            cnx.close()
        return True
    
    def update_bandeira(self,tabela, **kwargs):
        with self.cnx.session as cnx:
            cnx.execute(text(f"update '{tabela}' set BANDEIRA = '{kwargs["bandeira"]}', VALOR = '{kwargs["valor"]}' where MES = '{kwargs["mes"]}'"))
            cnx.commit()
            cnx.close()
        return True
    
    def __init__(self,bd):
        self.cnx = st.connection(f"{bd}", type="sql", url = f"sqlite:///database/bd_sec/{bd}.db")


