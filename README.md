# 🏥 MediCare Pro

**Application de gestion médicale complète** pour cabinets, cliniques et professionnels de santé.

---

## 📋 Fonctionnalités

### 👥 Gestion des patients
- Ajout, modification, suppression
- Dossier médical complet (nom, prénom, date naissance, téléphone, email, adresse)
- Recherche avancée

### 👨‍⚕️ Gestion des médecins
- Ajout, modification, suppression
- Spécialité, téléphone, email
- Gestion des disponibilités

### 📅 Gestion des rendez-vous
- Prise de rendez-vous patient/médecin
- Planification par date et heure
- Statuts : Planifié, Confirmé, Terminé, Annulé
- Filtrage par statut

### 📋 Gestion des consultations
- Dossier de consultation complet
- Diagnostic et prescription
- Historique des consultations

### 💰 Facturation
- Génération de factures
- Suivi des paiements
- Statistiques financières

### 📊 Dashboard
- Vue d'ensemble des activités
- Statistiques en temps réel
- Graphiques interactifs

### 👤 Multi-utilisateurs
- Authentification sécurisée
- Rôles : Admin, Médecin, Assistant

---

## 🚀 Installation

### 1. Prérequis
- Python 3.8 ou supérieur
- Streamlit

### 2. Installation

```bash
# Cloner le projet
git clone https://github.com/votre-repo/medical-app.git
cd medical-app

# Installer les dépendances
pip install streamlit pandas plotly

# Lancer l'application
streamlit run app.py
