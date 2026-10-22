"""
Script d'initialisation et de peuplement (Seed) rejouable pour Baserow - HelpDesk IA
Projet ESGI 5ème année - NoCode Avancé
"""

import sys
import json
import urllib.request
import urllib.error
import argparse

DEFAULT_BASE_URL = "http://localhost:8080"

# --- Jeu de données initial ---
SEED_DATA = {
    "collaborators": [
        {"first_name": "Jean", "last_name": "Dupont", "email": "test@test.com", "team": "Tech", "site": "Paris", "role": "Développeur Senior"},
        {"first_name": "Sophie", "last_name": "Laurent", "email": "sophie.laurent@northwind.com", "team": "Sales", "site": "Paris", "role": "Commerciale Grand Compte"},
        {"first_name": "Thomas", "last_name": "Bernard", "email": "thomas.bernard@northwind.com", "team": "HR", "site": "Lyon", "role": "Responsable RH"},
        {"first_name": "Emma", "last_name": "Petit", "email": "emma.petit@northwind.com", "team": "Operations", "site": "Paris", "role": "Cheffe de projet Logistique"},
        {"first_name": "Lucas", "last_name": "Roux", "email": "lucas.roux@northwind.com", "team": "Tech", "site": "Lyon", "role": "Ingénieur DevOps"},
        {"first_name": "Claire", "last_name": "Dubois", "email": "claire.dubois@northwind.com", "team": "Sales", "site": "Lyon", "role": "Chargée de clientèle"}
    ],
    "technicians": [
        {
            "name": "Alice Martin",
            "email": "alice@northwind.com",
            "skills": ["access", "software", "onboarding"],
            "open_tickets": 0,
            "available": True
        },
        {
            "name": "Bob Bernard",
            "email": "bob@northwind.com",
            "skills": ["network", "hardware"],
            "open_tickets": 0,
            "available": True
        },
        {
            "name": "Charlie Chen",
            "email": "charlie@northwind.com",
            "skills": ["hardware", "software", "access"],
            "open_tickets": 0,
            "available": True
        }
    ],
    "knowledge_base": [
        {
            "title": "Procédure de connexion au VPN Cisco AnyConnect",
            "category": "network",
            "keywords": "vpn, cisco, anyconnect, connexion, télétravail, réseau",
            "content": "Pour vous connecter au réseau d'entreprise depuis votre poste en télétravail :\n1. Lancez le client Cisco AnyConnect Secure Mobility Client.\n2. Saisissez l'adresse de passerelle : vpn.northwind.com:443.\n3. Entrez vos identifiants Active Directory (votre email d'entreprise et votre mot de passe habituel).\n4. Validez l'invite d'authentification multifacteur (MFA) reçue sur votre application mobile.\nEn cas d'échec répété, redémarrez votre box internet et assurez-vous qu'aucun antivirus tiers ne bloque le port 443."
        },
        {
            "title": "Réinitialisation de mot de passe et déblocage de compte",
            "category": "access",
            "keywords": "mot de passe, password, active directory, compte bloqué, login, accès",
            "content": "Si votre compte Windows est verrouillé suite à plusieurs tentatives erronées :\n1. Attendez 15 minutes pour le déverrouillage automatique de sécurité.\n2. Si le problème persiste, rendez-vous sur le portail interne https://password.northwind.internal depuis un appareil connecté.\n3. Renseignez votre adresse email et répondez à vos questions de sécurité.\n4. Votre nouveau mot de passe doit comporter au moins 12 caractères, incluant majuscules, minuscules, chiffres et un caractère spécial."
        },
        {
            "title": "Demande et gestion des licences logicielles",
            "category": "software",
            "keywords": "licence, logiciel, software, office, figma, jetbrains, installation",
            "content": "L'attribution des licences bureautiques et métiers est automatisée selon votre rôle :\n- Pack Microsoft 365 : attribué par défaut à tout nouvel arrivant dès la création du compte.\n- JetBrains & GitHub Copilot : réservé à l'équipe Tech sur simple validation du Lead Dev.\n- Adobe Creative Cloud & Figma : réservé aux équipes Marketing et Produit.\nToute demande complémentaire doit être formalisée avec l'accord écrit du manager direct."
        },
        {
            "title": "Remplacement et commande de matériel informatique",
            "category": "hardware",
            "keywords": "matériel, hardware, écran, clavier, souris, chargeur, docking, ordinateur",
            "content": "Le catalogue de matériel standard Northwind Industries comprend :\n- Écran externe 27 pouces Dell USB-C avec hub intégré.\n- Ensemble clavier/souris sans fil ergonomique Logitech.\n- Câble de chargeur USB-C 65W ou 100W.\nPour toute demande de renouvellement ou commande de périphérique défectueux, précisez le numéro de série de votre PC portable dans la demande."
        },
        {
            "title": "Résolution des incidents de poste de travail Windows 11",
            "category": "hardware",
            "keywords": "windows, écran bleu, crash, lenteur, redémarrage, mise à jour",
            "content": "En cas de dysfonctionnement de votre poste de travail (écran bleu BSOD, freeze système) :\n1. Débranchez tous les périphériques externes (écrans, stations d'accueil, clés USB).\n2. Maintenez le bouton d'alimentation enfoncé pendant 15 secondes pour forcer une réinitialisation électrique complète.\n3. Rallumez le PC et vérifiez la présence de mises à jour dans Windows Update."
        }
    ]
}


class BaserowClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.jwt_token = None

    def request(self, method, endpoint, data=None, token=None):
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Host": "localhost:8080"
        }
        auth_token = token or self.jwt_token
        if auth_token:
            headers["Authorization"] = f"JWT {auth_token}"

        req_body = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=req_body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                return json.loads(res_body) if res_body else None
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                error_json = json.loads(error_body)
            except Exception:
                error_json = error_body
            raise RuntimeError(f"HTTP {e.code} on {endpoint}: {error_json}")

    def login(self, email, password):
        print(f"[*] Authentification sur Baserow avec {email}...")
        res = self.request("POST", "/api/user/token-auth/", {"username": email, "password": password})
        self.jwt_token = res["token"]
        print("[+] Connecté avec succès !")
        return self.jwt_token

    def register_if_needed(self, email, password, name="Admin Northwind"):
        try:
            return self.login(email, password)
        except Exception:
            print("[*] Compte introuvable, tentative d'inscription du premier administrateur...")
            try:
                self.request("POST", "/api/user/", {"email": email, "password": password, "name": name})
                print("[+] Compte créé avec succès !")
                return self.login(email, password)
            except Exception as e:
                print(f"[!] Échec d'inscription : {e}")
                raise

    def get_workspaces(self):
        return self.request("GET", "/api/workspaces/")

    def get_applications(self, workspace_id):
        return self.request("GET", f"/api/applications/workspace/{workspace_id}/")

    def create_database(self, workspace_id, name="HelpDesk-IA"):
        return self.request("POST", f"/api/applications/workspace/{workspace_id}/", {
            "name": name,
            "type": "database"
        })

    def get_tables(self, database_id):
        return self.request("GET", f"/api/database/tables/database/{database_id}/")

    def create_table(self, database_id, name):
        return self.request("POST", f"/api/database/tables/database/{database_id}/", {"name": name})

    def get_fields(self, table_id):
        return self.request("GET", f"/api/database/fields/table/{table_id}/")

    def create_field(self, table_id, name, field_type, **kwargs):
        payload = {"name": name, "type": field_type, **kwargs}
        return self.request("POST", f"/api/database/fields/table/{table_id}/", payload)

    def insert_row(self, table_id, row_data):
        return self.request("POST", f"/api/database/rows/table/{table_id}/?user_field_names=true", row_data)

    def get_rows(self, table_id):
        return self.request("GET", f"/api/database/rows/table/{table_id}/?user_field_names=true")

    def create_database_token(self, workspace_id, name="n8n-token"):
        return self.request("POST", "/api/database/tokens/", {
            "name": name,
            "workspace": workspace_id,
            "permissions": {"create": True, "read": True, "update": True, "delete": True}
        })


def setup_and_seed(base_url, email, password):
    client = BaserowClient(base_url)
    client.register_if_needed(email, password)

    # 1. Vérifier ou récupérer le workspace
    workspaces = client.get_workspaces()
    if not workspaces:
        raise RuntimeError("Aucun workspace trouvé. Veuillez en créer un dans Baserow.")
    workspace = workspaces[0]
    workspace_id = workspace["id"]
    print(f"[+] Workspace cible : '{workspace['name']}' (ID: {workspace_id})")

    # 2. Vérifier ou créer la base HelpDesk-IA
    apps = client.get_applications(workspace_id)
    db = next((app for app in apps if app["name"] == "HelpDesk-IA" and app["type"] == "database"), None)
    if not db:
        print("[*] Création de la base de données 'HelpDesk-IA'...")
        db = client.create_database(workspace_id, "HelpDesk-IA")
    db_id = db["id"]
    print(f"[+] Base de données HelpDesk-IA prête (ID: {db_id})")

    # 3. Récupérer les tables existantes
    existing_tables = client.get_tables(db_id)
    table_map = {t["name"]: t["id"] for t in existing_tables}

    tables_needed = ["Collaborators", "Technicians", "Tickets", "Replies", "KnowledgeBase", "AuditLog"]
    for t_name in tables_needed:
        if t_name not in table_map:
            print(f"[*] Création de la table '{t_name}'...")
            new_t = client.create_table(db_id, t_name)
            table_map[t_name] = new_t["id"]
        else:
            print(f"[=] Table '{t_name}' déjà existante (ID: {table_map[t_name]})")

    # 4. Peuplement des Collaborateurs
    collab_table_id = table_map["Collaborators"]
    current_collabs = client.get_rows(collab_table_id).get("results", [])
    if len(current_collabs) == 0:
        print("[*] Insertion des collaborateurs de test...")
        for c in SEED_DATA["collaborators"]:
            try:
                client.insert_row(collab_table_id, c)
            except Exception as e:
                print(f"[!] Erreur insertion collaborateur {c['email']}: {e}")
        print("[+] Collaborateurs insérés avec succès !")
    else:
        print(f"[=] {len(current_collabs)} collaborateurs déjà présents.")

    # 5. Peuplement des Techniciens
    tech_table_id = table_map["Technicians"]
    current_techs = client.get_rows(tech_table_id).get("results", [])
    if len(current_techs) == 0:
        print("[*] Insertion des techniciens de test...")
        for tech in SEED_DATA["technicians"]:
            try:
                client.insert_row(tech_table_id, tech)
            except Exception as e:
                print(f"[!] Erreur insertion technicien {tech['name']}: {e}")
        print("[+] Techniciens insérés avec succès !")
    else:
        print(f"[=] {len(current_techs)} techniciens déjà présents.")

    # 6. Peuplement de la Base de Connaissances (KnowledgeBase)
    kb_table_id = table_map["KnowledgeBase"]
    current_kb = client.get_rows(kb_table_id).get("results", [])
    if len(current_kb) == 0:
        print("[*] Insertion des articles documentaires (KnowledgeBase)...")
        for art in SEED_DATA["knowledge_base"]:
            try:
                client.insert_row(kb_table_id, art)
            except Exception as e:
                print(f"[!] Erreur insertion article '{art['title']}': {e}")
        print("[+] Base de connaissances initialisée !")
    else:
        print(f"[=] {len(current_kb)} articles déjà présents.")

    print("\n" + "=" * 50)
    print("✅ INITIALISATION BASEROW TERMINÉE AVEC SUCCÈS !")
    print("=" * 50)
    print(f"Database ID : {db_id}")
    for name, tid in table_map.items():
        print(f"- Table '{name}' -> ID: {tid}")
    print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de seed rejouable Baserow pour HelpDesk IA")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="URL de Baserow (défaut: http://localhost:8080)")
    parser.add_argument("--email", default="admin@northwind.com", help="Email administrateur Baserow")
    parser.add_argument("--password", default="Admin123456!", help="Mot de passe administrateur")
    args = parser.parse_args()

    setup_and_seed(args.url, args.email, args.password)
