import os
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        combined_path = os.path.join(working_dir_abs, file_path)
        target_file = os.path.normpath(combined_path)
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        completed_process = subprocess.run(command, text = True, timeout = 30, capture_output = True)
        output_str = ""
        if completed_process.returncode != 0:
            output_str += f"Process exited with code {completed_process.returncode}\n"
        if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
            output_str += "No output produced\n"
        else:
            output_str += f"STDOUT: {completed_process.stdout}\n"
            output_str += f"STDERR: {completed_process.stderr}\n"
        return output_str
    except Exception as e:
        return f"Error: executing python file: {e}"
