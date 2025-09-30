import sys
import json
import shutil
import subprocess
import re
from pathlib import Path
from datetime import datetime

BACKUP_ROOT = Path("backup_scripts")

def clean_code_from_markdown(text: str) -> str:
    # Supprime les blocs markdown (```python ... ```), '''...''', """..."""
    text = re.sub(r"```(?:python)?\n(.*?)```", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"'''(.*?)'''", r"\1", text, flags=re.DOTALL)
    text = re.sub(r'"""(.*?)"""', r"\1", text, flags=re.DOTALL)
    return text.strip()

def query_ollama_fix(script_content: str, error_log: str) -> str:
    prompt = f"""
Voici un script Python avec des erreurs. Analyse le script et l’erreur, puis propose une version corrigée complète.

Script :
\"\"\"
{script_content}
\"\"\"

Erreur :
\"\"\"
{error_log}
\"\"\"

Donne-moi **uniquement** le code corrigé sans balises markdown ni explications.
"""
    try:
        proc = subprocess.run(
            ["ollama", "run", "llama3:latest", prompt],
            capture_output=True, text=True, encoding='utf-8', timeout=300
        )
    except subprocess.TimeoutExpired:
        print("[FIX][OLLAMA ERROR] Timeout lors de l’appel à Ollama.")
        return None

    if proc.returncode == 0:
        return proc.stdout.strip()
    else:
        print("[FIX][OLLAMA ERROR]", proc.stderr)
        return None

def backup_file(filepath: Path, project_name: str, project_root: Path):
    # Crée un backup dans backup_scripts/<project_name>/... avec structure relative
    rel_path = filepath.relative_to(project_root)
    backup_dir = BACKUP_ROOT / project_name / rel_path.parent
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / (filepath.name + f".bak_{ts}")
    shutil.copy2(filepath, backup_path)
    print(f"[BACKUP] {filepath} -> {backup_path}")

def auto_fix(summary_json_path: Path):
    with open(summary_json_path, "r", encoding="utf-8") as f:
        summary = json.load(f)

    # Extraction du projet racine depuis le summary (doit être dans _project_root)
    project_root_str = summary.get("_project_root", None)
    if not project_root_str:
        print("[FIX][ERROR] _project_root absent du summary, impossible de localiser les fichiers.")
        sys.exit(1)
    project_root = Path(project_root_str).resolve()
    project_name = project_root.name
    print(f"[FIX] Projet racine estimé : {project_root}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for rel_path_str, info in summary.items():
        # Ignore la clé spéciale _project_root
        if rel_path_str == "_project_root":
            continue

        rc = info.get("returncode", 0)
        stderr = info.get("stderr", "")
        if rc == 0 and not stderr.strip():
            print(f"[FIX] Pas d’erreur détectée pour {rel_path_str}, skip.")
            continue

        source_file = project_root / rel_path_str
        if not source_file.exists():
            print(f"[FIX][WARN] Fichier à corriger introuvable : {source_file}")
            continue

        print(f"[FIX] Correction de {rel_path_str}")

        original_code = source_file.read_text(encoding="utf-8")
        fixed_code = query_ollama_fix(original_code, stderr)
        if not fixed_code:
            print(f"[FIX][FAIL] Aucun correctif obtenu pour {rel_path_str}")
            continue

        fixed_code = clean_code_from_markdown(fixed_code)

        # Backup avant écriture
        backup_file(source_file, project_name, project_root)

        # Écrase le fichier original avec le correctif
        source_file.write_text(fixed_code, encoding="utf-8")
        print(f"[FIX][PATCH] {source_file} mis à jour")

    print("[FIX] Correctifs appliqués.")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "fix":
        print("Usage: python auto_fixer.py fix <summary_json_path>")
        sys.exit(1)

    summary_path = Path(sys.argv[2])
    if not summary_path.exists():
        print(f"[FIX][ERROR] Fichier summary JSON non trouvé : {summary_path}")
        sys.exit(1)

    auto_fix(summary_path)
