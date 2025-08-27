import streamlit as st
import pandas as pd
from data.dados import database as db


st.set_page_config(page_title="Controle de Vencimentos", page_icon="🗓️", layout="wide")

st.title("🗓️ Controle de Vencimentos de Exames")
st.markdown("Visão completa dos exames a vencer e dos que já estão vencidos.")
st.markdown("---")

# --- SEÇÃO 1: EXAMES JÁ VENCIDOS ---
st.subheader("⚠️ Exames Vencidos")

# A chamada à função do banco de dados acontece aqui
exames_vencidos = db.get_exames_vencidos()

# A verificação acontece aqui: se a lista não estiver vazia, mostra a tabela.
if exames_vencidos:
    with st.expander("Clique para ver a lista de exames vencidos", expanded=True):
        df_vencidos = pd.DataFrame(
            exames_vencidos,
            columns=["Nome do Funcionário", "Matrícula", "Tipo de Exame", "Data de Vencimento"]
        )
        st.error("Atenção! Os seguintes exames já passaram da data de vencimento:")
        st.dataframe(df_vencidos, use_container_width=True, hide_index=True)
else:
    # Se a lista estiver vazia, mostra a mensagem de sucesso.
    st.success("Nenhum exame vencido encontrado. Parabéns!")

st.markdown("---")

# --- SEÇÃO 2: EXAMES A VENCER ---
st.subheader("Exames com Vencimento Próximo")

dias_para_vencer = st.slider(
    label="Selecione o período de visualização (em dias):",
    min_value=7,
    max_value=180,
    value=30,
    step=7
)

exames_a_vencer = db.get_exames_vencendo(dias=dias_para_vencer)

if exames_a_vencer:
    st.info(f"Encontrados {len(exames_a_vencer)} exames vencendo nos próximos {dias_para_vencer} dias.")
    df_exames = pd.DataFrame(
        exames_a_vencer,
        columns=["Nome do Funcionário", "Matrícula", "Tipo de Exame", "Data de Vencimento"]
    )
    st.dataframe(df_exames, use_container_width=True, hide_index=True)
else:
    st.info(f"Nenhum exame previsto para vencer nos próximos {dias_para_vencer} dias.")
