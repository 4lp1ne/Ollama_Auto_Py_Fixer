import sys
import subprocess
import time
import json
from pathlib import Path
import datetime
import shutil

MAX_ITERATIONS = 10
SLEEP_BETWEEN = 1  # secondes entre itérations
BACKUP_ROOT = Path("backups")


class AutoOrchestrator:
    def __init__(self):
        self.execution_results_dir = Path("execution_results")
        self.backup_root = BACKUP_ROOT
        self.backup_root.mkdir(exist_ok=True)

    def run_auto_return(self, project_path: Path) -> bool:
        print(f"[ORCH] => Lancement auto_return pour {project_path}")
        cmd = [
            sys.executable, "auto_return.py", "exec",
            "-p", str(project_path)
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        print(proc.stdout)
        if proc.returncode != 0:
            print(f"[ORCH][ERROR] auto_return a échoué (code {proc.returncode})")
            print(proc.stderr)
            return False
        return True

    def find_latest_summary_json(self, project_name: str) -> Path or None:
        proj_dir = self.execution_results_dir / project_name
        if not proj_dir.exists():
            return None
        json_files = list(proj_dir.glob("summary_*.json"))
        if not json_files:
            return None
        return max(json_files, key=lambda p: p.stat().st_mtime)

    def backup_and_write(self, file_path: Path, new_code: str, project_name: str):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_root / project_name / file_path.parent.relative_to(file_path.parents[len(file_path.parents) - 1])
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / (file_path.name + f".bak_{timestamp}")
        shutil.copy2(file_path, backup_file)
        print(f"[ORCH][BACKUP] {file_path} → {backup_file}")

        file_path.write_text(new_code, encoding="utf-8")
        print(f"[ORCH][PATCH] {file_path} corrigé")

    def run_auto_fixer(self, summary_path: Path, project_root: Path) -> bool:
        print(f"[ORCH] => Lancement auto_fixer sur {summary_path}")
        cmd = [sys.executable, "auto_fixer.py", "fix", str(summary_path)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        print(proc.stdout)
        if proc.returncode != 0:
            print(f"[ORCH][ERROR] auto_fixer a échoué : {proc.stderr}")
            return False
        return True

    def orchestrate(self, project_path: str):
        project_root = Path(project_path).resolve()
        if not project_root.exists() or not project_root.is_dir():
            print(f"[ORCH][ERROR] Le chemin projet n’existe pas : {project_root}")
            sys.exit(1)
        print(f"[ORCH] Démarrage orchestration sur projet : {project_root}")

        project_name = project_root.name

        for iteration in range(1, MAX_ITERATIONS + 1):
            print("\n" + "=" * 60)
            print(f"[ORCH] Itération {iteration}/{MAX_ITERATIONS}")
            print("=" * 60)

            ok = self.run_auto_return(project_root)
            if not ok:
                print("[ORCH] auto_return a échoué, arrêt.")
                return False

            summary = self.find_latest_summary_json(project_name)
            if summary is None:
                print("[ORCH][ERROR] Aucun summary JSON trouvé.")
                return False

            print(f"[ORCH] Utilisation du summary : {summary}")

            with open(summary, "r", encoding="utf-8") as f:
                summary_data = json.load(f)

            all_good = True
            for rel, info in summary_data.items():
                if not isinstance(info, dict):
                    continue  # Ignore les métadonnées comme "_project_root"

                rc = info.get("returncode", 0)
                stderr = info.get("stderr", "")
                if rc != 0 or (stderr and stderr.strip()):
                    all_good = False
                    print(f"[ORCH] Erreur détectée dans {rel} : rc={rc}, stderr: {stderr.strip()[:100]}")
                    break

            if all_good:
                print("[ORCH] Tous les scripts passent sans erreur — fin de l’orchestration.")
                return True

            print("[ORCH] Bugs détectés — application de correctifs...")

            ok_fix = self.run_auto_fixer(summary, project_root)
            if not ok_fix:
                print("[ORCH] Application des fixes échouée, arrêt.")
                return False

            print(f"[ORCH] Correctifs appliqués. Attente {SLEEP_BETWEEN}s avant la prochaine itération.")
            time.sleep(SLEEP_BETWEEN)

        print("[ORCH] Nombre max d’itérations atteint, orchestration terminée.")
        return False


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "run":
        print("Usage : python auto_orchestrator.py run <project_folder>")
        sys.exit(1)

    project_folder = sys.argv[2]
    orch = AutoOrchestrator()
    success = orch.orchestrate(project_folder)
    if success:
        print("[ORCH] Orchestration réussie")
        sys.exit(0)
    else:
        print("[ORCH] Orchestration échouée")
        sys.exit(1)


if __name__ == "__main__":
    main()
