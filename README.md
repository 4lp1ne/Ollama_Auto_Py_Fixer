Ollama Auto Py Fixer

An automated system for executing, analyzing, and fixing Python projects iteratively.

🚀 Overview

Auto Orchestrator is a set of tools that enables:

· Automatically executing all Python scripts in a project
· Detecting runtime errors
· Automatically fixing bugs using AI (Ollama)
· Iterating until all scripts work correctly

📁 Project Structure

```
.
├── auto_orchestrator.py    # Main orchestrator
├── auto_return.py          # Script executor
├── auto_fixer.py           # Automatic fixer
├── backups/               # Backups of modified files
├── execution_results/     # Execution results and logs
└── backup_scripts/        # Backup of corrections
```

🛠️ Installation

1. Clone the repository:

```bash
git clone <your-repo>
cd auto-orchestrator
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Install Ollama:

· Download from ollama.ai
· Or install with:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

1. Download the Llama model:

```bash
ollama pull llama3:latest
```

🎯 Usage

Complete Orchestration

```bash
python auto_orchestrator.py run /path/to/your/project
```

Script Execution Only

```bash
python auto_return.py exec -p /path/to/project
```

Manual Correction

```bash
python auto_fixer.py fix /path/to/summary_xxx.json
```

🔧 Features

Auto Return (auto_return.py)

· 🔍 Automatically detects all Python scripts
· 🎯 Executes main.py files first, then other scripts
· 📊 Generates detailed execution reports
· ⏱️ Handles timeouts (5 minutes by default)

Auto Fixer (auto_fixer.py)

· 🤖 Uses Ollama + Llama3 to fix errors
· 🔄 Creates backups before modification
· 🧹 Cleans AI-generated code
· 📝 Handles multiple response formats (markdown, triple quotes)

Auto Orchestrator (auto_orchestrator.py)

· 🔁 Iterative process (max 10 iterations)
· 📈 Real-time progress monitoring
· 🛡️ Robust backup system
· 📋 Detailed status reports

⚙️ Configuration

Modifiable Variables

```python
MAX_ITERATIONS = 10        # Maximum number of iterations
SLEEP_BETWEEN = 1          # Seconds between iterations
IGNORED_DIRS = {'__pycache__', 'venv', 'env', 'Scripts'}  # Ignored directories
```

Results Structure

```
execution_results/
└── project_name/
    ├── summary_YYYYMMDD_HHMMSS.json
    ├── path/to/script1.py.log.txt
    └── path/to/script2.py.log.txt
```

🎪 Example Workflow

1. Launch:

```bash
python auto_orchestrator.py run ./my-project
```

1. Iteration 1:
   · Execution of all scripts
   · Detection of 3 scripts with errors
   · Generation of fixes via AI
   · Application of fixes
2. Iteration 2:
   · Re-execution of corrected scripts
   · Only 1 script remaining with errors
   · New correction...
3. Termination:
   · Either all scripts work ✅
   · Or iteration limit reached ⏰

🛡️ Security and Backups

· Automatic backup of each modified file
· Unique timestamp for each modification
· Preserved structure in backup folders
· Manual rollback possible with .bak_* files

🐛 Troubleshooting

Common Errors

1. Ollama not installed:
   ```bash
   [FIX][OLLAMA ERROR] [Errno 2] No such file or directory: 'ollama'
   ```
   Solution: Install Ollama and the Llama3 model
2. Ollama timeout:
   ```bash
   [FIX][OLLAMA ERROR] Timeout during Ollama call.
   ```
   Solution: Increase timeout in auto_fixer.py
3. Project not found:
   ```bash
   [ORCH][ERROR] Project path does not exist
   ```
   Solution: Verify the absolute project path

📊 Outputs

Generated Files

· summary_*.json: Metadata and execution results
· *.log.txt: Detailed logs per script
· backups/: Backups of original files
· backup_scripts/: Correction history

Summary JSON Format

```json
{
  "_project_root": "/absolute/path",
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

Contributions are welcome! Feel free to:

· Report bugs
· Propose improvements
· Submit pull requests

📄 License

MIT License - See LICENSE file for details.

---

Note: This tool uses generative AI to fix code. Always verify modifications made to your source code.