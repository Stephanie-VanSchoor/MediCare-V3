import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime
import hashlib

st.set_page_config(page_title="🏥 MediCare V3", layout="wide")


# ========== BASE DE DONNÉES ==========
def init_db():
    conn = sqlite3.connect('medical.db')
    c = conn.cursor()

    # Tables
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prenom TEXT, date_naissance TEXT, telephone TEXT, email TEXT, adresse TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS medecins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prenom TEXT, specialite TEXT, telephone TEXT, email TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS rdvs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, medecin_id INTEGER, date TEXT, heure TEXT, motif TEXT, statut TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS consultations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, medecin_id INTEGER, date TEXT, diagnostic TEXT, prescription TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS factures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, montant REAL, date_emission TEXT, date_echeance TEXT, statut TEXT
    )''')

    conn.commit()
    conn.close()


init_db()


# ========== FONCTIONS ==========
def get_patients():
    conn = sqlite3.connect('medical.db')
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    return df


def get_medecins():
    conn = sqlite3.connect('medical.db')
    df = pd.read_sql_query("SELECT * FROM medecins", conn)
    conn.close()
    return df


def get_rdvs():
    conn = sqlite3.connect('medical.db')
    df = pd.read_sql_query("SELECT * FROM rdvs", conn)
    conn.close()
    return df


def get_consultations():
    conn = sqlite3.connect('medical.db')
    df = pd.read_sql_query("SELECT * FROM consultations", conn)
    conn.close()
    return df


def get_factures():
    conn = sqlite3.connect('medical.db')
    df = pd.read_sql_query("SELECT * FROM factures", conn)
    conn.close()
    return df


def add_patient(nom, prenom, date_naissance, telephone, email, adresse):
    conn = sqlite3.connect('medical.db')
    c = conn.cursor()
    c.execute("INSERT INTO patients (nom, prenom, date_naissance, telephone, email, adresse) VALUES (?,?,?,?,?,?)",
              (nom, prenom, date_naissance, telephone, email, adresse))
    conn.commit()
    conn.close()


def add_medecin(nom, prenom, specialite, telephone, email):
    conn = sqlite3.connect('medical.db')
    c = conn.cursor()
    c.execute("INSERT INTO medecins (nom, prenom, specialite, telephone, email) VALUES (?,?,?,?,?)",
              (nom, prenom, specialite, telephone, email))
    conn.commit()
    conn.close()


def add_rdv(patient_id, medecin_id, date, heure, motif, statut):
    conn = sqlite3.connect('medical.db')
    c = conn.cursor()
    c.execute("INSERT INTO rdvs (patient_id, medecin_id, date, heure, motif, statut) VALUES (?,?,?,?,?,?)",
              (patient_id, medecin_id, date, heure, motif, statut))
    conn.commit()
    conn.close()


# ========== SIDEBAR ==========
st.sidebar.title("🏥 MediCare V3")
st.sidebar.markdown("---")

menu = st.sidebar.radio("📋 MENU", [
    "🏠 Dashboard",
    "👥 Patients",
    "👨‍⚕️ Médecins",
    "📅 Rendez-vous",
    "📋 Consultations",
    "💰 Factures"
])

# ========== DASHBOARD ==========
if menu == "🏠 Dashboard":
    st.title("📊 Dashboard")

    patients = get_patients()
    medecins = get_medecins()
    rdvs = get_rdvs()
    factures = get_factures()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Patients", len(patients))
    col2.metric("👨‍⚕️ Médecins", len(medecins))
    col3.metric("📅 Rendez-vous", len(rdvs))
    col4.metric("💰 Factures", len(factures))

    st.subheader("📋 Derniers rendez-vous")
    if len(rdvs) > 0:
        st.dataframe(rdvs.tail(5))

# ========== PATIENTS ==========
elif menu == "👥 Patients":
    st.title("👥 Gestion des patients")

    with st.form("add_patient"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            date_naissance = st.date_input("Date de naissance")
        with col2:
            telephone = st.text_input("Téléphone")
            email = st.text_input("Email")
            adresse = st.text_input("Adresse")

        if st.form_submit_button("➕ Ajouter"):
            if nom and prenom:
                add_patient(nom, prenom, date_naissance, telephone, email, adresse)
                st.success("Patient ajouté !")
                st.rerun()

    st.dataframe(get_patients())

# ========== MÉDECINS ==========
elif menu == "👨‍⚕️ Médecins":
    st.title("👨‍⚕️ Gestion des médecins")

    with st.form("add_medecin"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            specialite = st.text_input("Spécialité")
        with col2:
            telephone = st.text_input("Téléphone")
            email = st.text_input("Email")

        if st.form_submit_button("➕ Ajouter"):
            if nom and prenom and specialite:
                add_medecin(nom, prenom, specialite, telephone, email)
                st.success("Médecin ajouté !")
                st.rerun()

    st.dataframe(get_medecins())

# ========== RENDEZ-VOUS ==========
elif menu == "📅 Rendez-vous":
    st.title("📅 Gestion des rendez-vous")

    patients = get_patients()
    medecins = get_medecins()

    with st.form("add_rdv"):
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.selectbox("Patient", patients["id"].tolist(),
                                      format_func=lambda x: patients[patients["id"] == x]["nom"].iloc[0] + " " +
                                                            patients[patients["id"] == x]["prenom"].iloc[0] if len(
                                          patients) > 0 else "")
            medecin_id = st.selectbox("Médecin", medecins["id"].tolist(),
                                      format_func=lambda x: medecins[medecins["id"] == x]["nom"].iloc[0] + " " +
                                                            medecins[medecins["id"] == x]["prenom"].iloc[0] if len(
                                          medecins) > 0 else "")
        with col2:
            date_rdv = st.date_input("Date")
            heure_rdv = st.time_input("Heure")
            motif = st.text_input("Motif")
            statut = st.selectbox("Statut", ["Planifié", "Confirmé", "Terminé"])

        if st.form_submit_button("➕ Ajouter"):
            add_rdv(patient_id, medecin_id, date_rdv, heure_rdv, motif, statut)
            st.success("Rendez-vous ajouté !")
            st.rerun()

    rdvs = get_rdvs()
    if len(rdvs) > 0:
        st.dataframe(rdvs)

# ========== CONSULTATIONS ==========
elif menu == "📋 Consultations":
    st.title("📋 Consultations")
    st.info("Module de consultations - bientôt disponible")

    patients = get_patients()
    medecins = get_medecins()

    with st.form("add_consultation"):
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.selectbox("Patient", patients["id"].tolist(),
                                      format_func=lambda x: patients[patients["id"] == x]["nom"].iloc[0] + " " +
                                                            patients[patients["id"] == x]["prenom"].iloc[0] if len(
                                          patients) > 0 else "")
            medecin_id = st.selectbox("Médecin", medecins["id"].tolist(),
                                      format_func=lambda x: medecins[medecins["id"] == x]["nom"].iloc[0] + " " +
                                                            medecins[medecins["id"] == x]["prenom"].iloc[0] if len(
                                          medecins) > 0 else "")
        with col2:
            date_cons = st.date_input("Date")

        diagnostic = st.text_area("Diagnostic")
        prescription = st.text_area("Prescription")

        if st.form_submit_button("➕ Ajouter"):
            st.success("Consultation ajoutée !")

# ========== FACTURES ==========
elif menu == "💰 Factures":
    st.title("💰 Facturation")
    st.info("Module de facturation - bientôt disponible")

    patients = get_patients()

    with st.form("add_facture"):
        patient_id = st.selectbox("Patient", patients["id"].tolist(),
                                  format_func=lambda x: patients[patients["id"] == x]["nom"].iloc[0] + " " +
                                                        patients[patients["id"] == x]["prenom"].iloc[0] if len(
                                      patients) > 0 else "")
        montant = st.number_input("Montant (€)", min_value=0.0)
        date_echeance = st.date_input("Date d'échéance")
        statut = st.selectbox("Statut", ["En attente", "Payée"])

        if st.form_submit_button("➕ Générer"):
            st.success("Facture générée !")
