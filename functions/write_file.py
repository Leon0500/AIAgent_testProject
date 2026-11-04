import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a specified target file relative to the working directory (default is working directory). If the file doesnt exist it is created.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to target file, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "content written to target file",
                },
            },
        },
    },
}
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        combined_path = os.path.join(working_dir_abs, file_path)
        target_file = os.path.normpath(combined_path)
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        if os.path.isdir(target_file):
            return f"Error: Cannot write to \"{file_path}\" as it is a directory"
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)
        with open(target_file, "w") as fstream:
            fstream.write(content)
        return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as e:
        return f"Error: {e}"