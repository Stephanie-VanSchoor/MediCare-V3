import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta
import uuid
import hashlib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="🏥 MediCare Odoo", layout="wide", initial_sidebar_state="expanded")

# ========== BASE DE DONNÉES ==========
def init_db():
    conn = sqlite3.connect('medicare.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, password TEXT, role TEXT, nom TEXT, prenom TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prenom TEXT, date_naissance TEXT, sexe TEXT, telephone TEXT, 
        email TEXT, adresse TEXT, allergies TEXT, antecedents TEXT, date_creation TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS medecins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prenom TEXT, specialite TEXT, telephone TEXT, email TEXT, disponible TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS rdvs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, medecin_id INTEGER, date TEXT, heure TEXT, motif TEXT, statut TEXT, notes TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS consultations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, medecin_id INTEGER, date TEXT, diagnostic TEXT, prescription TEXT, notes TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS factures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, montant REAL, date_emission TEXT, date_echeance TEXT, statut TEXT, description TEXT
    )''')
    
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role, nom, prenom) VALUES (?,?,?,?,?)",
                  ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'Admin', 'Admin', 'System'))
    
    conn.commit()
    conn.close()

init_db()

# ========== FONCTIONS ==========
def get_db():
    return sqlite3.connect('medicare.db')

def execute_query(query, params=()):
    conn = get_db()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def fetch_query(query, params=()):
    conn = get_db()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# ========== AUTH ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

def login(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    df = fetch_query("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    if len(df) > 0:
        st.session_state.logged_in = True
        st.session_state.user = df.iloc[0].to_dict()
        return True
    return False

# ========== DESIGN ODOO MEDICAL ULTRA-PRO ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    
    /* ===== SIDEBAR ODOO ===== */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a2332 0%, #0d1520 100%) !important;
        padding: 20px 16px !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    
    /* Logo Odoo Style */
    .odoo-logo {
        text-align: center;
        padding: 16px 0 24px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 20px;
    }
    
    .odoo-logo .icon {
        font-size: 42px;
        display: block;
        margin-bottom: 8px;
    }
    
    .odoo-logo h1 {
        color: #ffffff !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }
    
    .odoo-logo .sub {
        color: #6b8cae !important;
        font-size: 11px !important;
        font-weight: 400 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 4px;
    }
    
    /* Menu Odoo */
    .css-1d391kg .stRadio label {
        color: #8a9bb5 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        padding: 10px 16px !important;
        border-radius: 8px !important;
        transition: all 0.25s ease !important;
        margin: 2px 0 !important;
        border-left: 3px solid transparent !important;
    }
    
    .css-1d391kg .stRadio label:hover {
        background: rgba(255,255,255,0.06) !important;
        color: #ffffff !important;
        border-left-color: #6b8cae !important;
    }
    
    .css-1d391kg .stRadio label[data-baseweb="radio"] {
        background: rgba(107, 140, 174, 0.12) !important;
        color: #ffffff !important;
        border-left-color: #6b8cae !important;
        font-weight: 600 !important;
    }
    
    /* User info sidebar */
    .sidebar-user {
        padding: 16px;
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
        margin-top: 16px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    
    .sidebar-user .name {
        color: #ffffff;
        font-weight: 600;
        font-size: 14px;
    }
    
    .sidebar-user .role {
        color: #6b8cae;
        font-size: 12px;
        font-weight: 400;
    }
    
    .sidebar-user .badge-role {
        display: inline-block;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 600;
        background: #6b8cae;
        color: #1a2332;
        margin-top: 4px;
    }
    
    /* ===== ODOO CARDS ===== */
    .odoo-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #eef2f6;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .odoo-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6b8cae, #4a6a8a);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .odoo-card:hover {
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        transform: translateY(-2px);
        border-color: #dce3ec;
    }
    
    .odoo-card:hover::before {
        opacity: 1;
    }
    
    .odoo-card .card-icon {
        font-size: 28px;
        margin-bottom: 12px;
        display: inline-block;
    }
    
    .odoo-card .card-number {
        font-size: 34px;
        font-weight: 700;
        color: #1a2332;
        line-height: 1.1;
        letter-spacing: -1px;
    }
    
    .odoo-card .card-label {
        color: #6b7a8f;
        font-size: 13px;
        font-weight: 500;
        margin-top: 4px;
    }
    
    .odoo-card .card-trend {
        font-size: 11px;
        font-weight: 600;
        padding: 3px 14px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 10px;
    }
    
    .trend-up {
        background: #e8f5e9;
        color: #2e7d32;
    }
    
    .trend-down {
        background: #fce4ec;
        color: #c62828;
    }
    
    /* ===== TITRE ===== */
    .odoo-title {
        font-size: 22px;
        font-weight: 700;
        color: #1a2332;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 2px solid #eef2f6;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .odoo-title .badge {
        background: #eef2f6;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        color: #6b7a8f;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    
    /* ===== BOUTONS ===== */
    .stButton button {
        background: linear-gradient(135deg, #2c3e6b 0%, #1a2b4a 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 24px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(44, 62, 107, 0.2) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(44, 62, 107, 0.35) !important;
        background: linear-gradient(135deg, #1a2b4a 0%, #0d1520 100%) !important;
    }
    
    /* ===== BADGES ODOO ===== */
    .badge-odoo {
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
        letter-spacing: 0.2px;
    }
    
    .badge-primary { background: #e3f0ff; color: #1a56db; }
    .badge-success { background: #e6f7e6; color: #059669; }
    .badge-warning { background: #fff8e1; color: #d97706; }
    .badge-danger { background: #fde8e8; color: #dc2626; }
    .badge-info { background: #e0f2fe; color: #0284c7; }
    .badge-purple { background: #ede9fe; color: #7c3aed; }
    
    /* ===== TABLEAU ===== */
    .dataframe {
        border-radius: 8px !important;
        border: 1px solid #eef2f6 !important;
        overflow: hidden !important;
    }
    
    .dataframe thead th {
        background: #f8fafc !important;
        color: #1a2332 !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.3px !important;
        padding: 12px 16px !important;
        border-bottom: 2px solid #eef2f6 !important;
    }
    
    .dataframe tbody td {
        padding: 10px 16px !important;
        font-size: 13px !important;
        border-bottom: 1px solid #f1f4f8 !important;
        color: #1a2332 !important;
    }
    
    .dataframe tbody tr:hover {
        background: #f8fafc !important;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid #eef2f6 !important;
        font-weight: 600 !important;
        color: #1a2332 !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f4f8 !important;
        border-color: #dce3ec !important;
    }
    
    /* ===== INPUTS ===== */
    .stTextInput input, .stSelectbox select, .stTextArea textarea, .stDateInput input, .stNumberInput input {
        border-radius: 8px !important;
        border: 1px solid #dce3ec !important;
        padding: 8px 14px !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
        background: #ffffff !important;
        color: #1a2332 !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #6b8cae !important;
        box-shadow: 0 0 0 3px rgba(107, 140, 174, 0.15) !important;
        outline: none !important;
    }
    
    /* ===== METRIC ===== */
    .stMetric {
        background: white;
        padding: 16px 20px;
        border-radius: 10px;
        border: 1px solid #eef2f6;
    }
    
    .stMetric .stMetricLabel {
        color: #6b7a8f !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    
    .stMetric .stMetricValue {
        color: #1a2332 !important;
        font-weight: 700 !important;
        font-size: 28px !important;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        margin: 28px 0 !important;
        border: none !important;
        border-top: 1px solid #eef2f6 !important;
    }
    
    /* ===== LOGIN ===== */
    .login-box {
        max-width: 420px;
        margin: 60px auto;
        padding: 48px 40px;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 8px 48px rgba(0,0,0,0.06);
        border: 1px solid #eef2f6;
    }
    
    .login-box .logo {
        text-align: center;
        margin-bottom: 32px;
    }
    
    .login-box .logo .icon {
        font-size: 48px;
        display: block;
    }
    
    .login-box .logo h1 {
        color: #1a2332;
        font-size: 26px;
        font-weight: 700;
        margin: 8px 0 4px 0;
    }
    
    .login-box .logo p {
        color: #6b7a8f;
        font-size: 14px;
        margin: 0;
    }
    
    .login-box .stButton button {
        width: 100% !important;
        padding: 12px !important;
        font-size: 15px !important;
    }
    
    /* ===== CONTAINER ===== */
    .main-container {
        padding: 20px 32px 32px 32px;
    }
    
    @media (max-width: 768px) {
        .main-container {
            padding: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========== LOGIN ==========
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-box">
        <div class="logo">
            <span class="icon">🏥</span>
            <h1>MediCare</h1>
            <p>Gestion Médicale Professionnelle</p>
        </div>
    """, unsafe_allow_html=True)
    
    username = st.text_input("Nom d'utilisateur", placeholder="admin", key="login_user")
    password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_pass")
    
    if st.button("🔐 Se connecter", use_container_width=True):
        if login(username, password):
            st.success("✅ Connexion réussie")
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")
    
    st.markdown("""
    <p style="text-align: center; color: #6b7a8f; font-size: 12px; margin-top: 20px;">
        🔑 admin / admin123
    </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div class="odoo-logo">
        <span class="icon">🏥</span>
        <h1>MediCare</h1>
        <div class="sub">Medical Management</div>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("", [
        "📊 Tableau de bord",
        "👥 Patients",
        "👨‍⚕️ Médecins",
        "📅 Rendez-vous",
        "📋 Consultations",
        "💰 Factures",
        "📈 Statistiques",
        "⚙️ Administration"
    ])
    
    st.markdown("""
    <div class="sidebar-user">
        <div class="name">👤 {}</div>
        <div class="role">{}</div>
        <span class="badge-role">{}</span>
    </div>
    """.format(
        st.session_state.user.get('nom', '') + ' ' + st.session_state.user.get('prenom', ''),
        st.session_state.user.get('role', ''),
        st.session_state.user.get('role', '')
    ), unsafe_allow_html=True)
    
    if st.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

# ========== DATA ==========
@st.cache_data
def get_patients():
    return fetch_query("SELECT * FROM patients ORDER BY id DESC")

@st.cache_data
def get_medecins():
    return fetch_query("SELECT * FROM medecins ORDER BY id DESC")

@st.cache_data
def get_rdvs():
    return fetch_query("SELECT * FROM rdvs ORDER BY id DESC")

@st.cache_data
def get_consultations():
    return fetch_query("SELECT * FROM consultations ORDER BY id DESC")

@st.cache_data
def get_factures():
    return fetch_query("SELECT * FROM factures ORDER BY id DESC")

# ========== DASHBOARD ==========
if menu == "📊 Tableau de bord":
    st.markdown('<div class="odoo-title">📊 Tableau de bord <span class="badge">Vue d\'ensemble</span></div>', unsafe_allow_html=True)
    
    patients = get_patients()
    medecins = get_medecins()
    rdvs = get_rdvs()
    factures = get_factures()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="odoo-card">
            <div class="card-icon">👥</div>
            <div class="card-number">{len(patients)}</div>
            <div class="card-label">Patients</div>
            <span class="card-trend trend-up">▲ 12%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="odoo-card">
            <div class="card-icon">👨‍⚕️</div>
            <div class="card-number">{len(medecins)}</div>
            <div class="card-label">Médecins</div>
            <span class="card-trend trend-up">▲ 5%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="odoo-card">
            <div class="card-icon">📅</div>
            <div class="card-number">{len(rdvs)}</div>
            <div class="card-label">Rendez-vous</div>
            <span class="card-trend trend-up">▲ 8%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total = factures["montant"].sum() if len(factures) > 0 else 0
        st.markdown(f"""
        <div class="odoo-card">
            <div class="card-icon">💰</div>
            <div class="card-number">{total:,.0f}€</div>
            <div class="card-label">Chiffre d'affaires</div>
            <span class="card-trend trend-up">▲ 15%</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="odoo-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <span style="font-weight: 600; color: #1a2332; font-size: 15px;">📋 Derniers rendez-vous</span>
                <span class="badge-odoo badge-primary">5 derniers</span>
            </div>
        """, unsafe_allow_html=True)
        if len(rdvs) > 0:
            st.dataframe(rdvs[["patient_id", "medecin_id", "date", "statut"]].tail(5), use_container_width=True)
        else:
            st.info("Aucun rendez-vous")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="odoo-card">
            <div style="font-weight: 600; color: #1a2332; font-size: 15px; margin-bottom: 16px;">📊 Répartition</div>
        """, unsafe_allow_html=True)
        if len(rdvs) > 0:
            stats = rdvs["statut"].value_counts()
            fig = px.pie(values=stats.values, names=stats.index, 
                        color_discrete_sequence=["#2c3e6b", "#059669", "#d97706", "#dc2626"],
                        hole=0.3)
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), showlegend=True)
            fig.update_traces(textposition='inside', textinfo='percent')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée")
        st.markdown('</div>', unsafe_allow_html=True)

# ========== PATIENTS ==========
elif menu == "👥 Patients":
    st.markdown('<div class="odoo-title">👥 Patients <span class="badge">Gestion</span></div>', unsafe_allow_html=True)
    
    with st.expander("➕ Nouveau patient", expanded=False):
        with st.form("add_patient"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom *")
                prenom = st.text_input("Prénom *")
                date_naissance = st.date_input("Date de naissance")
                sexe = st.selectbox("Sexe", ["", "M", "F"])
            with col2:
                telephone = st.text_input("Téléphone")
                email = st.text_input("Email")
                adresse = st.text_area("Adresse", height=60)
            
            allergies = st.text_area("Allergies", height=50)
            antecedents = st.text_area("Antécédents", height=50)
            
            if st.form_submit_button("💾 Enregistrer"):
                if nom and prenom:
                    execute_query("""
                        INSERT INTO patients (nom, prenom, date_naissance, sexe, telephone, email, adresse, allergies, antecedents, date_creation)
                        VALUES (?,?,?,?,?,?,?,?,?,?)
                    """, (nom, prenom, date_naissance, sexe, telephone, email, adresse, allergies, antecedents, date.today()))
                    st.success("✅ Patient ajouté !")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Nom et Prénom obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.dataframe(get_patients(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== MÉDECINS ==========
elif menu == "👨‍⚕️ Médecins":
    st.markdown('<div class="odoo-title">👨‍⚕️ Médecins <span class="badge">Gestion</span></div>', unsafe_allow_html=True)
    
    with st.expander("➕ Nouveau médecin", expanded=False):
        with st.form("add_medecin"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom *")
                prenom = st.text_input("Prénom *")
                specialite = st.text_input("Spécialité *")
            with col2:
                telephone = st.text_input("Téléphone")
                email = st.text_input("Email")
                disponible = st.selectbox("Disponible", ["Oui", "Non"])
            
            if st.form_submit_button("💾 Enregistrer"):
                if nom and prenom and specialite:
                    execute_query("""
                        INSERT INTO medecins (nom, prenom, specialite, telephone, email, disponible)
                        VALUES (?,?,?,?,?,?)
                    """, (nom, prenom, specialite, telephone, email, disponible))
                    st.success("✅ Médecin ajouté !")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Nom, Prénom et Spécialité obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.dataframe(get_medecins(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== RENDEZ-VOUS ==========
elif menu == "📅 Rendez-vous":
    st.markdown('<div class="odoo-title">📅 Rendez-vous <span class="badge">Planning</span></div>', unsafe_allow_html=True)
    
    patients = get_patients()
    medecins = get_medecins()
    
    with st.expander("➕ Nouveau rendez-vous", expanded=False):
        with st.form("add_rdv"):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.selectbox("Patient", patients["id"].tolist() if len(patients) > 0 else [],
                                         format_func=lambda x: patients[patients["id"]==x]["nom"].iloc[0] + " " + patients[patients["id"]==x]["prenom"].iloc[0] if len(patients) > 0 else "")
                medecin_id = st.selectbox("Médecin", medecins["id"].tolist() if len(medecins) > 0 else [],
                                         format_func=lambda x: medecins[medecins["id"]==x]["nom"].iloc[0] + " " + medecins[medecins["id"]==x]["prenom"].iloc[0] if len(medecins) > 0 else "")
            with col2:
                date_rdv = st.date_input("Date")
                heure_rdv = st.time_input("Heure")
                motif = st.text_input("Motif")
                statut = st.selectbox("Statut", ["Planifié", "Confirmé", "Terminé", "Annulé"])
            
            if st.form_submit_button("💾 Enregistrer"):
                if patient_id and medecin_id:
                    execute_query("""
                        INSERT INTO rdvs (patient_id, medecin_id, date, heure, motif, statut)
                        VALUES (?,?,?,?,?,?)
                    """, (patient_id, medecin_id, date_rdv, heure_rdv, motif, statut))
                    st.success("✅ Rendez-vous ajouté !")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Patient et Médecin obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.dataframe(get_rdvs(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== CONSULTATIONS ==========
elif menu == "📋 Consultations":
    st.markdown('<div class="odoo-title">📋 Consultations <span class="badge">Dossiers</span></div>', unsafe_allow_html=True)
    
    patients = get_patients()
    medecins = get_medecins()
    
    with st.expander("➕ Nouvelle consultation", expanded=False):
        with st.form("add_consultation"):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.selectbox("Patient", patients["id"].tolist() if len(patients) > 0 else [],
                                         format_func=lambda x: patients[patients["id"]==x]["nom"].iloc[0] + " " + patients[patients["id"]==x]["prenom"].iloc[0] if len(patients) > 0 else "")
                medecin_id = st.selectbox("Médecin", medecins["id"].tolist() if len(medecins) > 0 else [],
                                         format_func=lambda x: medecins[medecins["id"]==x]["nom"].iloc[0] + " " + medecins[medecins["id"]==x]["prenom"].iloc[0] if len(medecins) > 0 else "")
            with col2:
                date_cons = st.date_input("Date")
            
            diagnostic = st.text_area("Diagnostic *", height=80)
            prescription = st.text_area("Prescription", height=80)
            notes = st.text_area("Notes", height=60)
            
            if st.form_submit_button("💾 Enregistrer"):
                if patient_id and medecin_id and diagnostic:
                    execute_query("""
                        INSERT INTO consultations (patient_id, medecin_id, date, diagnostic, prescription, notes)
                        VALUES (?,?,?,?,?,?)
                    """, (patient_id, medecin_id, date_cons, diagnostic, prescription, notes))
                    st.success("✅ Consultation ajoutée !")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Patient, Médecin et Diagnostic obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.dataframe(get_consultations(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== FACTURES ==========
elif menu == "💰 Factures":
    st.markdown('<div class="odoo-title">💰 Factures <span class="badge">Comptabilité</span></div>', unsafe_allow_html=True)
    
    patients = get_patients()
    
    with st.expander("➕ Nouvelle facture", expanded=False):
        with st.form("add_facture"):
            patient_id = st.selectbox("Patient", patients["id"].tolist() if len(patients) > 0 else [],
                                     format_func=lambda x: patients[patients["id"]==x]["nom"].iloc[0] + " " + patients[patients["id"]==x]["prenom"].iloc[0] if len(patients) > 0 else "")
            col1, col2 = st.columns(2)
            with col1:
                montant = st.number_input("Montant (€) *", min_value=0.0, step=10.0)
                date_echeance = st.date_input("Date d'échéance")
            with col2:
                statut = st.selectbox("Statut", ["En attente", "Payée", "Annulée"])
                description = st.text_area("Description", height=60)
            
            if st.form_submit_button("💾 Générer"):
                if patient_id and montant > 0:
                    execute_query("""
                        INSERT INTO factures (patient_id, montant, date_emission, date_echeance, statut, description)
                        VALUES (?,?,?,?,?,?)
                    """, (patient_id, montant, date.today(), date_echeance, statut, description))
                    st.success("✅ Facture générée !")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Patient et Montant obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    factures = get_factures()
    if len(factures) > 0:
        total = factures["montant"].sum()
        encours = len(factures[factures["statut"] == "En attente"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📄 Total factures", len(factures))
        col2.metric("💰 Montant total", f"{total:,.2f} €")
        col3.metric("⏳ En attente", encours)
        
        st.dataframe(factures, use_container_width=True)
    else:
        st.info("Aucune facture")
    st.markdown('</div>', unsafe_allow_html=True)

# ========== STATISTIQUES ==========
elif menu == "📈 Statistiques":
    st.markdown('<div class="odoo-title">📈 Statistiques <span class="badge">Analyses</span></div>', unsafe_allow_html=True)
    
    patients = get_patients()
    medecins = get_medecins()
    rdvs = get_rdvs()
    factures = get_factures()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
        st.subheader("👥 Patients")
        st.metric("Total patients", len(patients))
        if len(patients) > 0:
            st.dataframe(patients[["nom", "prenom", "telephone"]].head(5), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
        st.subheader("📅 Rendez-vous")
        if len(rdvs) > 0:
            stats = rdvs["statut"].value_counts()
            fig = px.bar(x=stats.index, y=stats.values, color=stats.index,
                        color_discrete_sequence=["#2c3e6b", "#059669", "#d97706", "#dc2626"])
            fig.update_layout(height=280, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée")
        st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
        st.subheader("💰 Factures")
        if len(factures) > 0:
            stats = factures["statut"].value_counts()
            fig = px.pie(values=stats.values, names=stats.index,
                        color_discrete_sequence=["#d97706", "#059669", "#dc2626"])
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
        st.subheader("👨‍⚕️ Médecins")
        st.metric("Total médecins", len(medecins))
        if len(medecins) > 0:
            st.dataframe(medecins[["nom", "prenom", "specialite"]].head(5), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ========== ADMINISTRATION ==========
elif menu == "⚙️ Administration":
    st.markdown('<div class="odoo-title">⚙️ Administration <span class="badge">Système</span></div>', unsafe_allow_html=True)
    
    with st.expander("➕ Nouvel utilisateur", expanded=False):
        with st.form("add_user"):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Nom d'utilisateur *")
                password = st.text_input("Mot de passe *", type="password")
            with col2:
                role = st.selectbox("Rôle", ["Admin", "Médecin", "Assistant"])
                nom = st.text_input("Nom")
                prenom = st.text_input("Prénom")
            
            if st.form_submit_button("💾 Ajouter"):
                if username and password:
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                    try:
                        execute_query("INSERT INTO users (username, password, role, nom, prenom) VALUES (?,?,?,?,?)",
                                     (username, hashed, role, nom, prenom))
                        st.success("✅ Utilisateur ajouté !")
                        st.rerun()
                    except:
                        st.error("Cet utilisateur existe déjà.")
                else:
                    st.error("Nom d'utilisateur et mot de passe obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    users = fetch_query("SELECT id, username, role, nom, prenom FROM users")
    st.dataframe(users, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="odoo-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-weight: 600; color: #1a2332;">📊 Base de données</div>
                <div style="color: #6b7a8f; font-size: 13px;">SQLite • medicare.db</div>
            </div>
            <span class="badge-odoo badge-success">✅ Actif</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
