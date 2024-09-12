import streamlit as st
import pandas as pd
from datetime import datetime

# Função para carregar dados do CSV
def load_data():
    try:
        return pd.read_csv('progress_log.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Activity', 'Duration', 'Notes'])

# Função para salvar dados no CSV
def save_data(data):
    data.to_csv('progress_log.csv', index=False)

# Carregar dados existentes
data = load_data()

# Título da aplicação
st.title("Registro de Progresso Diário")

# Inputs do usuário
activity = st.text_input("Atividade", "")
duration = st.number_input("Duração (em minutos)", min_value=0, value=0, step=1)
notes = st.text_area("Notas adicionais", "")
date = st.date_input("Data", datetime.now().date())

# Botão para salvar os dados
if st.button("Registrar Progresso"):
    new_entry = pd.DataFrame({
        'Date': [date],
        'Activity': [activity],
        'Duration': [duration],
        'Notes': [notes]
    })
    data = pd.concat([data, new_entry], ignore_index=True)
    save_data(data)
    st.success("Progresso registrado com sucesso!")

# Exibir os dados registrados
st.subheader("Histórico de Progresso")
st.dataframe(data)

# Download do CSV
st.download_button(
    label="Baixar registro em CSV",
    data=data.to_csv(index=False).encode('utf-8'),
    file_name='progress_log.csv',
    mime='text/csv',
)
