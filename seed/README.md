# Jeu de Données Initial & Script d'Initialisation (Seed)

Ce dossier contient le script rejouable d'initialisation et les jeux de données JSON pour la base Baserow du projet **HelpDesk IA**.

---

## 🚀 Utilisation du script d'initialisation

Le script utilise uniquement la bibliothèque standard Python (`urllib`, `json`), **aucune installation via pip n'est nécessaire**.

### 1. Démarrer la stack Docker
```bash
docker compose up -d
```

### 2. Exécuter l'initialisation
```bash
python seed/init_baserow.py --email VOTRE_EMAIL_BASEROW --password VOTRE_MOT_DE_PASSE
```

Exemple par défaut :
```bash
python seed/init_baserow.py
```

---

## 📦 Ce que fait ce script automatiquement

1. **Authentification / Inscription automatique :** Se connecte à l'API Baserow (`http://localhost:8080/api/`) ou crée le premier administrateur si l'instance est neuve.
2. **Création de la base :** Vérifie ou crée la base de données `HelpDesk-IA` dans le workspace.
3. **Création des 6 tables imposées :**
   - `Collaborators`
   - `Technicians`
   - `Tickets`
   - `Replies`
   - `KnowledgeBase`
   - `AuditLog`
4. **Peuplement rejouable :**
   - 6 collaborateurs réalistes répartis sur Paris et Lyon (`seed/collaborators.json`).
   - 3 techniciens de support IT avec compétences et disponibilité (`seed/technicians.json`).
   - 5 articles documentaires complets pour la base de connaissances (`seed/knowledge_base.json`).
