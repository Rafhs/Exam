# pages/2_Cadastro_de_Funcionários.py (Versão com CNPJ e CPF corrigido)

import streamlit as st
from datetime import datetime, timedelta
from data.dados import database as db

st.set_page_config(page_title="Cadastro de Funcionários", page_icon="📝", layout="wide")
st.header("📝 Portal de Cadastro de Funcionários")

if st.sidebar.button("🔄 Atualizar Lista de Funções"):
    st.cache_data.clear()
    st.success("Lista de funções atualizada!")

funcoes_cadastradas = db.get_all_funcoes()
if not funcoes_cadastradas:
    st.warning("Nenhuma função foi cadastrada no sistema.")
    st.info("Por favor, vá para a página 'Gerenciar Funções' para adicionar uma função.")
    st.page_link("pages/4_Gerenciar_Funcoes.py", label="Clique aqui para cadastrar a primeira função", icon="➕")
    st.stop()

opcoes_funcoes = [funcao[1] for funcao in funcoes_cadastradas]

with st.form(key="cadastro_funcionario_form", clear_on_submit=True):
    # --- NOVO LAYOUT PARA EMPRESA E CNPJ ---
    col_empresa, col_cnpj = st.columns(2)
    with col_empresa:
        empresa = st.text_input("Nome da Empresa", placeholder="Insira o nome da empresa")
    with col_cnpj:
        # Usamos text_input para melhor controle de validação e formato
        cnpj = st.text_input("CNPJ (apenas números)", max_chars=14)

    col_nome, col_cpf, col_rg = st.columns(3)
    with col_nome:
        nome = st.text_input("Nome Completo", placeholder="Insira o nome completo")
    with col_cpf:
        # --- ALTERAÇÃO IMPORTANTE PARA O CPF ---
        # Trocado para st.text_input para aceitar zeros à esquerda e validar o comprimento.
        cpf = st.text_input("CPF (apenas números)", max_chars=11)
    with col_rg:
        rg = st.text_input("RG (apenas números)", max_chars=9) # RG também como texto

    col_mat, col_cargo, col_admissao = st.columns(3)
    with col_mat:
        matricula = st.text_input("Matrícula", max_chars=10)
    with col_cargo:
        cargo = st.selectbox("Cargo / Função", options=opcoes_funcoes)
        st.page_link("pages/4_Gerenciar_Funcoes.py", label="Não encontrou? Cadastre aqui", icon="➕")
    with col_admissao:
        data_admissao = st.date_input("Data de Admissão", value=datetime.now(), format="DD/MM/YYYY")

    departamento = st.text_input("Departamento", placeholder="Ex: Tecnologia")
    submit_button = st.form_submit_button(label="Cadastrar Funcionário")

    if submit_button:
        # Validação para garantir que os campos numéricos contenham apenas dígitos
        if not (cpf.isdigit() and rg.isdigit() and matricula.isdigit() and cnpj.isdigit()):
            st.error("Erro: CPF, RG, Matrícula e CNPJ devem conter apenas números.")
        elif len(cpf) != 11:
            st.error("Erro: O CPF deve conter exatamente 11 dígitos.")
        elif len(cnpj) != 14:
            st.error("Erro: O CNPJ deve conter exatamente 14 dígitos.")
        elif nome and matricula and empresa and cargo and data_admissao:
            # Passa o novo campo 'cnpj' para a função do banco de dados
            if db.add_funcionario(nome, cpf, rg, matricula, cargo, departamento, data_admissao.strftime('%Y-%m-%d'), empresa, cnpj):
                st.success(f"Funcionário {nome} da empresa {empresa} cadastrado com sucesso!")
                # Lógica para adicionar exame...
            else:
                st.error("Erro: CPF ou Matrícula (para esta empresa) já existem no sistema.")
        else:
            st.warning("Todos os campos são obrigatórios.")