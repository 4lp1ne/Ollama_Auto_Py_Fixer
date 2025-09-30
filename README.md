# 🛠️ Ollama Auto Py Fixer

> An automated system to **run**, **analyze**, and **auto-fix** Python scripts using AI — powered by [Ollama](https://ollama.ai).

---

## 🚀 Overview

![20250930_164331.jpg](https://github.com/user-attachments/assets/f2e9f13e-b4b8-46d5-a36c-56752ed00f2b)

**Ollama Auto Py Fixer** enables:

✅ Automatic execution of all Python scripts in a project
🐞 Runtime error detection
🤖 Automatic bug fixing using AI (LLaMA via Ollama)
🔁 Iterative refinement until everything works

---

## 📁 Project Structure

```
.
├── auto_orchestrator.py     # Main orchestrator
├── auto_return.py           # Script executor
├── auto_fixer.py            # Automatic fixer
├── backups/                 # Backup of original files
├── execution_results/       # Logs and summaries
└── backup_scripts/          # Correction history
```

---

## 🧩 Requirements

> 💡 Minimal dependencies — only standard library (Python ≥3.4)

**Standard Library Used:**

* `sys`, `subprocess`, `json`, `shutil`, `re`
* `pathlib` (or `pathlib2` for Python < 3.4)
* `datetime`, `time`, `argparse`

Install optional backport (for old Python versions):

```text
pathlib2>=2.3.7; python_version < '3.4'
```

> 🔧 No third-party packages required.
> ⚠️ **Ollama must be installed manually** (see below).

---

## 🛠️ Installation

1. **Clone the repo**

```bash
git clone <your-repo>
cd auto-orchestrator
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Install Ollama**

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

4. **Pull the Llama3 model**

```bash
ollama pull llama3:latest
```

---

## 🎯 Usage

### 🔄 Full Orchestration

```bash
python auto_orchestrator.py run /path/to/your/project
```

### ▶️ Script Execution Only

```bash
python auto_return.py exec -p /path/to/your/project
```

### 🛠️ Manual Fix

```bash
python auto_fixer.py fix /path/to/summary_xxx.json
```

---

## 🔧 Features

### 📂 Auto Return (`auto_return.py`)

* Detects all `.py` files in the project
* Runs `main.py` scripts first
* Times out after 5 minutes per script (default)
* Logs outputs + errors

---

### 🤖 Auto Fixer (`auto_fixer.py`)

* Uses **LLaMA via Ollama** to analyze and fix errors
* Handles:

  * Markdown and triple-quoted responses
  * Edge cases and formatting
* Creates full backups before modification

---

### 🔁 Auto Orchestrator (`auto_orchestrator.py`)

* Runs full iterative cycle:

  1. Execute → 2. Detect Errors → 3. Fix → 4. Repeat
* Up to **10 iterations**
* Real-time progress and summary logging
* Intelligent backup handling

---

## ⚙️ Configuration

Modify variables in `auto_orchestrator.py` as needed:

```python
MAX_ITERATIONS = 10
SLEEP_BETWEEN = 1  # seconds
IGNORED_DIRS = {'__pycache__', 'venv', 'env', 'Scripts'}
```

---

## 📊 Output Structure

```
execution_results/
└── your_project/
    ├── summary_YYYYMMDD_HHMMSS.json
    ├── path/to/script1.py.log.txt
    └── path/to/script2.py.log.txt
```

### ✅ Sample Summary JSON

```json
{
  "_project_root": "/absolute/path",
  "script1.py": {
    "returncode": 0,
    "stdout": "Execution output...",
    "stderr": ""
  },
  "script2.py": {
    "returncode": 1,
    "stdout": "",
    "stderr": "Traceback (most recent call last)..."
  }
}
```

---

## 🛡️ Backups & Rollback

* Each modified file backed up in:

  * `backups/` — Original code
  * `backup_scripts/` — Fixed versions
* File names include **timestamps**
* `.bak_*` files allow **manual rollback**

---

## 🐛 Troubleshooting

### ❌ Ollama Not Installed

```bash
[FIX][OLLAMA ERROR] [Errno 2] No such file or directory: 'ollama'
```

**Solution:** Install Ollama and `llama3`

---

### 🕒 Ollama Timeout

```bash
[FIX][OLLAMA ERROR] Timeout during Ollama call.
```

**Solution:** Increase timeout in `auto_fixer.py`

---

### 📂 Project Path Error

```bash
[ORCH][ERROR] Project path does not exist
```

**Solution:** Check your project path is correct and absolute

---

## 🧑‍💻 Contribution

All contributions welcome:

* 🐞 Bug reports
* 🚀 Feature requests
* 📦 Pull requests

---

## 📄 License

**MIT License** — see `LICENSE` file for full terms.

---

## ⚠️ Disclaimer

> This tool uses **AI-generated code** to fix your files. Always review and test any modifications before deploying or committing changes.




