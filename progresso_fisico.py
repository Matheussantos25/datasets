import streamlit as st
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Nome do arquivo CSV
arquivo_csv = 'exercicios_diarios.csv'

# Cabeçalho do CSV
cabecalho = ['Dia', 'Tipo de Exercício', 'Repetições Totais', 'Número de Séries', 'Duração (min)', 'Horário', 'Intervalo entre Séries (min)']

# Função para adicionar um novo registro de exercício
def adicionar_exercicio(data_exercicio, tipo_exercicio, repeticoes_totais, numero_series, duracao, horario, intervalo_series):
    dia_formatado = data_exercicio.strftime('%d/%m/%Y')

    # Adicionar os dados no arquivo CSV
    with open(arquivo_csv, 'a', newline='', encoding='utf-8') as arquivo:
        escritor_csv = csv.writer(arquivo)
        if arquivo.tell() == 0:
            escritor_csv.writerow(cabecalho)
        escritor_csv.writerow([dia_formatado, tipo_exercicio, repeticoes_totais, numero_series, duracao, horario, intervalo_series])

    st.success("Registro adicionado com sucesso!")

# Função para carregar e processar dados
def carregar_dados():
    try:
        df = pd.read_csv(arquivo_csv, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(arquivo_csv, encoding='ISO-8859-1')
    
    df['Dia'] = pd.to_datetime(df['Dia'], format='%d/%m/%Y')
    return df

# Função para plotar gráfico de progresso com os dias da semana
def plotar_progresso(df, tipo_exercicio, periodo):
    if not df.empty:
        df_filtrado = df[df['Tipo de Exercício'] == tipo_exercicio]

        if periodo == 'Diário':
            df_filtrado = df_filtrado.groupby(pd.Grouper(key='Dia', freq='D')).sum()
        elif periodo == 'Semana':
            df_filtrado = df_filtrado.groupby(pd.Grouper(key='Dia', freq='W')).sum()
        elif periodo == 'Mês':
            df_filtrado = df_filtrado.groupby(pd.Grouper(key='Dia', freq='M')).sum()
        elif periodo == 'Semestre':
            df_filtrado = df_filtrado.groupby(pd.Grouper(key='Dia', freq='6M')).sum()

        if df_filtrado.empty:
            st.warning("Nenhum dado disponível para o período selecionado.")
            return

        # Adicionar a coluna com o nome dos dias da semana
        df_filtrado['Dia da Semana'] = df_filtrado.index.strftime('%A')

        plt.figure(figsize=(10, 5))
        plt.plot(df_filtrado['Dia da Semana'], df_filtrado['Repetições Totais'], marker='o')
        plt.title(f"Progresso de {tipo_exercicio} por {periodo}")
        plt.xlabel("Dia da Semana")
        plt.ylabel("Repetições Totais")
        plt.grid(True)
        st.pyplot(plt)

# Interface do usuário
st.title("Registro de Exercícios Diários")

# Substituir selectboxes por um date_input para o calendário completo
data_exercicio = st.date_input("Escolha a data", datetime.now())

# Dividindo a data em dia, mês e ano
dia = data_exercicio.day
mes = data_exercicio.month
ano = data_exercicio.year

# Adicionar lista de exercícios para o usuário escolher
exercicios = ['Flexão', 'Barra Sem Peso', 'Barra Com Peso', 'Agachamento', 'Pular Corda', 'Andar de Bike', 'Prancha']
tipo_exercicio = st.selectbox("Escolha o tipo de exercício:", exercicios)

repeticoes_totais = st.text_input("Digite o número total de repetições:")
numero_series = st.text_input("Digite o número de séries:")
duracao = st.text_input("Digite a duração de cada série (em minutos): (Se não se aplica, deixe em branco)")
horario = st.text_input("Digite o horário do exercício (HH:MM):")
intervalo_series = st.text_input("Digite o tempo de intervalo entre as séries (em minutos):")

if st.button("Adicionar Exercício"):
    adicionar_exercicio(data_exercicio, tipo_exercicio, repeticoes_totais, numero_series, duracao, horario, intervalo_series)

df = carregar_dados()

# Selecionar o tipo de exercício e o período para visualização
if not df.empty:
    st.header("Visualização do Progresso")
    exercicio_selecionado = st.selectbox("Escolha o tipo de exercício para ver o progresso:", df['Tipo de Exercício'].unique())
    periodo_selecionado = st.selectbox("Escolha o período:", ['Diário', 'Semana', 'Mês', 'Semestre'])

    if st.button("Mostrar Gráfico"):
        plotar_progresso(df, exercicio_selecionado, periodo_selecionado)
