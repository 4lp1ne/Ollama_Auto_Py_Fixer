Auto Orchestrator

Un système automatisé pour exécuter, analyser et corriger des projets Python de manière itérative.

🚀 Vue d'ensemble

Auto Orchestrator est un ensemble d'outils qui permet de :

· Exécuter automatiquement tous les scripts Python d'un projet
· Détecter les erreurs d'exécution
· Corriger automatiquement les bugs en utilisant l'IA (Ollama)
· Itérer jusqu'à ce que tous les scripts fonctionnent correctement

📁 Structure du projet

```
.
├── auto_orchestrator.py    # Orchestrateur principal
├── auto_return.py          # Exécuteur de scripts
├── auto_fixer.py           # Correcteur automatique
├── backups/               # Sauvegardes des fichiers modifiés
├── execution_results/     # Résultats d'exécution et logs
└── backup_scripts/        # Sauvegardes des correctifs
```

🛠️ Installation

1. Clonez le dépôt :

```bash
git clone <votre-repo>
cd auto-orchestrator
```

1. Installez les dépendances :

```bash
pip install -r requirements.txt
```

1. Installez Ollama :

· Téléchargez depuis ollama.ai
· Ou installez avec :

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

1. Téléchargez le modèle Llama :

```bash
ollama pull llama3:latest
```

🎯 Utilisation

Orchestration complète

```bash
python auto_orchestrator.py run /chemin/vers/votre/projet
```

Exécution seule des scripts

```bash
python auto_return.py exec -p /chemin/vers/projet
```

Correction manuelle

```bash
python auto_fixer.py fix /chemin/vers/summary_xxx.json
```

🔧 Fonctionnalités

Auto Return (auto_return.py)

· 🔍 Détecte automatiquement tous les scripts Python
· 🎯 Exécute d'abord les main.py, puis les autres scripts
· 📊 Génère des rapports détaillés d'exécution
· ⏱️ Gère les timeouts (5 minutes par défaut)

Auto Fixer (auto_fixer.py)

· 🤖 Utilise Ollama + Llama3 pour corriger les erreurs
· 🔄 Crée des sauvegardes avant modification
· 🧹 Nettoie le code généré par l'IA
· 📝 Gère plusieurs formats de réponse (markdown, triples quotes)

Auto Orchestrator (auto_orchestrator.py)

· 🔁 Processus itératif (max 10 itérations)
· 📈 Surveillance en temps réel des progrès
· 🛡️ Système de sauvegarde robuste
· 📋 Rapports de statut détaillés

⚙️ Configuration

Variables modifiables

```python
MAX_ITERATIONS = 10        # Nombre max d'itérations
SLEEP_BETWEEN = 1          # Secondes entre les itérations
IGNORED_DIRS = {'__pycache__', 'venv', 'env', 'Scripts'}  # Dossiers ignorés
```

Structure des résultats

```
execution_results/
└── nom_du_projet/
    ├── summary_YYYYMMDD_HHMMSS.json
    ├── chemin/vers/script1.py.log.txt
    └── chemin/vers/script2.py.log.txt
```

🎪 Exemple de workflow

1. Lancement :

```bash
python auto_orchestrator.py run ./mon-projet
```

1. Itération 1 :
   · Exécution de tous les scripts
   · Détection de 3 scripts avec erreurs
   · Génération des correctifs via IA
   · Application des correctifs
2. Itération 2 :
   · Ré-exécution des scripts corrigés
   · Plus que 1 script en erreur
   · Nouvelle correction...
3. Terminaison :
   · Soit tous les scripts fonctionnent ✅
   · Soit limite d'itérations atteinte ⏰

🛡️ Sécurité et sauvegardes

· Sauvegarde automatique de chaque fichier modifié
· Timestamp unique pour chaque modification
· Structure préservée dans les dossiers de backup
· Rollback manuel possible avec les fichiers .bak_*

🐛 Dépannage

Erreurs courantes

1. Ollama non installé :
   ```bash
   [FIX][OLLAMA ERROR] [Errno 2] No such file or directory: 'ollama'
   ```
   Solution : Installez Ollama et le modèle Llama3
2. Timeout Ollama :
   ```bash
   [FIX][OLLAMA ERROR] Timeout lors de l'appel à Ollama.
   ```
   Solution : Augmentez le timeout dans auto_fixer.py
3. Projet introuvable :
   ```bash
   [ORCH][ERROR] Le chemin projet n'existe pas
   ```
   Solution : Vérifiez le chemin absolu du projet

📊 Sorties

Fichiers générés

· summary_*.json : Métadonnées et résultats d'exécution
· *.log.txt : Logs détaillés par script
· backups/ : Sauvegardes des fichiers originaux
· backup_scripts/ : Historique des corrections

Format du summary JSON

```json
{
  "_project_root": "/chemin/absolu",
  "script1.py": {
    "returncode": 0,
    "stdout": "...",
    "stderr": ""
  },
  "script2.py": {
    "returncode": 1,
    "stdout": "",
    "stderr": "Error message..."
  }
}
```

🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

· Signaler des bugs
· Proposer des améliorations
· Soumettre des pull requests

📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

---

Note : Cet outil utilise l'IA générative pour corriger le code. Vérifiez toujours les modifications apportées à votre code source.Auto Orchestrator

Un système automatisé pour exécuter, analyser et corriger des projets Python de manière itérative.

🚀 Vue d'ensemble

Auto Orchestrator est un ensemble d'outils qui permet de :

· Exécuter automatiquement tous les scripts Python d'un projet
· Détecter les erreurs d'exécution
· Corriger automatiquement les bugs en utilisant l'IA (Ollama)
· Itérer jusqu'à ce que tous les scripts fonctionnent correctement

📁 Structure du projet

```
.
├── auto_orchestrator.py    # Orchestrateur principal
├── auto_return.py          # Exécuteur de scripts
├── auto_fixer.py           # Correcteur automatique
├── backups/               # Sauvegardes des fichiers modifiés
├── execution_results/     # Résultats d'exécution et logs
└── backup_scripts/        # Sauvegardes des correctifs
```

🛠️ Installation

1. Clonez le dépôt :

```bash
git clone <votre-repo>
cd auto-orchestrator
```

1. Installez les dépendances :

```bash
pip install -r requirements.txt
```

1. Installez Ollama :

· Téléchargez depuis ollama.ai
· Ou installez avec :

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

1. Téléchargez le modèle Llama :

```bash
ollama pull llama3:latest
```

🎯 Utilisation

Orchestration complète

```bash
python auto_orchestrator.py run /chemin/vers/votre/projet
```

Exécution seule des scripts

```bash
python auto_return.py exec -p /chemin/vers/projet
```

Correction manuelle

```bash
python auto_fixer.py fix /chemin/vers/summary_xxx.json
```

🔧 Fonctionnalités

Auto Return (auto_return.py)

· 🔍 Détecte automatiquement tous les scripts Python
· 🎯 Exécute d'abord les main.py, puis les autres scripts
· 📊 Génère des rapports détaillés d'exécution
· ⏱️ Gère les timeouts (5 minutes par défaut)

Auto Fixer (auto_fixer.py)

· 🤖 Utilise Ollama + Llama3 pour corriger les erreurs
· 🔄 Crée des sauvegardes avant modification
· 🧹 Nettoie le code généré par l'IA
· 📝 Gère plusieurs formats de réponse (markdown, triples quotes)

Auto Orchestrator (auto_orchestrator.py)

· 🔁 Processus itératif (max 10 itérations)
· 📈 Surveillance en temps réel des progrès
· 🛡️ Système de sauvegarde robuste
· 📋 Rapports de statut détaillés

⚙️ Configuration

Variables modifiables

```python
MAX_ITERATIONS = 10        # Nombre max d'itérations
SLEEP_BETWEEN = 1          # Secondes entre les itérations
IGNORED_DIRS = {'__pycache__', 'venv', 'env', 'Scripts'}  # Dossiers ignorés
```

Structure des résultats

```
execution_results/
└── nom_du_projet/
    ├── summary_YYYYMMDD_HHMMSS.json
    ├── chemin/vers/script1.py.log.txt
    └── chemin/vers/script2.py.log.txt
```

🎪 Exemple de workflow

1. Lancement :

```bash
python auto_orchestrator.py run ./mon-projet
```

1. Itération 1 :
   · Exécution de tous les scripts
   · Détection de 3 scripts avec erreurs
   · Génération des correctifs via IA
   · Application des correctifs
2. Itération 2 :
   · Ré-exécution des scripts corrigés
   · Plus que 1 script en erreur
   · Nouvelle correction...
3. Terminaison :
   · Soit tous les scripts fonctionnent ✅
   · Soit limite d'itérations atteinte ⏰

🛡️ Sécurité et sauvegardes

· Sauvegarde automatique de chaque fichier modifié
· Timestamp unique pour chaque modification
· Structure préservée dans les dossiers de backup
· Rollback manuel possible avec les fichiers .bak_*

🐛 Dépannage

Erreurs courantes

1. Ollama non installé :
   ```bash
   [FIX][OLLAMA ERROR] [Errno 2] No such file or directory: 'ollama'
   ```
   Solution : Installez Ollama et le modèle Llama3
2. Timeout Ollama :
   ```bash
   [FIX][OLLAMA ERROR] Timeout lors de l'appel à Ollama.
   ```
   Solution : Augmentez le timeout dans auto_fixer.py
3. Projet introuvable :
   ```bash
   [ORCH][ERROR] Le chemin projet n'existe pas
   ```
   Solution : Vérifiez le chemin absolu du projet

📊 Sorties

Fichiers générés

· summary_*.json : Métadonnées et résultats d'exécution
· *.log.txt : Logs détaillés par script
· backups/ : Sauvegardes des fichiers originaux
· backup_scripts/ : Historique des corrections

Format du summary JSON

```json
{
  "_project_root": "/chemin/absolu",
  "script1.py": {
    "returncode": 0,
    "stdout": "...",
    "stderr": ""
  },
  "script2.py": {
    "returncode": 1,
    "stdout": "",
    "stderr": "Error message..."
  }
}
```

🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

· Signaler des bugs
· Proposer des améliorations
· Soumettre des pull requests
