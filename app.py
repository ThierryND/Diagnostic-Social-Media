
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

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004aad; color: white; }
    .stSelectbox, .stRadio { background-color: white; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html =True)

# --- LOGIQUE D'AUTHENTIFICATION ---
def login_page():
    st.title("🔐 Accès Interface Multigestion")
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

# --- MOTEUR DE SCORING ---
def calculate_scoring(r):
    # Initialisation
    scores = {"TikTok": 0, "Instagram": 0, "Facebook": 0, "YouTube": 0}
    eliminated = []

    # --- PHASE 1 (Coeff 1.0) ---
    # Logique simplifiée : on simule l'attribution de points
    if r['q1'] == "1500€+": scores["YouTube"] += 10; scores["TikTok"] += 10
    if r['q6'] == "Blocage total": eliminated.extend(["TikTok", "YouTube"])
    
    # --- PHASE 2 (Coeff 1.5) ---
    c2 = 1.5
    if r['q13'] == "Expertise": scores["YouTube"] += 10 * c2
    if r['q14'] == "18-25": scores["TikTok"] += 10 * c2
    if r['q15'] == "TPE": scores["Facebook"] += 8 * c2; scores["Instagram"] += 8 * c2

    # --- PHASE 3 (Malus 0.8) ---
    m = 0.8
    if r['q31'] == "Perfectionniste bloquant":
        for k in scores: scores[k] -= 15 * m

    # Application des éliminations
    for p in eliminated: scores[p] = 0
    return scores, eliminated

# --- PAGE DIAGNOSTIC (32 QUESTIONS) ---
def diag_page():
    st.title("📋 Questionnaire de Diagnostic")
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
            # Collecte des données
            responses = {
                            'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6,
                            'q7': q7, 'q8': q8, 'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                            'q13': q13, 'q14': q14, 'q15': q15, 'q16': q16, 'q17': q17, 'q18': q18,
                            'q19': q19, 'q20': q20, 'q21': q21, 'q22': q22, 'q23': q23, 'q24': q24,
                            'q25': q25, 'q26': q26, 'q27': q27, 'q28': q28, 'q29': q29, 'q30': q30,
                            'q31': q31, 'q32': q32
                        }# Capture toutes les variables q1...q32

            #responses = locals() ancien code qui Capture toutes les variables q1...q32
            st.session_state.results, st.session_state.eliminated = calculate_scoring(responses)
            st.session_state.page = "results"
            st.rerun()

# --- PAGE RÉSULTATS ---
def results_page():
    st.title("🎯 Résultat de votre Diagnostic Stratégique")
    scores = st.session_state.results
    eliminated = st.session_state.eliminated
    
    # Calcul plateforme gagnante
    winner = max(scores, key=scores.get)
    score_final = scores[winner]
    compatibility = min(98, int((score_final / 60) * 100)) # Normalisation pour affichage

    # Affichage Header
    st.balloons()
    col_res1, col_res2 = st.columns([1,1])
    
    with col_res1:
        st.success(f"## Recommandation : {winner}")
        st.metric("Compatibilité", f"{compatibility}%")
        st.write("**Pourquoi cette plateforme ?** Votre profil montre une adéquation entre vos ressources temps/budget et l'audience cible de ce réseau.")

    with col_res2:
        # Graphique
        df = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
        fig = go.Figure(data=[go.Bar(x=list(scores.keys()), y=list(scores.values()), marker_color='#004aad')])
        fig.update_layout(title="Comparatif des potentiels", height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Plateformes éliminées
    if eliminated:
        st.warning(f"🚫 Plateformes exclues de la stratégie : {', '.join(eliminated)} (Raison : Contraintes techniques ou blocages vidéo)")

    # Plan d'Action
    st.header("📌 Votre Plan d'Action V1")
    t1, t2, t3 = st.tabs(["Action Immédiate", "Contenu", "KPIs"])
    with t1:
        st.write(f"- Création/Optimisation du profil sur **{winner}**")
        st.write("- Paramétrage des outils de sécurité et déontologie")
    with t2:
        st.write("- Production de 2 publications piliers par semaine")
        st.write("- Utilisation des thématiques identifiées en Phase 2")
    with t3:
        st.write("- Objectif : 100 abonnés qualifiés en 30 jours")

    if st.button("🔄 Refaire un diagnostic"):
        st.session_state.page = "diag"
        st.rerun()

# --- ROUTAGE ---
if not st.session_state.auth:
    login_page()
elif st.session_state.page == "diag":
    diag_page()
elif st.session_state.page == "results":
    results_page()
