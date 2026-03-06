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
