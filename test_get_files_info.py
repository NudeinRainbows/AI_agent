from functions.get_files_info import get_files_info


def main():
    print(f"Result for current directory")
    print(get_files_info("calculator", "."))

    print(f"Result for '/bin' directory")
    print(get_files_info("calculator", "/bin"))

    print(f"Result for '../' directory")
    print(get_files_info("calculator", "../"))

    print(f"Result for 'pkg' directory")
    print(get_files_info("calculator", "pkg"))

if __name__ == "__main__":
    main()
