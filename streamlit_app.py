
import streamlit as st

# 1. Config de base
st.set_page_config(page_title="SCAN FRONTIÈRE", page_icon="🛂")

# 2. Design
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; background: #007BFF; color: white; font-weight: bold; border: none; }
    .id-card { background: white; padding: 25px; border-radius: 15px; border-left: 10px solid #007BFF; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialisation de la session
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

# 4. Questions
questions = [
    ("Motif du passage ?", ["Humanitaire", "Tourisme", "Affaires", "Asile"]),
    ("Objet suspect ?", ["Aucun", "Électronique", "Arme", "Bio"]),
    ("Durée du séjour ?", ["3 jours", "1 mois", "Permanent", "1 heure"])
]

st.title("🛂 SCAN FRONTIÈRE v1.0")

if st.session_state.question_index < len(questions):
    st.write(f"Question {st.session_state.question_index + 1} / {len(questions)}")
    q_text, options = questions[st.session_state.question_index]
    
    st.subheader(q_text)
    for opt in options:
        if st.button(opt):
            st.session_state.question_index += 1
            st.rerun()
else:
    st.success("ANALYSE TERMINÉE")
    st.markdown("""
        <div class="id-card">
            <h3>DOSSIER : NOUR AL-FAYED</h3>
            <p><b>RÉSULTAT :</b> ANALYSE VALIDÉE</p>
            <p><b>PROFIL :</b> EXPERT IA / HACKER</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("RESCANNER"):
        st.session_state.question_index = 0
        st.rerun()
