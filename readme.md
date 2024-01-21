
# PDF Translation Automation Tool

## Description
This automation tool is designed for translating large or lengthy PDF documents from English to Indonesian using Google Translate. It automatically splits large PDF documents into smaller sections if necessary, to meet the size and page limitations of Google Translate, and then recombines them after translation.

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
1. Set the path to the PDF file you want to translate in the `main` function of the script.
2. Run the script from the terminal or a Python IDE:
   ```bash
   python script_name.py
   ```
3. The translated file will be saved in the same directory as the original document.

## Code Structure
- `split_pdf_if_needed`: Splits the PDF document based on page count and file size.
- `combine_pdf_files`: Merges the translated PDF files.
- `run_translation`: Manages the translation process for each file using Selenium and Google Translate.
- `main`: The main function to orchestrate the splitting, translation, and merging processes.

## Notes
- Ensure you have a stable internet connection when running the script.
- This script uses Google Translate, which may have usage limitations.
