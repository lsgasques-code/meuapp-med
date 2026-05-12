import streamlit as st
import google.generativeai as genai
import data_helper

st.set_page_config(page_title="Gerador de Planos UNIPAR", layout="wide")

st.title("🍎 Arquiteto de Ensino Medicina UNIPAR")
st.caption("Alinhado às DCNs 2025 e Matriz de Referência ENAMED (Portaria 478/2025)")

# 1. Autenticação Segura
if "GEMINI_API_KEY" not in st.secrets:
    st.error("ERRO CRÍTICO: A chave 'GEMINI_API_KEY' não foi encontrada nos Secrets do Streamlit Cloud.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Definição do Modelo Oficial do Google (Versão Estável)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Identificação")
    professor_nome = st.text_input("Nome do Professor Responsável:")
    turma_periodo = st.text_input("Turma/Período (Ex: Turma A - 2026/1):")

# --- ÁREA PRINCIPAL ---
st.subheader("1. Configuração Curricular")
modulo_selecionado = st.selectbox("Selecione o Módulo Integrado:", list(data_helper.MODULOS_UNIPAR.keys()))
dados_modulo = data_helper.MODULOS_UNIPAR[modulo_selecionado]

# NOVO CAMPO: Nome da disciplina
disciplina_nome = st.text_input("Nome da Disciplina (Ex: Anatomia Humana I, Fisiologia II):")

st.subheader("2. Foco Pedagógico")
conteudo_input = st.text_area("Descreva os temas centrais ou patologias que deseja focar neste plano:", height=150)

if st.button("Gerar Plano de Ensino Ótimo"):
    if not professor_nome or not disciplina_nome or not conteudo_input:
        st.warning("Por favor, preencha o nome do professor, o nome da disciplina e os temas centrais antes de gerar o plano.")
    else:
        prompt = f"""
        Atue como um Especialista rigoroso em Educação Médica. Crie um Plano de Ensino oficial para o curso de Medicina da UNIPAR.
        
        DADOS INSTITUCIONAIS PARA IDENTIFICAÇÃO:
        Disciplina Foco: {disciplina_nome}
        Módulo Integrador: {modulo_selecionado}
        Professor Responsável: {professor_nome}
        Turma/Período: {turma_periodo}
        Carga Horária Total do Módulo: {dados_modulo['carga_horaria']}
        Ementas Oficiais do Módulo: {dados_modulo['ementas']}
        Ciclo: {dados_modulo['ciclo']}
        
        Temas inseridos pelo professor: {conteudo_input}
        
        REGRAS PEDAGÓGICAS ESTRITAS (NÃO DESVIE):
        1. Identificação
