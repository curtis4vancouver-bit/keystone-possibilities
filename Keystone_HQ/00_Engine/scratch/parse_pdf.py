import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to install pypdf if not present
install_and_import("pypdf")

import pypdf

def main():
    pdf_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\CURTIS_Resume_old.pdf"
    output_txt = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\CURTIS_Resume_old_text.txt"
    
    print(f"Parsing PDF: {pdf_path}")
    reader = pypdf.PdfReader(pdf_path)
    
    text_content = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        text_content.append(f"--- PAGE {i+1} ---")
        text_content.append(text)
        
    full_text = "\n".join(text_content)
    
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"Extracted text written to {output_txt}!")
    print("\nPreview of extracted text (first 1000 chars):")
    print(full_text[:1000])

if __name__ == "__main__":
    main()
