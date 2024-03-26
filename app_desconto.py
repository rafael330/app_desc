import streamlit as st
import gspread as gs 
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
        page_title="Solicitação de desconto",
        page_icon=("🌐"),
        layout="wide",
        initial_sidebar_state="expanded"    
    )

tab1, tab2 = st.tabs(['Formulário de solicitação','Status de dolicitação'])

with tab1:
    
    st.title('SOLICITAÇÃO DE :red[DESCONTOS]')
    st.text('Neste aplicativo você fara as solicitações de descontos que seguirão o fluxo de aprovação junto a diretoria, por tanto, muita ATENÇÃO!!')
    st.text('Preencha corretamente as informações solicitadas')
    st.write("<br>", unsafe_allow_html=True)
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('jsonkey_raf.json', scope)
    client = gs.authorize(creds)
    planilha = client.open_by_key('1m6cIPe-LiYI07YNUOnDfJKthjlRDauxns98GdHV7-RY')
    aba = planilha.worksheet('Página1')

    filial = st.text_input('*Filial:*','Digite aqui ...')
    st.write("<br>", unsafe_allow_html=True)

    cod_cliente = st.text_input('*Código Cliente:*', 'Digite o código do cliente')
    st.write("<br>", unsafe_allow_html=True)

    nome_cliente = st.text_input('*Nome Cliente:*', 'Digite o nome do cliente')
    st.write("<br>", unsafe_allow_html=True)

    cod_vendedor = st.text_input('*Código Vendedor:*', 'Digite o código do vendedor')
    st.write("<br>", unsafe_allow_html=True)

    plano_pagamento = st.text_input('*Plano de pagamento*', 'Digite aqui ...')
    st.write("<br>", unsafe_allow_html=True)

    cod_produto = st.text_input('*Código do produto*', 'Digite o código do produto')
    st.write("<br>", unsafe_allow_html=True)

    preco_tabela = st.text_input('*Preço tabela*', 'Digite o preço de tabela')
    st.write("<br>", unsafe_allow_html=True)

    preco_negociado = st.text_input('*Preço negociado*', 'Digite aqui ...')
    st.write("<br>", unsafe_allow_html=True)

    quantidade = st.text_input('*Quantidade*', 'Digite aqui ...')
    st.write('Sempre em unidade de venda')
    st.write("<br>", unsafe_allow_html=True)
    
    import time

    if st.button('Enviar solicitação', type='primary'):
        aba.append_row([filial, cod_cliente, nome_cliente, cod_vendedor, plano_pagamento, cod_produto, preco_tabela, preco_negociado, quantidade])
        texto_progresso = "Solicitação sendo finalizada. Aguarde ..."
        barra = st.progress(0, text=texto_progresso)
        for percentual_completo in range(100):
            time.sleep(0.01)
            barra.progress(percentual_completo + 1, text=texto_progresso)
        time.sleep(1)
        barra.empty()
        time.sleep(1)
        st.success('Solicitação enviada com sucesso')

with tab2:
    import pandas as pd
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('jsonkey_raf.json', scope)
    client = gs.authorize(creds)
    planilha = client.open_by_key('1m6cIPe-LiYI07YNUOnDfJKthjlRDauxns98GdHV7-RY')
    aba = planilha.worksheet('Página1')
    
    dados = aba.get_all_records()
    df = pd.DataFrame(dados) 
    df['CÓDIGO VENDEDOR'] = df['CÓDIGO VENDEDOR'].astype(str)
    df = df[['cod_identificador','FILIAL','NOME CLIENTE','CÓDIGO VENDEDOR','STATUS','OBS:']]
    
    filtro_vendedor = st.text_input('*Código vendedor*', 'Digite aqui ...')
    df_filtrado = df[df['CÓDIGO VENDEDOR'] == filtro_vendedor]
    
    def style_table(df):
        return df.style.set_table_styles(
            [{'selector': 'th', 'props': [('background-color', '#8A2BE2'), ('color', 'white'), ('text-align', 'center')]}]
        ).set_properties(**{'text-align': 'center'}).hide()
    
    st.header('Status da solicitação')
    styled_df = style_table(df_filtrado)    
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)