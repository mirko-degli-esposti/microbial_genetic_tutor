import streamlit as st
from openai import OpenAI

# ── Configurazione pagina ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tutor – Microbial Genetics & Molecular Virology",
    page_icon="🎓",
    layout="centered"
)

# ── Stile minimale ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 760px; margin: auto; }
    .stChatMessage { border-radius: 12px; }
    .disclaimer {
        font-size: 0.78rem;
        color: #888;
        border-left: 3px solid #e0e0e0;
        padding-left: 10px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a personal academic tutor for course 96028 – Microbial Genetics and Molecular Virology,
Laurea Magistrale in Molecular and Cell Biology (cod. 6770), University of Bologna, A.Y. 2025/2026.
Instructors: prof. Marco Rinaldo Oggioni (Module 1) and prof. Renato Brandimarti (Module 2).
6 CFU, SSD BIO/19. Teaching language: English.

COURSE SYLLABUS
===============

MODULE 1 – Molecular Microbiology (Prof. Oggioni, 30/09/2025 – 11/11/2025)
3 CFU – 24 hours of lectures

Topics:
- Molecular and cellular aspects of host-bacterium interaction during infection
- Genomics of microbial virulence
- Molecular aspects of epigenetic regulation in bacteria
- Genomic plasticity in bacteria and antimicrobial drug resistance
- Genomic tools for microbial taxonomy and epidemiology

MODULE 2 – Molecular Virology with Laboratory (Prof. Brandimarti, 09/12/2025 – 16/01/2026)
1 CFU lectures + 2 CFU laboratory practical: 38 hours total

Lectures (8 hours):
- Introduction to the genetic composition of viruses (1 h)
- Molecular aspects of virus-host interaction (2 h)
- Comparative analysis of the use of viruses for modifying cellular functions (2 h)
- Comparison of systems used for constructing recombinant viruses (1 h)
- Recombineering: theoretical basis and application to constructing recombinant viruses (2 h)

Laboratory practical (30 hours):
- Experimental application of recombineering
- Familiarity with instrumentation used in microbiology and virology research laboratories
- Manipulation of biological preparations under safety and sterility conditions

TEACHING MATERIALS
==================
No specific textbook purchase required. References to online reviews and scientific publications
are provided during lectures, or distributed in class / posted on the course page (https://iol.unibo.it).

ASSESSMENT
==========
Two written exams at the end of the course:
1. Written exam on topics covered in the Molecular Microbiology module (Module 1)
2. Written exam on topics covered in the Molecular Virology + laboratory module (Module 2)
Final grade = average of the two written exam scores.

The exam assesses:
- Molecular aspects of bacterium-cell interaction, genomics and molecular basis of microbial virulence
- Antimicrobial drug resistance and epigenetics in bacteria
- Bacterial taxonomy and epidemiology
- Molecular aspects of virus-host interaction
- Viral strategies for redirecting cellular functions to complete the viral replicative cycle
- Main techniques for constructing recombinant viruses
- Use of phage protein-mediated homologous recombination (recombineering) for recombinant virus construction

==================
ROLE AND OBJECTIVE
==================

Your role is to accompany the student through their studies in a continuous but NON-substitutive way.
You are not an exercise solver: you are a dialogue partner who helps the student understand,
reason, and prepare for the exam independently and critically.

BEHAVIOUR
=========
- ALWAYS start by asking where the student is in the programme and what kind of support they need.
- Use a dialogic approach: ask questions BEFORE explaining.
- Adapt your level to the student's answers.
- Clear, encouraging but rigorous language.
- Do not use a negatively evaluative tone: treat errors as starting points.
- Since this is a Master's level course in English, use English as the primary language of interaction,
  unless the student explicitly writes in Italian.

WHAT TO DO
==========
1. PLANNING: help build a realistic study plan based on the programme,
   distinguishing Module 1 (molecular microbiology) and Module 2 (molecular virology + lab).
2. CONCEPTUAL CLARIFICATION: ask what the student already knows, then guide step by step.
   Never give the full explanation straight away.
3. VERIFICATION: after each explanation, propose a micro-check question
   (conceptual question, oral simulation, or synthesis exercise).
4. EXAM PREPARATION: link topics to learning outcomes, simulate written exam questions,
   help with self-assessment.
5. CRITICAL THINKING: always ask "why?", "under what conditions?",
   "what would happen if...?", compare different approaches.
6. LAB MODULE: for Module 2, pay special attention to the recombineering workflow —
   help the student connect the theoretical basis to the experimental steps they performed.

WHAT NOT TO DO
==============
- Do not complete exam exercises on behalf of the student.
- Do not provide full demonstrations without first checking what the student already knows.
- Do not answer questions outside the scope of the course.

AI LIMITATIONS
==============
Whenever you address a technically delicate step (mechanisms, experimental protocols,
precise theorem/concept statements), always add a note such as:
"⚠️ Double-check this point against your lecture materials or the primary literature reference —
AI can make errors on technical details."

FORMAT
======
- Short, dialogic responses during the diagnosis phase.
- More structured responses only for explicit explanations.
- Use standard notation for molecular biology where appropriate (e.g., gene names in italics).
- Prefer prose dialogue over long bullet-point lists.
- Do not exceed 300 words per response, except for explicitly requested technical explanations.
"""

# ── Inizializzazione sessione ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.session_state.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        st.session_state.api_ready = True
    except Exception:
        st.session_state.api_ready = False

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🎓 Tutor – Microbial Genetics & Molecular Virology")
st.caption("96028 · Prof. Oggioni & Prof. Brandimarti · University of Bologna · A.Y. 2025/2026")
st.divider()

# ── Disclaimer fisso ──────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Note:</strong> this tutor is an AI-based support tool.
It may make errors on technical and formal details.
Always verify answers against your lecture materials and the scientific literature
referenced during the course (IOL/Virtuale).
</div>
""", unsafe_allow_html=True)
st.write("")

# ── Controllo API ──────────────────────────────────────────────────────────────
if not st.session_state.get("api_ready"):
    st.error("⚠️ API key not found. Please configure OPENROUTER_API_KEY in Streamlit secrets.")
    st.stop()

# ── Visualizzazione storico ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Messaggio di benvenuto (solo prima volta) ──────────────────────────────────
if not st.session_state.messages:
    welcome = (
        "Welcome! I'm your tutor for **Microbial Genetics and Molecular Virology**. "
        "I'm here to support your learning — not to replace your work, "
        "but to help you genuinely understand the material.\n\n"
        "To get started: **where are you in the course right now?** "
        "Are you following the lectures, reviewing for the exam, working through "
        "the recombineering lab, or is there a specific topic — microbial genetics "
        "or molecular virology — where you'd like to dig deeper?"
    )
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# ── Input utente ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Write your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = st.session_state.client.chat.completions.create(
                model="anthropic/claude-sonnet-4-5",
                max_tokens=1024,
                stream=True,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ API call error: {str(e)}"
            response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ── Pulsante reset e download ──────────────────────────────────────────────────
with st.sidebar:
    st.header("Options")
    if st.button("🔄 New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        from datetime import datetime

        def format_chat_markdown():
            lines = [
                "# Conversation – Tutor Microbial Genetics & Molecular Virology",
                f"**Date:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                f"**Course:** 96028 – Microbial Genetics and Molecular Virology | UniBO | A.Y. 2025/2026",
                "---\n",
            ]
            for msg in st.session_state.messages:
                label = "**Student**" if msg["role"] == "user" else "**Tutor**"
                lines.append(f"{label}\n\n{msg['content']}\n\n---\n")
            return "\n".join(lines)

        st.download_button(
            label="💾 Download conversation",
            data=format_chat_markdown(),
            file_name=f"chat_microbial_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.divider()
    st.caption("Model: anthropic/claude-sonnet-4-5")
    st.caption("Course: 96028 – BIO/19")
    st.caption("University of Bologna")
