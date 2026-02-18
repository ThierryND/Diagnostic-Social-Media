import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="ExpertSocial Diag V1", layout="wide")

# Initialisation des états
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'page' not in st.session_state:
    st.session_state.page = "login"

# --- GRILLE DE NOTATION ---
SCORING_GRID = {
    "Q1": {
        "0-300€": {"YT": 0, "FB": 1, "IG": 2, "TK": 3},
        "300-800€": {"YT": 1, "FB": 2, "IG": 3, "TK": 2},
        "800-1500€": {"YT": 2, "FB": 3, "IG": 2, "TK": 1},
        "1500€+": {"YT": 3, "FB": 2, "IG": 2, "TK": 1}
    },
    "Q2": {
        "0-2h": {"YT": 0, "FB": 3, "IG": 1, "TK": 1},
        "2-4h": {"YT": 1, "FB": 2, "IG": 2, "TK": 2},
        "4-7h": {"YT": 2, "FB": 1, "IG": 3, "TK": 2},
        "7-10h": {"YT": 3, "FB": 1, "IG": 2, "TK": 2},
        "10h+": {"YT": 3, "FB": 0, "IG": 1, "TK": 3}
    },
    "Q3": {
        "Débutant": {"YT": 0, "FB": 3, "IG": 2, "TK": 2},
        "Intermédiaire": {"YT": 1, "FB": 2, "IG": 3, "TK": 3},
        "Avancé": {"YT": 3, "FB": 1, "IG": 2, "TK": 2},
        "Expert": {"YT": 3, "FB": 0, "IG": 1, "TK": 1}
    },
    "Q6": {
        "Blocage total": {"YT": -20, "FB": 5, "IG": 0, "TK": -20},
        "Peu à l'aise": {"YT": 0, "FB": 3, "IG": 2, "TK": 1},
        "Assez à l'aise": {"YT": 2, "FB": 1, "IG": 3, "TK": 3},
        "Très à l'aise": {"YT": 4, "FB": 0, "IG": 2, "TK": 5}
    },
    "Q13": {
        "Notoriété locale": {"YT": 0, "FB": 4, "IG": 2, "TK": 1},
        "Acquisition clients": {"YT": 1, "FB": 2, "IG": 4, "TK": 3},
        "Recrutement": {"YT": 2, "FB": 2, "IG": 2, "TK": 4},
        "Expertise": {"YT": 5, "FB": 1, "IG": 1, "TK": 0}
    },
    "Q14": {
        "18-25": {"YT": 1, "FB": 0, "IG": 2, "TK": 5},
        "25-35": {"YT": 2, "FB": 1, "IG": 4, "TK": 3},
        "35-50": {"YT": 2, "FB": 4, "IG": 3, "TK": 1},
        "50-65": {"YT": 1, "FB": 5, "IG": 1, "TK": 0},
        "Multi": {"YT": 3, "FB": 2, "IG": 2, "TK": 2}
    },
    "Q18": {
        "Quartier/Ville": {"YT": 0, "FB": 5, "IG": 3, "TK": 1},
        "Région": {"YT": 1, "FB": 4, "IG": 3, "TK": 2},
        "National": {"YT": 3, "FB": 2, "IG": 4, "TK": 4},
        "International": {"YT": 5, "FB": 1, "IG": 3, "TK": 3}
    },
    "Q20": {
        "Vidéo courte": {"YT": 1, "FB": 1, "IG": 3, "TK": 5},
        "Vidéo longue": {"YT": 5, "FB": 1, "IG": 0, "TK": 0},
        "Visuels+Texte": {"YT": 0, "FB": 4, "IG": 5, "TK": 0},
        "Texte long": {"YT": 0, "FB": 5, "IG": 1, "TK": 0}
    },
    "Q23": {
        "100% Actu": {"YT": 0, "FB": 3, "IG": 4, "TK": 5},
        "Mixte": {"YT": 3, "FB": 3, "IG": 3, "TK": 3},
        "100% Evergreen": {"YT": 5, "FB": 1, "IG": 1, "TK": 0}
    },
    "Q26": {
        "Très forte": {"YT": 0, "FB": 3, "IG": 1, "TK": -2},
        "Moyenne": {"YT": 2, "FB": 2, "IG": 2, "TK": 1},
        "Aucune": {"YT": 3, "FB": 0, "IG": 3, "TK": 5}
    },
    "Q31": {
        "Détaché": {"YT": 1, "FB": 2, "IG": 3, "TK": 5},
        "Moyen": {"YT": 3, "FB": 3, "IG": 3, "TK": 2},
        "Perfectionniste bloquant": {"YT": 4, "FB": 1, "IG": 2, "TK": -3}
    }
}

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004aad; color: white; }
    .stSelectbox, .stRadio { background-color: white; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE D'AUTHENTIFICATION ---
def login_page():
    st.title("Accès Interface Multigestion")
    st.subheader("Outil de diagnostic pour Experts-Comptables")
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            user = st.text_input("Identifiant")
            pw = st.text_input("Mot de passe", type="password")
            if st.button("Se connecter"):
                if user == "admin" and pw == "expert2024":
                    st.session_state.auth = True
                    st.session_state.page = "diag"
                    st.rerun()
                else:
                    st.error("Identifiants incorrects (Essai : admin / expert2024)")

# --- MOTEUR DE SCORING ACTUALISÉ ---
def calculate_scoring(r):
    # On sépare les scores par phase pour les graphiques
    phases_scores = {
        "Phase 1 : Ressources": {"YouTube": 0, "Facebook": 0, "Instagram": 0, "TikTok": 0},
        "Phase 2 : Stratégie": {"YouTube": 0, "Facebook": 0, "Instagram": 0, "TikTok": 0},
        "Phase 3 : Psychologie": {"YouTube": 0, "Facebook": 0, "Instagram": 0, "TikTok": 0}
    }
    
    mapping = {"YT": "YouTube", "FB": "Facebook", "IG": "Instagram", "TK": "TikTok"}
    
    for q_id, options in SCORING_GRID.items():
        user_answer = r.get(q_id.lower())
        if user_answer in options:
            points = options[user_answer]
            # Détermination de la phase selon le numéro de question
            q_num = int(q_id[1:])
            if q_num <= 12: phase = "Phase 1 : Ressources"
            elif q_num <= 24: phase = "Phase 2 : Stratégie"
            else: phase = "Phase 3 : Psychologie"
            
            for platform_key, score_val in points.items():
                phases_scores[phase][mapping[platform_key]] += score_val

    # Calcul du total pour déterminer le gagnant
    total_scores = {"YouTube": 0, "Facebook": 0, "Instagram": 0, "TikTok": 0}
    for p_scores in phases_scores.values():
        for plat, val in p_scores.items():
            total_scores[plat] += val
            
    return total_scores, phases_scores

# --- PAGE DIAGNOSTIC ---
def diag_page():
    st.title("Questionnaire de Diagnostic")
    st.info("Répondez sincèrement. Ce diagnostic prend environ 5 minutes.")

    with st.form("main_survey"):
        # PHASE 1
        st.header("Phase 1 : Analyse du Profil (Ressources)")
        col1, col2 = st.columns(2)
        with col1:
            q1 = st.selectbox("Q1 : Budget marketing mensuel", ["0-300€", "300-800€", "800-1500€", "1500€+"])
            q2 = st.selectbox("Q2 : Temps hebdomadaire disponible", ["0-2h", "2-4h", "4-7h", "7-10h", "10h+"])
            q3 = st.select_slider("Q3 : Compétences techniques", ["Débutant", "Intermédiaire", "Avancé", "Expert"])
            q4 = st.selectbox("Q4 : Équipement disponible", ["Smartphone seul", "Kit lumières/micro", "Studio complet"])
            q5 = st.selectbox("Q5 : Aide disponible", ["Seul", "Alternant/Stagiaire", "Agence/Équipe"])
            q6 = st.radio("Q6 : Confort avec la vidéo (Critique)", ["Blocage total", "Peu à l'aise", "Assez à l'aise", "Très à l'aise"])
        with col2:
            q7 = st.select_slider("Q7 : Capacité d'apprentissage", ["Faible", "Moyenne", "Élevée"])
            q8 = st.select_slider("Q8 : Tolérance risque échec", ["Très faible", "Modérée", "Élevée"])
            q9 = st.selectbox("Q9 : Expérience passée réseaux", ["Aucune", "Utilisateur perso", "Créateur régulier"])
            q10 = st.selectbox("Q10 : Disponibilité commentaires", ["0-15min/j", "15-30min/j", "30-60min/j", "60min+"])
            q11 = st.radio("Q11 : Investissement pub payante", ["Non", "Peut-être", "Budget dédié"])
            q12 = st.selectbox("Q12 : Image de marque", ["Pas d'image", "En création", "Établie stricte"])

        # PHASE 2
        st.header("Phase 2 : Stratégie & Positionnement")
        col3, col4 = st.columns(2)
        with col3:
            q13 = st.selectbox("Q13 : Objectif principal", ["Notoriété locale", "Acquisition clients", "Recrutement", "Expertise"])
            q14 = st.selectbox("Q14 : Cible démographique", ["18-25", "25-35", "35-50", "50-65", "Multi"])
            q15 = st.selectbox("Q15 : Typologie clients", ["Auto-entrepreneurs", "TPE", "PME", "Grands comptes"])
            q16 = st.selectbox("Q16 : Spécialisation", ["Généraliste", "2-3 secteurs", "Niche unique"])
            q17 = st.text_input("Q17 : Secteurs spécifiques (ex: BTP, Tech...)", "Général")
            q18 = st.selectbox("Q18 : Zone géographique", ["Quartier/Ville", "Région", "National", "International"])
        with col4:
            q19 = st.selectbox("Q19 : Urgence résultats", ["< 3 mois", "3-6 mois", "6-12 mois", "12 mois+"])
            q20 = st.selectbox("Q20 : Type de contenu préféré", ["Vidéo courte", "Vidéo longue", "Visuels+Texte", "Texte long"])
            q21 = st.selectbox("Q21 : Fréquence publication", ["1x/sem", "2-3x/sem", "Quotidien"])
            q22 = st.selectbox("Q22 : Tonalité marque", ["Corporate", "Pro accessible", "Amical", "Disruptif"])
            q23 = st.select_slider("Q23 : Rapport Actu/Evergreen", ["100% Actu", "Mixte", "100% Evergreen"])
            q24 = st.radio("Q24 : Importance communauté", ["Secondaire", "Importante", "Priorité absolue"])

        # PHASE 3
        st.header("Phase 3 : Contraintes & Facteurs Bloquants")
        col5, col6 = st.columns(2)
        with col5:
            q25 = st.select_slider("Q25 : Déontologie perçue", ["Très restrictive", "Modérée", "Peu contraignante"])
            q26 = st.select_slider("Q26 : Crainte jugement pro", ["Très forte", "Moyenne", "Aucune"])
            q27 = st.radio("Q27 : Soutien entourage pro", ["Opposé", "Neutre", "Soutenant"])
            q28 = st.radio("Q28 : Complexité technique perçue", ["Insurmontable", "Difficile", "Facile"])
        with col6:
            q29 = st.radio("Q29 : Peur surcharge travail", ["Très forte", "Modérée", "Aucune"])
            q30 = st.selectbox("Q30 : Expériences passées", ["Échec cuisant", "Neutre", "Réussite partielle"])
            q31 = st.select_slider("Q31 : Niveau autocritique", ["Détaché", "Moyen", "Perfectionniste bloquant"])
            q32 = st.radio("Q32 : Capacité à déléguer", ["Impossible", "Difficile", "Facile"])

        if st.form_submit_button("LANCER L'ANALYSE"):
            responses = {
                'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6,
                'q7': q7, 'q8': q8, 'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                'q13': q13, 'q14': q14, 'q15': q15, 'q16': q16, 'q17': q17, 'q18': q18,
                'q19': q19, 'q20': q20, 'q21': q21, 'q22': q22, 'q23': q23, 'q24': q24,
                'q25': q25, 'q26': q26, 'q27': q27, 'q28': q28, 'q29': q29, 'q30': q30,
                'q31': q31, 'q32': q32
            }
            st.session_state.results = calculate_scoring(responses)
            st.session_state.page = "results"
            st.rerun()

# --- PAGE RÉSULTATS ---
def results_page():
    st.title("Analyse de votre Potentiel Social Media")
    
    total_scores = st.session_state.results[0]
    phases_data = st.session_state.results[1]
    winner = max(total_scores, key=total_scores.get)

    # Header de recommandation
    st.success(f"### Recommandation Prioritaire : **{winner}**")
    
    # Création des 3 graphiques
    for phase_name, scores in phases_data.items():
        st.subheader(phase_name)
        
        # Préparation des données pour Plotly
        df_plot = pd.DataFrame({
            'Plateforme': list(scores.keys()),
            'Score': list(scores.values())
        }).sort_values(by='Score', ascending=True)

        fig = go.Figure(go.Bar(
            x=df_plot['Score'],
            y=df_plot['Plateforme'],
            orientation='h',
            marker_color=['#004aad' if p != winner else '#FF4B4B' for p in df_plot['Plateforme']]
        ))

        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="Points accumulés",
            yaxis_title=None
        )
        
        st.plotly_chart(fig, use_container_width=True)

    if st.button("Relancer un diagnostic"):
        st.session_state.page = "diag"
        st.rerun()

# --- ROUTAGE ---
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "diag":
    diag_page()
elif st.session_state.page == "results":
    results_page()
