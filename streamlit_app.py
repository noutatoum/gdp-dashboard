import streamlit as st
import random

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="SCAN FRONTIÈRE v1.0",
    page_icon="🛂",
    layout="centered"
)

# --- 2. DESIGN GRAPHIQUE MODERNE (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #333333; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #007BFF !important; text-align: center; font-weight: 800; text-transform: uppercase; }
    
    /* Boutons de réponse */
    div.stButton > button {
        width: 100%; border: none; border-radius: 12px; padding: 15px;
        background: linear-gradient(135deg, #007BFF 0%, #0056b3 100%);
        color: white !important; font-weight: bold; font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.2); transition: 0.3s;
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4); }

    /* Carte de Résultat (Dossier) */
    .id-card {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-left: 10px solid #007BFF;
    }
    .status-badge { background: #dcfce7; color: #166534; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES DES PERSONNAGES ---
PERSONNAGES = {
    "Perso ONG": {"nom": "Isabelle", "icon": "🏥", "biom": "Empathie: 98%", "info": "Humanitaire. Dossier prioritaire."},
    "Perso Touriste": {"nom": "Marc", "icon": "📸", "biom": "Stress: Bas", "info": "Voyageur standard. Aucune alerte."},
    "Perso hacker": {"nom": "Nour", "icon": "💻", "biom": "Activité: Intense", "info": "Expert Cyber. Matériel chiffré détecté."},
    "Perso garde-frontières": {"nom": "Isabelle S.", "icon": "👮", "biom": "Discipline: 100%", "info": "Transit officiel autorisé."},
    "Perso trafiquant": {"nom": "Inconnu", "icon": "📦", "biom": "Nervosité: Masquée", "info": "Comportement suspect détecté."},
    "Perso évasion fiscale": {"nom": "Jean-Pierre", "icon": "💰", "biom": "Arrogance: 10/10", "info": "Flux financiers suspects."},
    "Perso exil": {"nom": "Geoffrey", "icon": "🛡️", "biom": "État: Épuisement", "info": "Demande de protection internationale."},
    "Perso Ananas": {"nom": "Specimen X", "icon": "🍍", "biom": "Bio-Scan: Inconnu", "info": "Inexplicable. Ne répond à rien."},
    "Perso chercheur": {"nom": "Dr Thorne", "icon": "🔬", "biom": "Focus: Scientifique", "info": "Échantillons non identifiés."},
    "Perso artiste": {"nom": "Luna", "icon": "🎨", "biom": "Créativité: Élevée", "info": "Voyage pour résidence artistique."}
}

# --- 4. LES 10 QUESTIONS ---
QUESTIONS = [
    ("Motif principal de votre passage ?", [("Aide Humanitaire", "Perso ONG"), ("Vacances", "Perso Touriste"), ("Affaires", "Perso évasion fiscale"), ("Asile", "Perso exil")]),
    ("Objectif après la frontière ?", [("Installation", "Perso exil"), ("Transit", "Perso garde-frontières"), ("Recherche", "Perso chercheur"), ("Inconnu", "Perso Ananas")]),
    ("Ressources financières ?", [("Offshore", "Perso évasion fiscale"), ("Standard", "Perso Touriste"), ("Faibles", "Perso exil"), ("Crypto", "Perso hacker")]),
    ("Document présenté ?", [("Diplomatique", "Perso garde-frontières"), ("Biométrique", "Perso Touriste"), ("Abîmé", "Perso exil"), ("Aucun", "Perso trafiquant")]),
    ("Objets suspects ?", [("Aucun", "Perso garde-frontières"), ("Laptop chiffré", "Perso hacker"), ("Arme", "Perso trafiquant"), ("Échantillon bio", "Perso Ananas")]),
    ("Type de bagage ?", [("Luxe", "Perso évasion fiscale"), ("Sac à dos", "Perso Touriste"), ("Mallette technique", "Perso chercheur"), ("Rien", "Perso Ananas")]),
    ("Réaction au scanner ?", [("Calme", "Perso garde-frontières"), ("Nervosité", "Perso trafiquant"), ("Mépris", "Perso évasion fiscale"), ("Silence", "Perso Ananas")]),
    ("Profession ?", [("Artiste", "Perso artiste"), ("Agent d'État", "Perso garde-frontières"), ("Étudiant", "Perso Touriste"), ("Sans emploi", "Perso exil")]),
    ("Durée du séjour ?", [("Quelques jours", "Perso Touriste"), ("Indéfinie", "Perso chercheur"), ("Permanent", "Perso exil"), ("Quelques heures", "Perso garde-frontières")]),
    ("Dernière zone visitée ?", [("Capitale", "Perso Touriste"), ("Zone de conflit", "Perso ONG"), ("Paradis fiscal", "Perso évasion fiscale"), ("Inconnue", "Perso Ananas")])
]

# --- 5. LOGIQUE DE SESSION ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {k: 0 for k in PERSONNAGES.keys()}

# --- 6. INTERFACE ---
st.markdown("<h1>🛂 SCAN FRONTIÈRE v1.0</h1>", unsafe_allow_html=True)
st.write("---")

if st.session_state.step < len(QUESTIONS):
    st.progress(st.session_state.step / len(QUESTIONS))
    q_text, options = QUESTIONS[st.session_state.step]
    st.subheader(q_text)
    
    # Boutons pour les réponses
    for text, perso_id in options:
        if st.button(text, key=text):
            st.session_state.scores[perso_id] += 5
            st.session_state.step += 1
            st.rerun()
else:
    # RÉSULTAT FINAL
    gagnant_id = max(st.session_state.scores, key=st.session_state.scores.get)
    p = PERSONNAGES[gagnant_id]

    st.markdown('<div class="id-card">', unsafe_allow_html=True)
    st.markdown('<span class="status-badge">✓ ANALYSE VALIDÉE</span>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<h1 style='font-size: 100px; margin:0;'>{p['icon']}</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"### NOM : {p['nom']}")
        st.write(f"**PROFIL :** {gagnant_id}")
        st.info(f"**INSIGHTS :** {p['info']}")
        st.error(f"**BIOMÉTRIE :** {p['biom']}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("NOUVEAU SCAN"):
        st.session_state.step = 0
        st.session_state.scores = {k: 0 for k in PERSONNAGES.keys()}
        st.rerun()
