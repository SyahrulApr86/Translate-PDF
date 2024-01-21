import fitz  # PyMuPDF
import os
def merge_pdf_pages(pdf_path1, pdf_path2, output_path):
    """Merge two PDF files into one, side by side."""
    print(f"Merging {pdf_path1} and {pdf_path2} into {output_path}...")
    doc1 = fitz.open(pdf_path1)
    doc2 = fitz.open(pdf_path2)

    # create a blank new document
    new_doc = fitz.open()

    # ensure that both documents have the same number of pages
    if len(doc1) != len(doc2):
        file_name1 = os.path.basename(pdf_path1)
        file_name2 = os.path.basename(pdf_path2)
        print(f"Jumlah halaman {file_name1} ({len(doc1)}) tidak sama dengan jumlah halaman {file_name2} ({len(doc2)})")
        raise ValueError("Dokumen harus memiliki jumlah halaman yang sama")

    # loop through the pages
    for page_num in range(len(doc1)):
        # load the page
        page1 = doc1.load_page(page_num)
        page2 = doc2.load_page(page_num)

        # get the size of this page
        rect1 = page1.rect
        rect2 = page2.rect

        # create a new blank page big enough to fit both pages side by side
        new_page = new_doc.new_page(width=rect1.width + rect2.width, height=max(rect1.height, rect2.height))

        # Render the pages onto the new page
        new_page.show_pdf_page(page1.rect, doc1, page_num)
        new_page.show_pdf_page(fitz.Rect(rect1.width, 0, rect1.width + rect2.width, rect2.height), doc2, page_num)

    # save the newly created document
    new_doc.save(output_path)
    print(f"File {output_path} created successfully.")
    new_doc.close()
    doc1.close()
    doc2.close()
