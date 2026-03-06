# Job Automation Bot — First-Time Python Setup Guide

This guide is written for complete beginners. Follow each step in order.

## Step 1) Create a new project folder named `job_automation_bot`

A **project folder** is just a normal folder where all your files for this project will live.

Open your terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
mkdir job_automation_bot
cd job_automation_bot
```

### What this does
- `mkdir job_automation_bot` creates a new folder.
- `cd job_automation_bot` moves you into that folder.

---

## Step 2) Create a Python virtual environment named `venv`

A **virtual environment** is an isolated Python workspace for this project only.
It keeps project packages separate from the rest of your computer.

Run this command:

```bash
python -m venv venv
```

If `python` does not work, try:

```bash
python3 -m venv venv
```

### What this does
- `python -m venv venv` tells Python to create a virtual environment folder named `venv` inside your project.

---

## Step 3) Activate the virtual environment

Activation means: “Use the Python from this project’s `venv` right now.”

### On Windows (Command Prompt)

```bat
venv\Scripts\activate
```

### On Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

### On Mac/Linux

```bash
source venv/bin/activate
```

After activation, you should see `(venv)` at the start of your terminal line.

---

## Step 4) Verify that the virtual environment is activated

Run:

```bash
python --version
which python
```

On Windows, use this instead of `which`:

```bat
where python
```

### How to confirm
- If activated correctly, the Python path should point to something inside your project’s `venv` folder.
- Example (Mac/Linux): `/.../job_automation_bot/venv/bin/python`
- Example (Windows): `...\job_automation_bot\venv\Scripts\python.exe`

---

## Step 5) Create a `requirements.txt` file

This file stores the list of Python packages your project uses.

Create an empty file:

### Mac/Linux
```bash
touch requirements.txt
```

### Windows (PowerShell)
```powershell
New-Item requirements.txt -ItemType File
```

You can also create it with a text editor (Notepad, VS Code, etc.) and save as `requirements.txt`.

---

## Step 6) Add packages to `requirements.txt`

When you install packages, you can save them to this file.

Example:

```bash
pip install requests
pip freeze > requirements.txt
```

### What this does
- `pip install requests` installs a package.
- `pip freeze > requirements.txt` writes all installed packages (inside `venv`) to `requirements.txt`.

---

## Quick sanity check (recommended)

Run these commands while `(venv)` is active:

```bash
python --version
pip --version
```

If both commands run without errors, your setup is working.

---

## Optional: How to leave the virtual environment

When you are done, run:

```bash
deactivate
```

This returns your terminal to normal system Python.
