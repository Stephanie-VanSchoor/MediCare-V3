# 🏥 MediGest Pro
**Application de gestion médicale complète pour cabinets, cliniques et professionnels de santé.**

---

## 📋 Fonctionnalités

### 👥 Gestion des patients
- Ajout, affichage et suppression
- Dossier patient : nom, prénom, téléphone, email, adresse

### 📅 Gestion des rendez-vous
- Prise de rendez-vous
- Planification par date et heure
- Motif de consultation

### 💊 Gestion des consultations
- Suivi des consultations
- Motif, diagnostic, traitement

### 💰 Facturation
- Génération de factures (numéro automatique)
- Téléchargement en PDF
- Suivi des montants

### 📊 Dashboard
- Vue d'ensemble des activités
- Statistiques en temps réel :
  - Nombre de patients
  - Nombre de rendez-vous
  - Nombre de factures
  - Total des revenus

### 👤 Multi-utilisateurs
- Authentification sécurisée par email + PIN
- 4 rôles :
  - 👨‍⚕️ Administrateur
  - 👨‍⚕️ Médecin
  - 💪 Kinésithérapeute
  - 📋 Secrétaire

### 💲 Offres commerciales
- 3 formules : BASIC, PRO, PREMIUM
- Formulaire de commande intégré
- Contact direct

### 💾 Sauvegarde
- Sauvegarde automatique des données
- Restauration possible via historique local

---

## 🔑 Comptes de démonstration

| Rôle | Email | PIN |
|------|-------|-----|
| 🔧 Administrateur | admin@medicare.com | 1234 |
| 👨‍⚕️ Médecin | martin@cabinet.fr | 1111 |
| 💪 Kiné | dubois@cabinet.fr | 2222 |
| 📋 Secrétaire | secretaire@cabinet.fr | 3333 |

---

## 🚀 Installation

### 1. Prérequis
- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)

### 2. Installation des dépendances

```bash
pip install streamlit reportlab
