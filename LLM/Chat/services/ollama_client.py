import subprocess
import json


def get_models():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            models = []
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:  # Skip header
                if line.strip():
                    model_name = line.split()[0]
                    if model_name and model_name != "NAME":
                        models.append(model_name)
            return models
    except:
        pass
    return []


def generate_text(model, prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None


def generate_text_stream(model, prompt, context=""):
    # Simplified version - just return regular response for now
    response = generate_text(model, prompt)
    if response:
        yield response