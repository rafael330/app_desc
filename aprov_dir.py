import streamlit as st
import gspread as gs 
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

st.set_page_config(
        page_title="Solicitação de desconto",
        page_icon=("🎛️"),
        layout="wide",
        initial_sidebar_state="expanded"    
    )
st.title('SOLICITAÇÃO DE :blue[APROVAÇÃO]')
st.text('Monitore aqui as solicitações de descontos realizadas pelos vendedores')
st.write("<br>", unsafe_allow_html=True)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('jsonkey_raf.json', scope)
client = gs.authorize(creds)
planilha = client.open_by_key('1m6cIPe-LiYI07YNUOnDfJKthjlRDauxns98GdHV7-RY')
aba = planilha.worksheet('Página1')

dados = aba.get_all_records()
df = pd.DataFrame(dados)
df = df[df['Status atual'] == 'PENDENTE DE APROVAÇÃO']
df["PREÇO TABELA"] = df["PREÇO TABELA"].astype(float)/100
df['PREÇO TABELA'] = df['PREÇO TABELA'].apply(lambda x: '{:.2f}'.format(x).replace('.', ','))
df["PREÇO NEGOCIADO"] = df["PREÇO NEGOCIADO"].astype(float)/100
df['PREÇO NEGOCIADO'] = df['PREÇO NEGOCIADO'].apply(lambda x: '{:.2f}'.format(x).replace('.', ',')) 
df['QUANTIDADE'] = df['QUANTIDADE'].astype(int).replace(".",",").replace(",",".")
df = df[['FILIAL','NOME CLIENTE','CÓDIGO VENDEDOR','CÓDIGO DO PRODUTO','PREÇO TABELA','PREÇO NEGOCIADO','QUANTIDADE','url_aprovação']]

def style_table(df):
        return df.style.set_table_styles(
            [{'selector': 'th', 'props': [('background-color', '#8A2BE2'), ('color', 'white'), ('text-align', 'center')]}]
        ).set_properties(**{'text-align': 'center'}).hide()
        
def make_clickable(url):
    return f'<a href="{url}" target="_blank">{url}</a>'

df['url_aprovação'] = df['url_aprovação'].apply(make_clickable)
   
st.header('Solicitações Pendentes')
styled_df = style_table(df)    
st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)
