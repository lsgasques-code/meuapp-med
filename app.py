import streamlit as st
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import datetime
import io

# --- BANCO DE DADOS TÉCNICO (CONFORMIDADE) ---
def obter_dados_conformidade():
    return {
        "DCN_TEXTO": "Em conformidade com a Resolução nº 3/2025, esta disciplina foca na integração entre bases moleculares e prática clínica, priorizando os domínios Cognitivo (Saber), Psicomotor (Fazer) e Atitudinal (Ser).",
        "REGRAS_AVALIACAO": "70% Prova Teórico-Prática (Plataforma PreparaEdu) e 30% Atividades Formativas (Busca ativa no UpToDate e Seminários).",
        "REMEDIACO": "Conforme o Art. 37 das DCNs, alunos com desempenho insuficiente serão encaminhados ao Programa de Monitoria (apoio aluno-aluno) para revisão de conceitos e habilidades técnicas."
    }

# --- INTERFACE ---
st.set_page_config(page_title="Gerador Pro de Planos - Medicina", layout="centered")
st.title("🏥 Gerador de Plano de Ensino Profissional")
st.markdown("---")

# Perguntas para o Professor
professor = st.text_input("Nome do Docente:", placeholder="Ex: Prof. Dr. Luciano Gasques")
disciplina = st.text_input("Nome da Disciplina:", placeholder="Ex: Biologia Molecular Aplicada")
periodo = st.selectbox("Duração da Disciplina:", ["20 Semanas (Semestral)", "40 Semanas (Anual)"])
temas_brutos = st.text_area("Liste os temas centrais (um por linha):", placeholder="Ex: Replicação do DNA\nMutagênese e Câncer\nPCR em Tempo Real", height=150)

# --- GERADOR DE DOCUMENTO (LÓGICA DO PROTÓTIPO) ---
def criar_documento_profissional(p, d, per, t):
    doc = Document()
    dados = obter_dados_conformidade()
    
    # Cabeçalho
    title = doc.add_heading(f'PLANO DE ENSINO: {d.upper()}', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p1 = doc.add_paragraph()
    p1.add_run(f'Docente Responsável: ').bold = True
    p1.add_run(p)
    p1.add_run(f'\nPeríodo: ').bold = True
    p1.add_run(per)
    p1.add_run(f' | Data de Geração: {datetime.date.today().strftime("%d/%m/%Y")}')

    # 1. Ementa e Objetivos
    doc.add_heading('1. Ementa e Objetivos (DCN 2025)', level=1)
    doc.add_paragraph(dados["DCN_TEXTO"])
    
    # 2. Matriz ENAMED (Tabela Profissional)
    doc.add_heading('2. Mapeamento ENAMED (Portaria 478/2025)', level=1)
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Unidade Temática'
    hdr_cells[1].text = 'Eixo ENAMED'
    hdr_cells[2].text = 'Cenário de Prática / SUS'
    
    for tema in t.split('\n'):
        if tema.strip():
            row = table.add_row().cells
            row[0].text = tema.strip()
            row[1].text = "Eixo XVII / XX" # Classificação automática sugerida
            row[2].text = "Laboratório / Ambulatório"

    # 3. Metodologia e Recursos
    doc.add_heading('3. Metodologia e Recursos Tecnológicos', level=1)
    doc.add_paragraph("A disciplina utiliza infraestrutura tecnológica de ponta:")
    p_res = doc.add_paragraph(style='List Bullet')
    p_res.add_run("Chromebooks: Para atividades de pesquisa e quizzes semanais.\n")
    p_res.add_run("UpToDate: Base principal para Medicina Baseada em Evidências.\n")
    p_res.add_run("Monitoria Oficial: Suporte verticalizado entre estudantes.")

    # 4. Avaliação
    doc.add_heading('4. Sistema de Avaliação', level=1)
    doc.add_paragraph(dados["REGRAS_AVALIACAO"])

    # 5. Remediação
    doc.add_heading('5. Plano de Ação e Recuperação', level=1)
    doc.add_paragraph(dados["REMEDIACO"])

    # Finalização do arquivo para download
    target = io.BytesIO()
    doc.save(target)
    return target.getvalue()

# --- BOTÃO DE AÇÃO ---
if st.button("🚀 GERAR PLANO COMPLETO (DOCX)"):
    if professor and disciplina and temas_brutos:
        conteudo_arquivo = criar_documento_profissional(professor, disciplina, periodo, temas_brutos)
        
        st.success("Plano de Ensino estruturado com sucesso!")
        st.download_button(
            label="📥 Baixar Plano de Ensino Oficial",
            data=conteudo_arquivo,
            file_name=f"Plano_Ensino_{disciplina.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error("Por favor, preencha todos os campos para garantir a conformidade do plano.")
