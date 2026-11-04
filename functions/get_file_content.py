import os

MAX_CHARACTERS_TO_READ = 10000


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads up to 10000 characters of a specified relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to target file, relative to the working directory.",
                },
            },
        },
    },
}
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        content: str = ""
        working_dir_abs = os.path.abspath(working_directory)
        combined_path = os.path.join(working_dir_abs, file_path)
        target_file = os.path.normpath(combined_path)
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        if os.path.isfile(target_file) == False:
            return f"Error: File not found or is not a regular file: \"{file_path}\""

        with open(target_file, "r") as fstream:
            content += fstream.read(MAX_CHARACTERS_TO_READ)
            if fstream.read(1):
                content += f"[...File \"{file_path}\" truncated at {MAX_CHARACTERS_TO_READ} characters]"
        return content
    except Exception as e:
        return f"Error: {e}"

    
