# Deploying Your Python Job Automation System on Ubuntu (Beginner Guide)

This guide shows how to deploy your project on a Linux cloud server (Ubuntu) step by step.

---

## 1) Create an Ubuntu cloud server

You can use any cloud provider (AWS, Azure, GCP, DigitalOcean, Linode, etc.).

When creating the server:
- Choose **Ubuntu 22.04 LTS** (or Ubuntu 24.04 LTS).
- Choose at least **1 vCPU / 2GB RAM** for small workloads.
- Add an **SSH key** during setup (recommended).
- Open firewall ports:
  - **22** (SSH)
  - **8501** (Streamlit dashboard, optional)

### Why this matters
- Ubuntu gives a stable Linux environment.
- SSH key login is safer than password login.

---

## 2) Connect to server using SSH

From your local computer terminal:

```bash
ssh -i /path/to/your/private_key.pem ubuntu@YOUR_SERVER_IP
```

Example:

```bash
ssh -i ~/.ssh/jobbot_key ubuntu@203.0.113.10
```

### If this is your first connection
Type `yes` when asked to trust the host.

---

## 3) Update Ubuntu and install Python tools

After logging into server:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git tmux
```

### Why this matters
- `python3-venv` is required to create a virtual environment.
- `tmux` helps keep processes running after SSH disconnects.

---

## 4) Upload project files to server

You have two common options.

### Option A (recommended): Clone from Git repo

```bash
git clone <YOUR_REPOSITORY_URL>
cd Job-app
```

### Option B: Copy local folder with SCP
Run this from your **local machine**:

```bash
scp -i /path/to/private_key.pem -r /path/to/Job-app ubuntu@YOUR_SERVER_IP:~/
```

Then on server:

```bash
cd ~/Job-app
```

---

## 5) Create and activate Python virtual environment

Inside your project folder:

```bash
python3 -m venv venv
source venv/bin/activate
```

You should now see `(venv)` in your terminal prompt.

---

## 6) Install dependencies from `requirements.txt`

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Playwright extra setup (important)
Your project uses Playwright, so also run:

```bash
python -m playwright install chromium
```

If Ubuntu missing system libraries, run:

```bash
sudo npx playwright install-deps
```

(If `npx` is unavailable, install Node.js first or manually install required libs.)

---

## 7) Set environment variables (email credentials, API keys)

If your app needs secrets (SMTP password, API keys), do **not** hardcode them.

### Temporary (current session)

```bash
export EMAIL_SENDER="you@example.com"
export EMAIL_PASSWORD="your_app_password"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export OPENAI_API_KEY="your_key_if_used_later"
```

### Persistent (survives reboot/login)
Add to `~/.bashrc`:

```bash
nano ~/.bashrc
```

Add lines:

```bash
export EMAIL_SENDER="you@example.com"
export EMAIL_PASSWORD="your_app_password"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
```

Save and reload:

```bash
source ~/.bashrc
```

### Verify variables

```bash
echo $EMAIL_SENDER
echo $SMTP_SERVER
```

---

## 8) Run the automation pipeline manually

Inside project folder with venv active:

```bash
python run_auto_apply.py
```

### What this does
- Scrapes jobs
- Filters jobs
- Evaluates match
- Routes to ATS automation
- Stores status in SQLite

---

## 9) Schedule automation with cron (every 6 hours)

Open crontab:

```bash
crontab -e
```

Add this line:

```cron
0 */6 * * * cd /home/ubuntu/Job-app && /home/ubuntu/Job-app/venv/bin/python run_auto_apply.py >> /home/ubuntu/Job-app/logs/auto_apply.log 2>&1
```

Create log folder first:

```bash
mkdir -p /home/ubuntu/Job-app/logs
```

### Cron expression meaning
- `0 */6 * * *` = run at minute 0, every 6th hour.

### Check cron status

```bash
crontab -l
```

---

## 10) Run Streamlit dashboard on server

From project folder with venv active:

```bash
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
```

Then open in browser:

```text
http://YOUR_SERVER_IP:8501
```

### Important
Make sure port **8501** is allowed in cloud firewall/security group.

---

## 11) Keep long-running processes alive after SSH disconnect

### Option A: tmux (recommended)

Start tmux session:

```bash
tmux new -s jobbot
```

Run your command inside tmux, e.g.:

```bash
source venv/bin/activate
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
```

Detach from tmux (process keeps running):
- Press `Ctrl+B`, then `D`

Reattach later:

```bash
tmux attach -t jobbot
```

### Option B: screen

```bash
screen -S jobbot
```

Detach:
- Press `Ctrl+A`, then `D`

Reattach:

```bash
screen -r jobbot
```

---

## 12) Practical production tips (beginner-friendly)

- Use **app passwords** for email providers (not your normal password).
- Back up `job_applications.db` regularly.
- Rotate logs so disk does not fill up.
- Start small (manual run first), then enable cron.
- Test one ATS flow at a time to avoid account lock issues.

---

## Quick deployment checklist

1. Create Ubuntu server ✅
2. SSH into server ✅
3. Install Python + tools ✅
4. Upload code ✅
5. Create/activate venv ✅
6. Install dependencies + Playwright Chromium ✅
7. Configure environment variables ✅
8. Run `python run_auto_apply.py` ✅
9. Add cron job every 6 hours ✅
10. Run Streamlit on port 8501 ✅
11. Use tmux/screen to keep processes alive ✅
