from functions.get_file_content import get_file_content

def test(working_dir: str, file: str):
    result = get_file_content(working_dir, file)
    print(f"{file} length: {len(result)}")
    print(f"{file} truncated: {'truncated' in result}")
    if "Error:" in result and len(result) < 100:
        print(result)

def main():
    test("calculator", "lorem.txt")
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
if __name__ == "__main__":
    main()