import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import uuid
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="🏥 MediCare Pro", layout="wide", initial_sidebar_state="expanded")

# ========== DESIGN ODOO ==========
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Odoo Style */
    .css-1d391kg {
        background-color: #1a2b4a !important;
        padding-top: 20px !important;
    }
    
    .css-1d391kg .stRadio label {
        color: #c8d6e5 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }
    
    .css-1d391kg .stRadio label:hover {
        background-color: #2c3e6b !important;
        color: white !important;
    }
    
    .css-1d391kg .stRadio label[data-baseweb="radio"] {
        background-color: #2c3e6b !important;
        color: white !important;
    }
    
    /* Odoo Cards */
    .odoo-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #e8edf3;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }
    
    .odoo-card:hover {
        box-shadow: 0 4px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .odoo-card .icon {
        font-size: 28px;
        margin-bottom: 8px;
    }
    
    .odoo-card .number {
        font-size: 32px;
        font-weight: 700;
        color: #1a2b4a;
        line-height: 1.2;
    }
    
    .odoo-card .label {
        color: #6b7a8f;
        font-size: 14px;
        font-weight: 500;
        margin-top: 4px;
    }
    
    .odoo-card .trend {
        font-size: 12px;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 8px;
    }
    
    .trend-up { background: #e6f7e6; color: #00a651; }
    .trend-down { background: #fde8e8; color: #e74c3c; }
    
    /* Odoo Title */
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
    
    .odoo-title .badge {
        background: #e8edf3;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        color: #6b7a8f;
    }
    
    /* Odoo Buttons */
    .stButton button {
        background: #2c3e6b !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: all 0.2s !important;
    }
    
    .stButton button:hover {
        background: #1a2b4a !important;
        box-shadow: 0 4px 12px rgba(44, 62, 107, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Odoo Table */
    .dataframe {
        border-radius: 8px !important;
        overflow: hidden !important;
        border: 1px solid #e8edf3 !important;
    }
    
    .dataframe thead th {
        background: #f8fafc !important;
        color: #1a2b4a !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 12px 16px !important;
        border-bottom: 2px solid #e8edf3 !important;
    }
    
    .dataframe tbody td {
        padding: 10px 16px !important;
        font-size: 13px !important;
        border-bottom: 1px solid #f1f4f8 !important;
    }
    
    .dataframe tbody tr:hover {
        background: #f8fafc !important;
    }
    
    /* Odoo Badges */
    .badge-odoo {
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-blue { background: #e8f0fe; color: #2c3e6b; }
    .badge-green { background: #e6f7e6; color: #00a651; }
    .badge-yellow { background: #fff8e1; color: #f39c12; }
    .badge-red { background: #fde8e8; color: #e74c3c; }
    .badge-purple { background: #f3e8ff; color: #8b5cf6; }
    
    /* Odoo Inputs */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #dce3ec !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
        transition: all 0.2s !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #2c3e6b !important;
        box-shadow: 0 0 0 3px rgba(44, 62, 107, 0.1) !important;
    }
    
    /* Odoo Expander */
    .streamlit-expanderHeader {
        background: #f8fafc !important;
        border-radius: 8px !important;
        border: 1px solid #e8edf3 !important;
        font-weight: 600 !important;
        color: #1a2b4a !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f4f8 !important;
    }
    
    /* Odoo Divider */
    hr {
        margin: 24px 0 !important;
        border: none !important;
        border-top: 1px solid #e8edf3 !important;
    }
    
    /* Odoo Logo in sidebar */
    .odoo-logo {
        text-align: center;
        padding: 16px 0;
        border-bottom: 1px solid #2c3e6b;
        margin-bottom: 16px;
    }
    
    .odoo-logo h2 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        margin: 0 !important;
    }
    
    .odoo-logo span {
        color: #6b8cae !important;
        font-size: 12px !important;
    }
    
    .odoo-logo .icon {
        font-size: 40px !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== INITIALISATION ==========
if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=[
        "ID", "Nom", "Prenom", "Date_Naissance", "Sexe", "Telephone", "Email", "Adresse", "Date_Creation"
    ])

if "medecins" not in st.session_state:
    st.session_state.medecins = pd.DataFrame(columns=[
        "ID", "Nom", "Prenom", "Specialite", "Telephone", "Email", "Disponible"
    ])

if "rdvs" not in st.session_state:
    st.session_state.rdvs = pd.DataFrame(columns=[
        "ID", "Patient", "Medecin", "Date", "Heure", "Motif", "Statut"
    ])

if "consultations" not in st.session_state:
    st.session_state.consultations = pd.DataFrame(columns=[
        "ID", "Patient", "Medecin", "Date", "Diagnostic", "Prescription"
    ])

if "factures" not in st.session_state:
    st.session_state.factures = pd.DataFrame(columns=[
        "ID", "Patient", "Montant", "Date_Emission", "Date_Echeance", "Statut"
    ])

# ========== SIDEBAR ODOO ==========
with st.sidebar:
    st.markdown("""
    <div class="odoo-logo">
        <div class="icon">🏥</div>
        <h2>MediCare</h2>
        <span>Gestion Médicale Pro</span>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("", [
        "📊 Tableau de bord",
        "👥 Patients",
        "👨‍⚕️ Médecins",
        "📅 Rendez-vous",
        "📋 Consultations",
        "💰 Factures",
        "📈 Statistiques"
    ])
    
    st.markdown("---")
    st.markdown("""
    <div style="padding: 12px; background: #2c3e6b; border-radius: 8px; margin-top: 20px;">
        <p style="color: #c8d6e5; font-size: 12px; margin: 0; text-align: center;">
            <strong>Version 3.0</strong><br>
            © 2024 MediCare
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========== DASHBOARD ==========
if menu == "📊 Tableau de bord":
    st.markdown('<div class="odoo-title">📊 Tableau de bord <span class="badge">Vue d\'ensemble</span></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="odoo-card">
            <div class="icon">👥</div>
            <div class="number">{len(st.session_state.patients)}</div>
            <div class="label">Patients</div>
            <span class="trend trend-up">+12%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="odoo-card">
            <div class="icon">👨‍⚕️</div>
            <div class="number">{len(st.session_state.medecins)}</div>
            <div class="label">Médecins</div>
            <span class="trend trend-up">+5%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="odoo-card">
            <div class="icon">📅</div>
            <div class="number">{len(st.session_state.rdvs)}</div>
            <div class="label">Rendez-vous</div>
            <span class="trend trend-up">+8%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total = st.session_state.factures["Montant"].sum() if len(st.session_state.factures) > 0 else 0
        st.markdown(f"""
        <div class="odoo-card">
            <div class="icon">💰</div>
            <div class="number">{total:,.0f}€</div>
            <div class="label">Chiffre d'affaires</div>
            <span class="trend trend-up">+15%</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="odoo-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-weight: 600; color: #1a2b4a;">📋 Derniers rendez-vous</span>
                <span class="badge-odoo badge-blue">5 derniers</span>
            </div>
        """, unsafe_allow_html=True)
        if len(st.session_state.rdvs) > 0:
            st.dataframe(st.session_state.rdvs[["Patient", "Medecin", "Date", "Statut"]].tail(5), use_container_width=True)
        else:
            st.info("Aucun rendez-vous")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="odoo-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-weight: 600; color: #1a2b4a;">🆕 Derniers patients</span>
                <span class="badge-odoo badge-green">5 derniers</span>
            </div>
        """, unsafe_allow_html=True)
        if len(st.session_state.patients) > 0:
            st.dataframe(st.session_state.patients[["Nom", "Prenom", "Telephone"]].tail(5), use_container_width=True)
        else:
            st.info("Aucun patient")
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
                date_naiss = st.date_input("Date de naissance")
                sexe = st.selectbox("Sexe", ["", "M", "F"])
            with col2:
                telephone = st.text_input("Téléphone")
                email = st.text_input("Email")
                adresse = st.text_area("Adresse", height=68)
            
            if st.form_submit_button("💾 Enregistrer"):
                if nom and prenom:
                    new_id = str(uuid.uuid4())[:8]
                    new_row = pd.DataFrame([[
                        new_id, nom, prenom, date_naiss, sexe, telephone, email, adresse, date.today()
                    ]], columns=st.session_state.patients.columns)
                    st.session_state.patients = pd.concat([st.session_state.patients, new_row], ignore_index=True)
                    st.success(f"✅ Patient {nom} {prenom} ajouté !")
                    st.rerun()
                else:
                    st.error("❌ Nom et Prénom obligatoires.")
    
    st.markdown("""
    <div class="odoo-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span style="font-weight: 600; color: #1a2b4a;">📋 Liste des patients</span>
            <span class="badge-odoo badge-blue">Total: {}</span>
        </div>
    </div>
    """.format(len(st.session_state.patients)), unsafe_allow_html=True)
    
    search = st.text_input("🔍 Rechercher", placeholder="Nom, Prénom, Téléphone...")
    if search:
        filtered = st.session_state.patients[
            st.session_state.patients["Nom"].str.contains(search, case=False, na=False) |
            st.session_state.patients["Prenom"].str.contains(search, case=False, na=False) |
            st.session_state.patients["Telephone"].str.contains(search, case=False, na=False)
        ]
        st.dataframe(filtered, use_container_width=True)
    else:
        st.dataframe(st.session_state.patients, use_container_width=True)
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
                    new_id = str(uuid.uuid4())[:8]
                    new_row = pd.DataFrame([[
                        new_id, nom, prenom, specialite, telephone, email, disponible
                    ]], columns=st.session_state.medecins.columns)
                    st.session_state.medecins = pd.concat([st.session_state.medecins, new_row], ignore_index=True)
                    st.success(f"✅ Dr {nom} {prenom} ajouté !")
                    st.rerun()
                else:
                    st.error("❌ Nom, Prénom et Spécialité obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.dataframe(st.session_state.medecins, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== RENDEZ-VOUS ==========
elif menu == "📅 Rendez-vous":
    st.markdown('<div class="odoo-title">📅 Rendez-vous <span class="badge">Planning</span></div>', unsafe_allow_html=True)
    
    with st.expander("➕ Nouveau rendez-vous", expanded=False):
        with st.form("add_rdv"):
            patient_list = st.session_state.patients["Nom"] + " " + st.session_state.patients["Prenom"] if len(st.session_state.patients) > 0 else [""]
            medecin_list = st.session_state.medecins["Nom"] + " " + st.session_state.medecins["Prenom"] if len(st.session_state.medecins) > 0 else [""]
            
            col1, col2 = st.columns(2)
            with col1:
                patient = st.selectbox("Patient *", patient_list)
                medecin = st.selectbox("Médecin *", medecin_list)
            with col2:
                date_rdv = st.date_input("Date")
                heure_rdv = st.time_input("Heure")
                motif = st.text_input("Motif")
                statut = st.selectbox("Statut", ["Planifié", "Confirmé", "Terminé", "Annulé"])
            
            if st.form_submit_button("💾 Enregistrer"):
                if patient != "" and medecin != "":
                    new_id = str(uuid.uuid4())[:8]
                    new_row = pd.DataFrame([[
                        new_id, patient, medecin, date_rdv, heure_rdv, motif, statut
                    ]], columns=st.session_state.rdvs.columns)
                    st.session_state.rdvs = pd.concat([st.session_state.rdvs, new_row], ignore_index=True)
                    st.success("✅ Rendez-vous ajouté !")
                    st.rerun()
                else:
                    st.error("❌ Patient et Médecin obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.dataframe(st.session_state.rdvs, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== CONSULTATIONS ==========
elif menu == "📋 Consultations":
    st.markdown('<div class="odoo-title">📋 Consultations <span class="badge">Dossiers médicaux</span></div>', unsafe_allow_html=True)
    
    with st.expander("➕ Nouvelle consultation", expanded=False):
        with st.form("add_consultation"):
            patient_list = st.session_state.patients["Nom"] + " " + st.session_state.patients["Prenom"] if len(st.session_state.patients) > 0 else [""]
            medecin_list = st.session_state.medecins["Nom"] + " " + st.session_state.medecins["Prenom"] if len(st.session_state.medecins) > 0 else [""]
            
            col1, col2 = st.columns(2)
            with col1:
                patient = st.selectbox("Patient *", patient_list)
                medecin = st.selectbox("Médecin *", medecin_list)
            with col2:
                date_cons = st.date_input("Date")
            
            diagnostic = st.text_area("Diagnostic *", height=80)
            prescription = st.text_area("Prescription", height=80)
            
            if st.form_submit_button("💾 Enregistrer"):
                if patient != "" and medecin != "" and diagnostic:
                    new_id = str(uuid.uuid4())[:8]
                    new_row = pd.DataFrame([[
                        new_id, patient, medecin, date_cons, diagnostic, prescription
                    ]], columns=st.session_state.consultations.columns)
                    st.session_state.consultations = pd.concat([st.session_state.consultations, new_row], ignore_index=True)
                    st.success("✅ Consultation ajoutée !")
                    st.rerun()
                else:
                    st.error("❌ Patient, Médecin et Diagnostic obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    st.dataframe(st.session_state.consultations, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== FACTURES ==========
elif menu == "💰 Factures":
    st.markdown('<div class="odoo-title">💰 Factures <span class="badge">Comptabilité</span></div>', unsafe_allow_html=True)
    
    with st.expander("➕ Nouvelle facture", expanded=False):
        with st.form("add_facture"):
            patient_list = st.session_state.patients["Nom"] + " " + st.session_state.patients["Prenom"] if len(st.session_state.patients) > 0 else [""]
            
            col1, col2 = st.columns(2)
            with col1:
                patient = st.selectbox("Patient *", patient_list)
                montant = st.number_input("Montant (€) *", min_value=0.0, step=10.0)
            with col2:
                date_echeance = st.date_input("Date d'échéance")
                statut = st.selectbox("Statut", ["En attente", "Payée", "Annulée"])
            
            if st.form_submit_button("💾 Générer"):
                if patient != "" and montant > 0:
                    new_id = str(uuid.uuid4())[:8]
                    new_row = pd.DataFrame([[
                        new_id, patient, montant, date.today(), date_echeance, statut
                    ]], columns=st.session_state.factures.columns)
                    st.session_state.factures = pd.concat([st.session_state.factures, new_row], ignore_index=True)
                    st.success(f"✅ Facture générée pour {patient} !")
                    st.rerun()
                else:
                    st.error("❌ Patient et Montant obligatoires.")
    
    st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
    
    total = st.session_state.factures["Montant"].sum() if len(st.session_state.factures) > 0 else 0
    encours = len(st.session_state.factures[st.session_state.factures["Statut"] == "En attente"]) if len(st.session_state.factures) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Total factures", len(st.session_state.factures))
    col2.metric("💰 Montant total", f"{total:,.2f} €")
    col3.metric("⏳ En attente", encours)
    
    st.dataframe(st.session_state.factures, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== STATISTIQUES ==========
elif menu == "📈 Statistiques":
    st.markdown('<div class="odoo-title">📈 Statistiques <span class="badge">Analyses</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
        st.subheader("👥 Répartition patients")
        if len(st.session_state.patients) > 0:
            st.metric("Total patients", len(st.session_state.patients))
        else:
            st.info("Aucune donnée")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="odoo-card">', unsafe_allow_html=True)
        st.subheader("📊 Rendez-vous")
        if len(st.session_state.rdvs) > 0:
            stats = st.session_state.rdvs["Statut"].value_counts()
            fig = px.pie(values=stats.values, names=stats.index, color_discrete_sequence=["#2c3e6b", "#00a651", "#f39c12", "#e74c3c"])
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée")
        st.markdown('</div>', unsafe_allow_html=True)
