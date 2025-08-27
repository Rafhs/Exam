import streamlit as st
from datetime import datetime  # Adicionado import

st.set_page_config(
    page_title="Início - Gestão de Saúde Ocupacional",
    page_icon="⚕️",
    layout="wide"
)

st.title("Bem-vindo ao Sistema de Gestão de Saúde Ocupacional ⚕️")
st.markdown("---")
st.subheader("Navegue pelo menu lateral para acessar as funcionalidades.")
st.info("""
    **O que você pode fazer aqui?**
    - **Dashboard:** Visualizar, filtrar e exportar dados dos funcionários.
    - **Cadastro de Funcionários:** Adicionar novos colaboradores ao sistema.
    - **Lançar Exames:** Registrar os exames ocupacionais de cada funcionário.
    - **Gerenciar Funções:** Cadastrar funções e associar os exames necessários.
    - **Exames a Vencer:** Controlar exames vencidos e próximos do vencimento.
""")
st.success(f"Sistema operando normalmente. Data e hora atuais: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
