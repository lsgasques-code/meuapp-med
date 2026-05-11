import streamlit as st
from docx import Document
from docx.shared import Pt
import io

# --- BANCO DE DATOS INTEGRADO (EMENTÁRIO UNIPAR 2021) ---
# Extraído do documento oficial anexado
EMENTARIO_UNIPAR = {
    "História da Medicina": {
        "ch": "40 h/a", "serie": "1ª", "natureza": "Teórica",
        "ementa": "História da Medicina. Evolução da formação do raciocínio clínico... Introdução ao método científico. O processo saúde-doença... Sistema Único de Saúde.",
        "bibliografia_b": ["PEREIRA-NETO A. F. Ser médico no Brasil", "PORTER R. Cambridge - História da Medicina"],
        "bibliografia_c": ["FOUCAULT M. O Nascimento da clínica", "SOARES S. M. Médicos e mezinheiros"]
    },
    "Morfologia Humana Básica": {
        "ch": "240 h/a", "serie": "1ª", "natureza": "Integrada (T/P)",
        "ementa": "Histologia dos tecidos. Biologia do Desenvolvimento embrionário... Expressão Gênica. Síntese Proteica... Genética mendeliana.",
        "bibliografia_b": ["ALBERTS, B. et al. Biologia molecular da célula", "JUNQUEIRA, L. C. Histologia básica"],
        "bibliografia_c": ["THOMPSON, J. S. Genética médica", "MOORE, K. L. Embriologia básica"]
    },
    "Bioinformática": {
        "ch": "80 h/a", "serie": "2ª", "natureza": "Teórica/Prática",
        "ementa": "Informática computacional em saúde. Bancos de dados. Genômica e proteômica. Ferramentas de alinhamento e análise de sequências biológicas.",
        "bibliografia_b": ["LESK, A. M. Introdução à bioinformática", "ZVELEBIL, M. J. Understanding bioinformatics"],
        "bibliografia_c": ["VERLI, H. Bioinformática: da biologia à flexibilidade molecular"]
    }
    # O sistema buscará no dicionário acima. Se não achar, pedirá preenchimento manual.
}

# --- FUNÇÃO DE GERAÇÃO DE TEXTO INTELIGENTE (SIMULADA) ---
def gerar_objetivo_geral(temas):
    return f"Desenvolver a capacidade de analisar e aplicar os fundamentos de {temas.split(',')[0]}, alinhado às DCNs e ao raciocínio clínico médico."

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="IA Plano de Ensino Inteligente", layout="wide")
st.title("🧠 Geração de Plano de Ensino Inteligente")
st.caption("Modelo em conformidade com DCNs Medicina e ENAMED 2025")

# 1. IDENTIFICAÇÃO
st.header("1. Identificação da Disciplina")
nome_disc = st.selectbox("Nome da Disciplina (Conforme Matriz):", ["Selecione..."] + list(EMENTARIO_UNIPAR.keys()))
prof_resp = st.text_input("Nome do Professor Responsável:")
turma = st.text_input("Período/Turma:")

# Busca Automática no Ementário
dados_base = EMENTARIO_UNIPAR.get(nome_disc, {})
col1, col2, col3 = st.columns(3)
with col1:
    ch = st.text_input("Carga Horária:", valor=dados_base.get("ch", ""))
    serie = st.text_input("Série/Período:", valor=dados_base.get("serie", ""))
with col2:
    regime = st.selectbox("Regime:", ["Semestral", "Anual"])
    natureza = st.text_input("Natureza:", valor=dados_base.get("natureza", "Integrada"))
with col3:
    eixo = st.text_input("Eixo/Módulo:", placeholder="Ex: Morfofuncional")

# 2. EMENTA (Automática)
st.header("2. Ementa")
ementa_texto = st.text_area("Texto da Ementa (Puxado do Ementário):", value=dados_base.get("ementa", ""), height=100)

# 3. CONTEÚDO (Professor preenche)
st.header("5. Conteúdo Programático")
conteudo_input = st.text_area("Descreva os tópicos que pretende trabalhar (IA organizará):")

# --- PROCESSAMENTO DO DOCUMENTO ---
def gerar_plano_docx():
    doc = Document()
    
    # Estilo de Título
    h = doc.add_heading('PLANO DE ENSINO INTELIGENTE', 0)
    
    # Seção 1
    doc.add_heading('1. IDENTIFICAÇÃO', level=1)
    doc.add_paragraph(f"Disciplina: {nome_disc}\nProfessor: {prof_resp}\nCarga Horária: {ch}\nNatureza: {natureza}")
    
    # Seção 3 e 4 - Objetivos (IA)
    doc.add_heading('3. OBJETIVO GERAL', level=1)
    doc.add_paragraph(gerar_objetivo_geral(conteudo_input))
    
    doc.add_heading('4. OBJETIVOS ESPECÍFICOS', level=1)
    doc.add_paragraph("• Identificar estruturas e processos básicos;\n• Correlacionar achados laboratoriais;\n• Integrar conhecimentos teóricos à prática.")

    # Seção 6 - Matriz ENAMED
    doc.add_heading('6. ALINHAMENTO MATRIZ ENAMED (Portaria 478/2025)', level=1)
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    hdr = table.rows[0].cells
    hdr[0].text = 'Conteúdo'
    hdr[1].text = 'Competência'
    hdr[2].text = 'Área'
    hdr[3].text = 'Nível Cognitivo'
    
    for t in conteudo_input.split('\n')[:3]: # Simula as 3 primeiras linhas
        if t.strip():
            row = table.add_row().cells
            row[0].text = t
            row[1].text = "Manejo Clínico"
            row[2].text = "Clínica Médica"
            row[3].text = "Análise"

    # Seção 11 - Bibliografia
    doc.add_heading('11. BIBLIOGRAFIA', level=1)
    doc.add_paragraph("Básica: " + ", ".join(dados_base.get("bibliografia_b", ["Referência 1", "Referência 2"])))
    doc.add_paragraph("Complementar: " + ", ".join(dados_base.get("bibliografia_c", ["Ref A", "Ref B", "Ref C"])))

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()

# BOTÃO FINAL
if st.button("🚀 Gerar Plano de Ensino Completo"):
    if nome_disc != "Selecione...":
        arquivo = gerar_plano_docx()
        st.download_button(
            label="📥 Baixar Plano de Ensino (DOCX)",
            data=arquivo,
            file_name=f"Plano_{nome_disc}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error("Selecione uma disciplina para continuar.")
