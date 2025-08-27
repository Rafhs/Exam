
import streamlit as st
from datetime import datetime, timedelta
# A importação deve ser do seu novo caminho
from data.dados import database as db

st.set_page_config(page_title="Cadastro de Funcionários", page_icon="📝", layout="wide")
st.header("📝 Portal de Cadastro de Funcionários")

if st.sidebar.button("🔄 Atualizar Lista de Funções"):
    st.cache_data.clear()
    st.success("Lista de funções atualizada!")

funcoes_cadastradas = db.get_all_funcoes()
if not funcoes_cadastradas:
    st.warning("Nenhuma função foi cadastrada no sistema.")
    st.info("Por favor, vá para a página 'Gerenciar Funções' para adicionar pelo menos uma função.")
    # Verifique se o seu arquivo se chama '4_Gerenciar_Funcoes.py'
    st.page_link("pages/4_Gerenciar_Funcoes.py", label="Clique aqui para cadastrar a primeira função", icon="➕")
    st.stop()

opcoes_funcoes = [funcao[1] for funcao in funcoes_cadastradas]

with st.form(key="cadastro_funcionario_form", clear_on_submit=True):
    empresa = st.text_input("Nome da Empresa", placeholder="Insira o nome da empresa")
    col_nome, col_cpf, col_rg = st.columns(3)
    with col_nome:
        nome = st.text_input("Nome Completo", placeholder="Insira o nome completo")
    with col_cpf:
        cpf = st.number_input("CPF (apenas números)", step=1, format="%d", max_value=99999999999)
    with col_rg:
        rg = st.number_input("RG (apenas números)", step=1, format="%d")

    col_mat, col_cargo, col_admissao = st.columns(3)
    with col_mat:
        matricula = st.number_input("Matrícula", min_value=1, step=1, format="%d")
    with col_cargo:
        cargo = st.selectbox("Cargo / Função", options=opcoes_funcoes)
        # Verifique se o seu arquivo se chama '4_Gerenciar_Funcoes.py'
        st.page_link("pages/4_Gerenciar_Funcoes.py", label="Não encontrou? Cadastre aqui", icon="➕")
    with col_admissao:
        data_admissao = st.date_input("Data de Admissão", value=datetime.now(), format="DD/MM/YYYY")

    departamento = st.text_input("Departamento", placeholder="Ex: Tecnologia")
    submit_button = st.form_submit_button(label="Cadastrar Funcionário")

    if submit_button:
        # A lógica de submissão permanece a mesma...
        if nome and cpf and rg and matricula and empresa and cargo and data_admissao:
            if db.add_funcionario(nome, str(cpf), str(rg), str(matricula), cargo, departamento, data_admissao.strftime('%Y-%m-%d'), empresa):
                st.success(f"Funcionário {nome} da empresa {empresa} cadastrado com sucesso!")
                # ... Lógica para adicionar exame ...
            else:
                st.error("Erro: CPF ou Matrícula (para esta empresa) já existem no sistema.")
        else:
            st.warning("Todos os campos são obrigatórios.")