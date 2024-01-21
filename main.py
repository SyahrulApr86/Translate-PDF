import run_translation


def main():
    file_paths = [
        r"tes"
        # add more files here
    ]

    for file_path in file_paths:
        try:
            run_translation.translate_file(file_path)
        except Exception as e:
            print(f"An error occurred while translating {file_path}: {e}")


if __name__ == "__main__":
    main()