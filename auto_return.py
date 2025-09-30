import sys
import subprocess
from pathlib import Path
import json
import datetime

IGNORED_DIRS = {'__pycache__', 'venv', 'env', 'Scripts', '.venv', '.env'}

def is_ignored_dir(path: Path):
    return any(part in IGNORED_DIRS for part in path.parts)

def find_python_scripts(project_root: Path):
    scripts = []
    for path in project_root.rglob('*.py'):
        if is_ignored_dir(path.parent):
            continue
        scripts.append(path)
    return scripts

def run_script(script_path: Path):
    print(f"[EXEC] Running script: {script_path}")
    cmd = [sys.executable, str(script_path)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout expired for script: {script_path}")
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": "TimeoutExpired"
        }
    except Exception as e:
        print(f"[ERROR] Exception running script {script_path}: {e}")
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e)
        }

def save_results(project_name: str, project_root: Path, results: dict):
    base_dir = Path("execution_results") / project_name
    base_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = base_dir / f"summary_{timestamp}.json"

    # Ajoute le chemin racine au résumé
    results["_project_root"] = str(project_root)

    # Enregistre le résumé global
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    # Enregistre aussi les logs individuels
    for rel_script, res in results.items():
        if rel_script == "_project_root":
            continue
        log_file = base_dir / (rel_script + ".log.txt")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"Returncode: {res['returncode']}\n\n")
            f.write(f"STDOUT:\n{res['stdout']}\n\n")
            f.write(f"STDERR:\n{res['stderr']}\n")

    print(f"[INFO] Results saved in {summary_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="auto_return.py - exec mode")
    parser.add_argument("command", choices=["exec"], help="Command to run")
    parser.add_argument("-p", "--project_path", required=True, help="Path to project folder")
    args = parser.parse_args()

    project_root = Path(args.project_path).resolve()
    if not project_root.exists() or not project_root.is_dir():
        print(f"[ERROR] Project path does not exist or is not a directory: {project_root}")
        sys.exit(1)

    project_name = project_root.name

    # Find all python scripts
    all_scripts = find_python_scripts(project_root)
    print(f"[INFO] Found {len(all_scripts)} python scripts in project {project_name}")

    # Identify main.py scripts (could be multiple in subfolders)
    main_scripts = [s for s in all_scripts if s.name == "main.py"]

    results = {}

    # Always run main.py scripts first
    for main_script in main_scripts:
        rel_path = main_script.relative_to(project_root).as_posix()
        res = run_script(main_script)
        results[rel_path] = res

    # Then run other scripts (excluding those run above)
    other_scripts = [s for s in all_scripts if s.name != "main.py"]
    for script in other_scripts:
        rel_path = script.relative_to(project_root).as_posix()
        res = run_script(script)
        results[rel_path] = res

    # Save results and logs
    save_results(project_name, project_root, results)



if __name__ == "__main__":
    main()
