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
model = genai.GenerativeModel('gemini-pro')

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
        # ATENÇÃO AQUI: As três aspas abrem o texto
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
        1. Identificação: Crie o cabeçalho completo utilizando os dados acima.
        2. Objetivos (Bloom): Se o ciclo for 'Básico', use verbos de Compreensão/Aplicação. Se for 'Clínico', use Análise/Decisão. Focados na disciplina de {disciplina_nome}.
        3. Visão Integrada: Organize o conteúdo programático de forma sistêmica, garantindo que {disciplina_nome} dialogue com as outras áreas do módulo {modulo_selecionado}.
        4. Matriz ENAMED (Portaria 478/2025): Crie uma tabela cruzando os conteúdos de {disciplina_nome} com as competências do ENAMED.
        5. Sistema de Avaliação: Crie uma tabela de avaliação garantindo rigorosamente que Provas Somativas/OSCE tenham peso total de 70%, e atividades formativas (PBL/Portfólio) tenham 30%.
        6. Metodologia: Proponha um mix de PBL, Simulação Realística e preleção dialogada adequado para {disciplina_nome}.
        7. Plano de Recuperação: Estabeleça estratégias claras para alunos com baixo rendimento.
        8. Bibliografia: Sugira 3 obras básicas e 3 complementares no formato ABNT, priorizando literaturas médicas consagradas e atualizadas para a área.
        
        Gere o plano formatado em Markdown profissional.
        """
        # ATENÇÃO AQUI: As três aspas fecham o texto. Não as apague!

        with st.spinner('A analisar matriz curricular e a gerar arquitetura pedagógica...'):
            try:
                response = model.generate_content(prompt)
                plano_gerado = response.text
                
                st.success("Plano de Ensino gerado com sucesso!")
                st.markdown("---")
                st.markdown(plano_gerado)
                
                st.download_button(
                    label="Baixar Plano (Arquivo Markdown)", 
                    data=plano_gerado, 
                    file_name=f"Plano_de_Ensino_{disciplina_nome.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error("Ocorreu um erro ao comunicar com a IA do Google.")
                st.info(f"Detalhe técnico para o suporte: {e}")
