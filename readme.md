# PDF Translation Automation Tool

## Description
This automation tool is designed for translating large or lengthy PDF documents from English to Indonesian using Google Translate. It automatically splits large PDF documents into smaller sections if necessary to meet the size and page limitations of Google Translate and then recombines them after translation.

## Features
- Splits PDF documents based on page count and file size constraints.
- Automates the translation process using Google Translate.
- Merges translated PDF parts into a single document.

## System Requirements
- Python 3.6 or higher.
- Selenium WebDriver.
- PyPDF2.
- undetected_chromedriver.

## Installation
Before running the script, ensure all dependencies are installed. Install them using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage
1. Add the paths to the PDF files you want to translate in the `main.py` file.
2. Run the `main.py` script from the terminal or a Python IDE:
   ```bash
   python main.py
   ```
3. The translated files will be saved in the same directory as the original documents.

## Code Structure
- `split_pdf_if_needed`: Splits the PDF document based on page count and file size.
- `combine_pdf_files`: Merges the translated PDF files.
- `run_translation`: Manages the translation process for each file using Selenium and Google Translate.
- `translate_file`: Orchestrates the process for a single file, including splitting, translating, and merging.
- `main.py`: The main script to process multiple PDF files.

## Notes
- Ensure you have a stable internet connection when running the script.
- This script uses Google Translate, which may have usage limitations.
usage.