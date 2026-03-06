# Resume PDF Text Extraction (Beginner Guide)

Great progress so far 🎉

This guide shows you how to extract text from `resume.pdf` using Python and `pdfplumber`.

---

## Step 1) Make sure your virtual environment is active

You should see `(venv)` in your terminal prompt.

If not, activate it:

- **Windows (Command Prompt)**
  ```bat
  venv\Scripts\activate
  ```
- **Windows (PowerShell)**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **Mac/Linux**
  ```bash
  source venv/bin/activate
  ```

---

## Step 2) Install `pdfplumber`

Run:

```bash
pip install pdfplumber
```

### Why
- `pdfplumber` is a Python library that can read text from PDF pages.

---

## Step 3) Update `requirements.txt` (recommended)

Run:

```bash
pip freeze > requirements.txt
```

### Why
- Saves exact package versions, so you can recreate the same environment later.

---

## Step 4) Create `resume_parser.py`

Create a file named `resume_parser.py` in your project folder and paste the script below:

```python
# Import Path to safely work with file paths like resume.pdf and output files.
from pathlib import Path

# Import pdfplumber to read text from PDF files.
import pdfplumber


# Create a main function to keep the script organized and beginner-friendly.
def main():
    # Define the input PDF path (expects resume.pdf in the current project folder).
    pdf_path = Path("resume.pdf")

    # Define the output text file path where extracted text will be saved.
    output_path = Path("resume_text.txt")

    # Check if resume.pdf exists before trying to open it.
    if not pdf_path.exists():
        # Print a clear error message for beginners.
        print(f"Error: '{pdf_path}' was not found in this folder.")
        # Tell the user exactly how to fix it.
        print("Please place resume.pdf in the project directory and run again.")
        # Stop the script because extraction cannot continue without the file.
        return

    # Create an empty list to store text extracted from each page.
    page_text_chunks = []

    # Open the PDF file using pdfplumber in a context manager.
    # The context manager closes the file automatically when done.
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through every page in the PDF.
        for page in pdf.pages:
            # Extract text from the current page.
            text = page.extract_text()

            # Add text only if readable text exists on that page.
            if text:
                page_text_chunks.append(text)

    # Combine all collected page text into one big string.
    full_text = "\n\n".join(page_text_chunks).strip()

    # Handle the case where no readable text was found in the PDF.
    if not full_text:
        print("Error: No readable text found in resume.pdf.")
        print("This can happen if the PDF is scanned as images.")
        print("Try an OCR tool first, then run this script again.")
        return

    # Print extracted text clearly in the terminal.
    print("\n===== EXTRACTED RESUME TEXT START =====\n")
    print(full_text)
    print("\n===== EXTRACTED RESUME TEXT END =====\n")

    # Save the extracted text to resume_text.txt.
    output_path.write_text(full_text, encoding="utf-8")

    # Print confirmation so the user knows where the file was saved.
    print(f"Success: extracted text saved to '{output_path}'.")


# Run main() only when this script is executed directly.
if __name__ == "__main__":
    # Start the text extraction workflow.
    main()
```

---

## Step 5) Run the script

From the terminal (inside your project folder, with `(venv)` active), run:

```bash
python resume_parser.py
```

---

## How PDF text extraction works (simple explanation)

- A PDF can contain actual text data, or just images of text.
- `pdfplumber` reads text objects from each PDF page.
- The script loops through all pages, extracts each page's text, then combines everything into one string.
- That final text is printed and also saved to `resume_text.txt`.

---

## If extraction fails, what should you do?

### 1) `resume.pdf` missing
- Put `resume.pdf` in the same folder as `resume_parser.py`.
- Run the script again.

### 2) No readable text found
- Your PDF might be scanned images.
- Use OCR (Optical Character Recognition) to convert images to real text first.
- Then rerun `python resume_parser.py`.

### 3) Module not found (`No module named pdfplumber`)
- Your venv may not be active, or package not installed in it.
- Activate venv and run:
  ```bash
  pip install pdfplumber
  ```
