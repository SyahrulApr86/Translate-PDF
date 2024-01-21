import run_translation


def main():
    file_paths = [
        r"D:\OneDrive - UNIVERSITAS INDONESIA\Documents\KULIAH\Book\Introduction to information retrieval 2009.pdf",
        r"D:\OneDrive - UNIVERSITAS INDONESIA\Documents\KULIAH\Book\Recommender Systems The Textbook.pdf",
        # add more files here
    ]

    for file_path in file_paths:
        try:
            run_translation.translate_file(file_path)
        except Exception as e:
            print(f"An error occurred while translating {file_path}: {e}")


if __name__ == "__main__":
    main()