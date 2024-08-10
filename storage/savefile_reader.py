import subprocess
import json

class SaveEditor:
    def __init__(self, jar_path):
        self.jar_path = jar_path

    def _run_command(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Error output: {e.stderr}")
            return None

    def decode_save(self, save_file, output_file):
        command = ["java", "-jar", self.jar_path, "decode", "-o", output_file]
        
        command.append(save_file)
        
        self._run_command(command)