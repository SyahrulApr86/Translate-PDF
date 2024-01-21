import bot_translate
from merge import merge_pdf_pages
import os
from PyPDF2 import PdfReader, PdfWriter


def _split_pdf_by_page_count(file_path, max_pages=299):
    """Split PDF into parts based on the maximum number of pages."""
    reader = PdfReader(file_path)
    total_pages = len(reader.pages)

    if total_pages <= max_pages:
        print(f"No need to split file: {file_path}, the number of pages is less than or equal to {max_pages}.")
        return [file_path]

    print(f"Splitting file based on page count: {file_path}")
    split_files = []
    for i in range(0, total_pages, max_pages):
        writer = PdfWriter()
        end_page = min(i + max_pages, total_pages)

        for j in range(i, end_page):
            writer.add_page(reader.pages[j])

        split_file_path = f"{file_path}_part_{i // max_pages + 1}.pdf"
        with open(split_file_path, 'wb') as f:
            writer.write(f)

        split_files.append(split_file_path)

    print(f"File {file_path} split into {len(split_files)} parts based on the number of pages.")
    return split_files


def split_pdf_by_size(file_path, max_size_mb=9.5):
    """Further split PDF parts if they exceed the maximum file size."""
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
    if file_size <= max_size_mb:
        print(f"File {file_path} does not need to be split, its size is {file_size:.2f} MB.")
        return [file_path]

    print(f"Splitting file based on size: {file_path} (size: {file_size:.2f} MB)")
    reader = PdfReader(file_path)
    writer = PdfWriter()
    split_files = []
    base_name, _ = os.path.splitext(file_path)

    for i, page in enumerate(reader.pages):
        writer.add_page(page)

        temp_file_path = f"{base_name}_temp.pdf"
        with open(temp_file_path, 'wb') as f:
            writer.write(f)

        if (os.path.getsize(temp_file_path) / (1024 * 1024) > max_size_mb) or (i == len(reader.pages) - 1):
            final_file_path = f"{base_name}_part_{len(split_files) + 1}.pdf"
            os.rename(temp_file_path, final_file_path)
            split_files.append(final_file_path)
            writer = PdfWriter()

    delete_files([file_path])  # Delete the original file
    print(f"File {file_path} split into {len(split_files)} parts based on file size.")
    return split_files


def split_pdf_if_needed(file_path, max_pages=299, max_size_mb=9.5):
    """Coordinate the splitting of a PDF based on page count and file size."""
    initial_splits = _split_pdf_by_page_count(file_path, max_pages)
    all_splits = []

    for initial_split in initial_splits:
        file_size = os.path.getsize(initial_split) / (1024 * 1024)  # Convert to MB
        if file_size > max_size_mb:
            size_based_splits = split_pdf_by_size(initial_split, max_size_mb)
            all_splits.extend(size_based_splits)
        else:
            all_splits.append(initial_split)

    return all_splits


def combine_pdf_files(file_paths, output_file_path):
    pdf_writer = PdfWriter()

    for path in file_paths:
        pdf_reader = PdfReader(path)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(output_file_path, 'wb') as out:
        pdf_writer.write(out)


def rename_file(original_path, new_name):
    """Change the name of the file at the specified path."""
    dir_name = os.path.dirname(original_path)
    new_path = os.path.join(dir_name, new_name)
    os.rename(original_path, new_path)
    return new_path


def delete_files(file_paths):
    """Delete files at the specified paths."""
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error occurred while deleting file {path}: {e}")


def run_translation(file_path, driver):
    """Use the same driver instance for each file"""
    bot_translate.translate(file_path, driver)


def translate_file(file_path):
    download_path = bot_translate.create_download_directory(file_path)
    split_files = split_pdf_if_needed(file_path)
    print("Split files:", split_files)

    driver = bot_translate.initialize_undetected_chrome(download_dir=download_path)
    translated_files_path = ""

    base_name, ext = os.path.splitext(os.path.basename(file_path))
    output_file_name = f"{base_name}_en-id{ext}"
    output_merged_path = os.path.join(download_path, output_file_name)
    print("Output file path:", output_merged_path)

    if len(split_files) > 1:

        translated_files = []
        for split_file in split_files:
            translated_file = os.path.join(download_path, os.path.basename(split_file))
            try:
                run_translation(split_file, driver)
                translated_files.append(translated_file)
            except Exception as e:
                print(f"An error occurred while translating {split_file}: {e}")

        print("All files have been translated.")

        base_name, ext = os.path.splitext(os.path.basename(file_path))
        combined_file_name = f"{base_name}_Translated{ext}"
        combined_file_path = os.path.join(download_path, combined_file_name)
        translated_files_path = combined_file_path

        combine_pdf_files(translated_files, combined_file_path)
        print(f"All translated files have been combined into {combined_file_path}.")
        delete_files(split_files)
        delete_files(translated_files)
    else:
        try:
            run_translation(file_path, driver)
            print("File has been translated.")

            # Rename the translated file
            base_name, ext = os.path.splitext(os.path.basename(file_path))
            translated_file_name = f"{base_name}_Translated{ext}"
            translated_files_path = os.path.join(download_path, translated_file_name)

            rename_file(os.path.join(download_path, os.path.basename(file_path)), translated_file_name)
            print(f"Translated file saved as {translated_files_path}")

        except Exception as e:
            print(f"An error occurred while translating the file: {e}")

    # Merge the translated files with the original file
    merge_pdf_pages(file_path, translated_files_path, output_merged_path)

    driver.quit() # Close the browser


if __name__ == "__main__":
    file_path = r"test.pdf"
    translate_file(file_path)
