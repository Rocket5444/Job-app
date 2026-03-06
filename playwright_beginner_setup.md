# Playwright Setup Guide (After Virtual Environment Is Activated)

Great job activating your virtual environment 🎉

This guide starts from that point and walks you through installing Playwright, installing Chromium, saving dependencies, and running a first browser test script.

---

## Before you start (quick check)

Make sure your terminal prompt shows `(venv)`.

Example:

```bash
(venv) your-name@computer:~/job_automation_bot$
```

If you do **not** see `(venv)`, activate it first:

- **Windows (Command Prompt):** `venv\Scripts\activate`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Mac/Linux:** `source venv/bin/activate`

---

## Step 1) Install Playwright using pip

Run this command:

```bash
pip install playwright
```

### What this does
- `pip` is Python's package installer.
- This command downloads and installs the Playwright Python library inside your active `venv`.

---

## Step 2) Install Playwright Chromium browser

Playwright needs browser binaries to control a real browser.

Run:

```bash
playwright install chromium
```

If the `playwright` command is not found, use:

```bash
python -m playwright install chromium
```

### What this does
- Downloads only the Chromium browser package required by Playwright.
- Keeps your setup lightweight (only what you need).

---

## Step 3) Update `requirements.txt` correctly

Now save installed packages so the project can be recreated later.

Run:

```bash
pip freeze > requirements.txt
```

### What this does
- Writes all currently installed Python packages from your virtual environment into `requirements.txt`.
- This helps others (or future you) install the same dependencies quickly.

---

## Step 4) Verify Playwright is installed properly

Run these checks:

```bash
pip show playwright
python -c "import playwright; print('Playwright import successful')"
```

### What to expect
- `pip show playwright` should display package details (name, version, location).
- The second command should print:
  `Playwright import successful`

---

## Step 5) Create `test_browser.py`

Create a file named `test_browser.py` in your project folder and paste this code:

```python
# Import Playwright's sync API so we can write simple step-by-step Python code.
from playwright.sync_api import sync_playwright

# Create a main function so our script has a clear entry point.
def main():
    # Start Playwright inside a context manager.
    # This automatically sets up resources and cleans them up safely.
    with sync_playwright() as p:
        # Launch Chromium browser in visible mode (headless=False).
        # headless=False means you will see the browser window open.
        browser = p.chromium.launch(headless=False)

        # Open a new browser tab (called a page in Playwright).
        page = browser.new_page()

        # Navigate to the target website.
        page.goto("https://example.com")

        # Wait for 5 seconds (5000 milliseconds) so you can see the page.
        page.wait_for_timeout(5000)

        # Close the browser when done.
        browser.close()


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
```

---

## Step 6) Why the script works (beginner explanation)

- `from playwright.sync_api import sync_playwright` imports the Playwright tools.
- `with sync_playwright() as p:` starts Playwright safely.
- `p.chromium.launch(headless=False)` opens a visible Chromium browser.
- `browser.new_page()` creates a browser tab.
- `page.goto("https://example.com")` opens the website.
- `page.wait_for_timeout(5000)` pauses for 5 seconds.
- `browser.close()` closes the browser.
- The `if __name__ == "__main__":` block runs your script when you execute the file.

---

## Step 7) Run the script

From the same folder (with `(venv)` active), run:

```bash
python test_browser.py
```

### Expected result
1. A Chromium window opens.
2. It loads `https://example.com`.
3. It stays open for about 5 seconds.
4. It closes automatically.

---

## Troubleshooting (common beginner issues)

### Error: `ModuleNotFoundError: No module named 'playwright'`
- Your virtual environment is likely not active.
- Activate `venv` and run `pip install playwright` again.

### Error: Browser executable doesn't exist
- Chromium binaries were not installed yet.
- Run `python -m playwright install chromium`.

### Script closes too fast
- Increase timeout value, for example:
  `page.wait_for_timeout(10000)` for 10 seconds.
