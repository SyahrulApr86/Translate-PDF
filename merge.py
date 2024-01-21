import fitz  # PyMuPDF
import os
def merge_pdf_pages(pdf_path1, pdf_path2, output_path):
    # Membuka kedua dokumen PDF
    doc1 = fitz.open(pdf_path1)
    doc2 = fitz.open(pdf_path2)

    # Membuat dokumen PDF baru untuk output
    new_doc = fitz.open()

    # Pastikan kedua dokumen memiliki jumlah halaman yang sama
    if len(doc1) != len(doc2):
        file_name1 = os.path.basename(pdf_path1)
        file_name2 = os.path.basename(pdf_path2)
        print(f"Jumlah halaman {file_name1} ({len(doc1)}) tidak sama dengan jumlah halaman {file_name2} ({len(doc2)})")
        raise ValueError("Dokumen harus memiliki jumlah halaman yang sama")

    # Menggabungkan halaman
    for page_num in range(len(doc1)):
        # Load halaman dari kedua dokumen
        page1 = doc1.load_page(page_num)
        page2 = doc2.load_page(page_num)

        # Dapatkan ukuran halaman
        rect1 = page1.rect
        rect2 = page2.rect

        # Buat halaman baru dengan lebar gabungan dan tinggi maksimum
        new_page = new_doc.new_page(width=rect1.width + rect2.width, height=max(rect1.height, rect2.height))

        # Render halaman asli ke halaman baru
        new_page.show_pdf_page(page1.rect, doc1, page_num)
        new_page.show_pdf_page(fitz.Rect(rect1.width, 0, rect1.width + rect2.width, rect2.height), doc2, page_num)

    # Simpan dokumen baru
    new_doc.save(output_path)
    new_doc.close()
    doc1.close()
    doc2.close()
