import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta
import uuid
import hashlib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="🏥 MediCare", layout="wide")

# ========== BASE DE DONNÉES ==========
def init_db():
    conn = sqlite3.connect('medicare.db')
    c = conn.cursor()
    
    # Tables
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
    
    # Admin par défaut
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

# ========== STYLE ODOO ==========
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Sidebar Odoo Style */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a2b4a 0%, #0f1a2e 100%) !important;
        padding-top: 20px !important;
    }
    
    .css-1d391kg .stRadio label {
        color: #a8b8c8 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
        border-radius: 8px !important;
        transition: all 0.3s !important;
        margin: 2px 0 !important;
    }
    
    .css-1d391kg .stRadio label:hover {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
    }
    
    .css-1d391kg .stRadio label[data-baseweb="radio"] {
        background: rgba(44, 62, 107, 0.5) !important;
        color: white !important;
        border-left: 3px solid #4a90d9 !important;
    }
    
    /* Odoo Cards */
    .odoo-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e8edf3;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }
    
    .odoo-card:hover {
        box-shadow: 0 4px 24px rgba(0,0,0,0.10);
        transform: translateY(-2px);
    }
    
    .odoo-card .icon { font-size: 28px; margin-bottom: 8px; }
    .odoo-card .number { font-size: 32px; font-weight: 700; color: #1a2b4a; }
    .odoo-card .label { color: #6b7a8f; font-size: 14px; font-weight: 500; margin-top: 4px; }
    .odoo-card .trend { font-size: 12px; font-weight: 600; padding: 2px 12px; border-radius: 20px; display: inline-block; margin-top: 8px; }
    .trend-up { background: #e8f5e9; color: #2e7d32; }
    .trend-down { background: #fde8e8; color: #c62828; }
    
    /* Title */
    .odoo-title {
        font-size: 24px;
        font-weight: 700;
        color: #1a2b4a;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 2px solid #e8edf3;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .odoo-title .badge { background: #e8edf3; padding: 2px 16px; border-radius: 20px; font-size: 12px; color: #6b7a8f; }
    
    /* Logo Sidebar */
    .sidebar-logo {
        text-align: center;
        padding: 20px 0 24px 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 16px;
    }
    .sidebar-logo h2 { color: white !important; font-weight: 700 !important; font-size: 24px !important; margin: 0 !important; }
    .sidebar-logo .sub { color: #6b8cae !important; font-size: 12px !important; }
    .sidebar-logo .icon { font-size: 48px; }
    
    /* Buttons */
    .stButton button {
        background: #2c3e6b !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 24px !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
    }
    .stButton button:hover {
        background: #1a2b4a !important;
        box-shadow: 0 4px 16px rgba(44, 62, 107, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Badges */
    .badge-odoo {
        padding: 3px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-blue { background: #e3f0ff; color: #1a56db; }
    .badge-green { background: #e6f7e6; color: #059669; }
    .badge-yellow { background: #fff8e1; color: #d97706; }
    .badge-red { background: #fde8e8; color: #dc2626; }
    
    /* Tables */
    .dataframe {
        border-radius: 8px !important;
        border: 1px solid #e8edf3 !important;
    }
    .dataframe thead th {
        background: #f8fafc !important;
        color: #1a2b4a !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
    }
    .dataframe tbody td { padding: 10px 16px !important; }
    .dataframe tbody tr:hover { background: #f8fafc !important; }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc !important;
        border-radius: 8px !important;
        border: 1px solid #e8edf3 !important;
        font-weight: 600 !important;
        color: #1a2b4a !important;
    }
    
    /* Login */
    .login-container {
        max-width: 400px;
        margin: 80px auto;
        padding: 40px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.08);
        border: 1px solid #e8edf3;
    }
    .login-container h1 {
        text-align: center;
        color: #1a2b4a;
        font-size: 28px;
        margin-bottom: 8px;
    }
    .login-container .sub {
        text-align: center;
        color: #6b7a8f;
        margin-bottom: 32px;
    }
</style>
""", unsafe_allow_html=True)

# ========== LOGIN ==========
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-container">
        <h1>🏥 MediCare</h1>
        <p class="sub">Gestion Médicale Professionnelle</p>
    """, unsafe_allow_html=True)
    
    username = st.text_input("Nom d'utilisateur", key="login_user")
    password = st.text_input("Mot de passe", type="password", key="login_pass")
    
    if st.button("🔐 Se connecter", use_container_width=True):
        if login(username, password):
            st.success("✅ Connexion réussie !")
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")
    
    st.markdown("""
    <p style="text-align: center; color: #6b7a8f; font-size: 12px; margin-top: 16px;">
        Admin: admin / admin123
    </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="icon">🏥</div>
        <h2>MediCare</h2>
        <div class="sub">Gestion Médicale</div>
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
        "👤 Utilisateurs"
    ])
    
    st.markdown("---")
    st.markdown(f"""
    <div style="padding: 12px; background: rgba(255,255,255,0.05); border-radius: 8px; margin-top: 20px;">
        <p style="color: #6b8cae; font-size: 12px; margin: 0; text-align: center;">
            <strong>{st.session_state.user.get('nom', '')}</strong><br>
            {st.session_state.user.get('role', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
            <div class="icon">👥</div>
            <div class="number">{len(patients)}</div>
            <div class="label">Patients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="odoo-card">
            <div class="icon">👨‍⚕️</div>
            <div class="number">{len(medecins)}</div>
            <div class="label">Médecins</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="odoo-card">
            <div class="icon">📅</div>
            <div class="number">{len(rdvs)}</div>
            <div class="label">Rendez-vous</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total = factures["montant"].sum() if len(factures) > 0 else 0
        st.markdown(f"""
        <div class="odoo-card">
            <div class="icon">💰</div>
            <div class="number">{total:,.0f}€</div>
            <div class="label">Chiffre d'affaires</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
        st.subheader("📋 Derniers rendez-vous")
        if len(rdvs) > 0:
            st.dataframe(rdvs[["patient_id", "medecin_id", "date", "statut"]].tail(5), use_container_width=True)
        else:
            st.info("Aucun rendez-vous")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
        st.subheader("📊 Rendez-vous par statut")
        if len(rdvs) > 0:
            stats = rdvs["statut"].value_counts()
            fig = px.pie(values=stats.values, names=stats.index, color_discrete_sequence=["#2c3e6b", "#059669", "#d97706", "#dc2626"])
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
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
                    st.success(f"✅ Patient {nom} {prenom} ajouté !")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Nom et Prénom obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    patients = get_patients()
    if len(patients) > 0:
        st.dataframe(patients, use_container_width=True)
    else:
        st.info("Aucun patient")
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
                    st.success(f"✅ Dr {nom} {prenom} ajouté !")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Nom, Prénom et Spécialité obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    medecins = get_medecins()
    if len(medecins) > 0:
        st.dataframe(medecins, use_container_width=True)
    else:
        st.info("Aucun médecin")
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
    rdvs = get_rdvs()
    if len(rdvs) > 0:
        st.dataframe(rdvs, use_container_width=True)
    else:
        st.info("Aucun rendez-vous")
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
    consultations = get_consultations()
    if len(consultations) > 0:
        st.dataframe(consultations, use_container_width=True)
    else:
        st.info("Aucune consultation")
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
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
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
            fig = px.pie(values=stats.values, names=stats.index, color_discrete_sequence=["#d97706", "#059669", "#dc2626"])
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

# ========== UTILISATEURS ==========
elif menu == "👤 Utilisateurs":
    st.markdown('<div class="odoo-title">👤 Utilisateurs <span class="badge">Administration</span></div>', unsafe_allow_html=True)
    
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
                        st.success(f"✅ Utilisateur {username} ajouté !")
                        st.rerun()
                    except:
                        st.error("Cet utilisateur existe déjà.")
                else:
                    st.error("Nom d'utilisateur et mot de passe obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    users = fetch_query("SELECT id, username, role, nom, prenom FROM users")
    if len(users) > 0:
        st.dataframe(users, use_container_width=True)
    else:
        st.info("Aucun utilisateur")
    st.markdown('</div>', unsafe_allow_html=True)
