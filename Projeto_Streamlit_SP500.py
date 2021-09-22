import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import plotly.express as px
import datetime


# Titulo do Aplicativo
st.markdown('''
# Aplicativo de Consulta do Índice S&P 500 
O índice do mercado de ações S&P 500 , mantido pela S&P Dow Jones Indices , compreende 505 ações ordinárias emitidas por 500 empresas de grande capitalização e negociadas nas bolsas de valores americanas (incluindo as 30 empresas que compõem o Dow Jones Industrial Average ), e inclui cerca de 80 por cento do mercado de ações americano por capitalização. 

O aplicativo consiste em exibir os dados dos preços das ações e gráficos com visualização interativa para a empresa e o período de tempo que você escolher.

**Créditos**
- Aplicativo desenvolvido por [Gabriela L. Paresqui](https://github.com/Paresqui) 
- Criado em `Python` utilizando`streamlit`,`pandas`, `cufflinks`, `yfinance` e `Plotly`
''')
st.write('---')

# Criando o Sidebar
st.sidebar.subheader('Parâmetros para Consulta')
data_inicio = st.sidebar.date_input("Data de Início", datetime.date(2019, 1, 1))
data_termino = st.sidebar.date_input("Data de Término", datetime.date(2021, 1, 31))

# Recuperando os dados 
lista_siglas = pd.read_csv('https://raw.githubusercontent.com/Paresqui/Streamlit_S-P-500-companies/main/siglas_empresas.txt.txt')
sidebar_siglas = st.sidebar.selectbox('Selecione a empresa', lista_siglas) # Selecionando os dados das siglas
dados_siglas = yf.Ticker(sidebar_siglas) # Setando os dados das siglas para o método 'Ticker' 
tickerDf = dados_siglas.history(period='1d', start=data_inicio, end=data_termino) #Retorna o histórico de preços para a sigla escolhida

# Informação das Empresas
string_logo = '<img src=%s>' % dados_siglas.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = dados_siglas.info['longName']
st.header('**%s**' % string_name)

string_summary = dados_siglas.info['longBusinessSummary']
st.info(string_summary)

# Dataframe
st.header('**Tabela de Ações**')
st.write(tickerDf)


# Bollinger bands
st.header('**Gráfico de Bandas de Bollinger **')
qf=cf.QuantFig(tickerDf,title='Primeira Figura do Quantil',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

                      
#SMA - Simple Moving Average
st.header('**Gráfico de SMA **')
qf1=cf.QuantFig(tickerDf,title='Média Móvel Simples - SMA',legend='top',name='GS')
qf1.add_sma([20,40], width=2, color=['green', 'lightgreen'],legendgroup=True)
fig1 = qf1.iplot(asFigure=True)
st.plotly_chart(fig1)

#Gráfico com Volume
st.header('**Gráfico de Linhas**')
qf2=cf.QuantFig(tickerDf,title='Volume de oscilação',legend='top',name='GS')
qf2.add_volume()
fig2 = qf2.iplot(asFigure=True)
st.plotly_chart(fig2)

#OHLC - Open-high-low-close
st.header('**Gráfico de OHLC**')
ohlc_graf = tickerDf.iplot(kind='ohlc',title='Open-high-low-close Chart', asFigure=True)
st.plotly_chart(ohlc_graf)

#High Low - Spread Chart
st.header('**Gráfico de High - Low Spread **')
rsi_graf = tickerDf[['High','Low']].iplot(kind='spread',title='High-low Spread Chart', asFigure=True)
st.plotly_chart(rsi_graf)

#Open Close - Spread Chart
st.header('**Gráfico de Open - Close Spread **')
rsi_graf = tickerDf[['Open','Close']].iplot(kind='spread',title='Relative Strength Index', asFigure=True)
st.plotly_chart(rsi_graf)

#RSI
st.header('**Gráfico de RSI**')
qf5=cf.QuantFig(tickerDf,title='Índice de Força Relativa - RSI')
qf5.add_rsi()
fig5 = qf5.iplot(asFigure=True)
st.plotly_chart(fig5)