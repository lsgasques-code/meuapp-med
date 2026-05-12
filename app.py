# app.py
import streamlit as st
import google.generativeai as genai
import data_helper

st.set_page_config(page_title="Gerador de Planos UNIPAR", layout="wide")

st.title("🍎 Arquiteto de Ensino Medicina UNIPAR")
st.caption("Alinhado às DCNs 2025 e Matriz de Referência ENAMED (Portaria 478/2025)")

# Verifica se a chave da API está configurada nos segredos do Streamlit
if "GEMINI_API_KEY" not in st.secrets:
    st.error("ERRO CRÍTICO: A chave 'GEMINI_API_KEY' não foi encontrada nos Secrets do Streamlit Cloud.")
    st.stop()

# Configuração da API do Gemini puxando a chave segura
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Identificação do Docente")
    professor_nome = st.text_input("Nome do Professor Responsável")

# --- ÁREA PRINCIPAL ---
st.subheader("1. Configuração do Módulo")
modulo_selecionado = st.selectbox("Selecione o Módulo Integrado:", list(data_helper.MODULOS_UNIPAR.keys()))
dados_modulo = data_helper.MODULOS_UNIPAR[modulo_selecionado]

st.subheader("2. Foco Pedagógico")
conteudo_input = st.text_area("Descreva os temas centrais ou patologias que deseja focar neste plano:", height=150)

if st.button("Gerar Plano de Ensino Ótimo"):
    if not professor_nome or not conteudo_input:
        st.warning("Por favor, preencha o nome do professor e os temas centrais antes de gerar.")
    else:
        prompt = f"""
        Atue como um Especialista rigoroso em Educação Médica. Crie um Plano de Ensino oficial para o curso de Medicina da UNIPAR.
        
        DADOS INSTITUCIONAIS:
        Módulo: {modulo_selecionado}
        Professor: {professor_nome}
        Carga Horária Total: {dados_modulo['carga_horaria']}
        Ementas Oficiais do Módulo: {dados_modulo['ementas']}
        Ciclo: {dados_modulo['ciclo']}
        
        Temas inseridos pelo professor: {conteudo_input}
        
        REGRAS PEDAGÓGICAS ESTRITAS (NÃO DESVIE):
        1. Identificação: Crie o cabeçalho completo.
        2. Objetivos (Bloom): Se o ciclo for 'Básico', use verbos de Compreensão/Aplicação. Se for 'Clínico', use Análise/Decisão.
        3. Visão Integrada: Organize o conteúdo programático de forma sistêmica (por sistemas do corpo ou síndromes), unindo as disciplinas básicas e clínicas.
        4. Matriz ENAMED (Portaria 478/2025): Crie uma tabela cruzando os conteúdos com as competências do ENAMED.
        5. Sistema de Avaliação: Crie uma tabela de avaliação garantindo rigorosamente que Provas Somativas/OSCE tenham peso total de 70%, e atividades formativas (PBL/Portfólio) tenham 30%.
        6. Metodologia: Proponha um mix de PBL, Simulação Realística e preleção dialogada.
        7. Plano de Recuperação: Estabeleça estratégias claras para alunos com baixo rendimento.
        8. Bibliografia: Sugira 3 obras básicas e 3 complementares no formato ABNT, priorizando literaturas médicas consagradas atualizadas.
        
        Gere o plano formatado em Markdown profissional.
        """

        with st.spinner('Analisando matriz curricular e gerando arquitetura pedagógica...') :
            try:
                response = model.generate_content(prompt)
                plano_gerado = response.text
                
                st.success("Plano de Ensino gerado com sucesso!")
                st.markdown("---")
                st.markdown(plano_gerado)
                
            except Exception as e:
                st.error(f"Ocorreu um erro ao comunicar com a IA: {e}")
