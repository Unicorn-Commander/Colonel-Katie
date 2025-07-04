import requests
from huggingface_hub import HfApi
import openai
import os

class ModelManager:
    def __init__(self):
        self.ollama_url = "http://localhost:11434" # Default Ollama URL
        self.hf_api = HfApi()
        
        # Only initialize OpenAI client if API key is available
        self.openai_client = None
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.openai_client = openai.OpenAI(api_key=api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")
        else:
            print("Info: ModelManager initialized without OpenAI API key - OpenAI models unavailable")

    def discover_ollama_models(self):
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            return [{"name": model["name"], "source": "ollama"} for model in models]
        except requests.exceptions.RequestException as e:
            print(f"Error discovering Ollama models: {e}")
            return []

    def discover_huggingface_models(self, limit=10):
        try:
            # This is a simplified discovery. In a real app, you'd filter/search more specifically.
            models = self.hf_api.list_models(limit=limit)
            return [{"name": model.modelId, "source": "huggingface"} for model in models]
        except Exception as e:
            print(f"Error discovering HuggingFace models: {e}")
            return []

    def discover_openai_models(self):
        if not self.openai_client:
            print("Info: OpenAI client not available - skipping OpenAI model discovery")
            return []
            
        try:
            models = self.openai_client.models.list()
            return [{"name": model.id, "source": "openai"} for model in models.data]
        except Exception as e:
            print(f"Error discovering OpenAI models: {e}")
            return []

    def list_all_models(self):
        all_models = []
        all_models.extend(self.discover_ollama_models())
        all_models.extend(self.discover_huggingface_models())
        all_models.extend(self.discover_openai_models())
        return all_models

    def tag_model(self, model_name, tags):
        # Placeholder for tagging models
        print(f"Tagging model {model_name} with {tags}")

    def categorize_model(self, model_name, category):
        # Placeholder for categorizing models
        print(f"Categorizing model {model_name} as {category}")

    def run_model_test(self, model_name, test_data):
        # Placeholder for running model tests
        print(f"Running test on {model_name} with data: {test_data}")
        return {"success": True, "results": "Simulated test results"}

    def get_model_performance_metrics(self, model_name):
        # Placeholder for getting performance metrics
        print(f"Getting performance metrics for {model_name}")
        return {"latency": "100ms", "accuracy": "90%"}

    def create_model_preset(self, preset_name, model_config):
        # Placeholder for creating model presets
        print(f"Creating preset {preset_name} with config: {model_config}")

    def apply_model_preset(self, preset_name):
        # Placeholder for applying model presets
        print(f"Applying preset {preset_name}")

    def create_agent_builder_interface(self):
        # Placeholder for visual agent builder
        print("Creating visual agent builder interface.")

    def load_prebuilt_agent_template(self, template_name):
        # Placeholder for loading pre-built templates
        print(f"Loading pre-built agent template: {template_name}")

    def manage_custom_instructions(self, agent_id, instructions):
        # Placeholder for custom instruction management
        print(f"Managing custom instructions for agent {agent_id}: {instructions}")

    def test_agent_capabilities(self, agent_id, test_data):
        # Placeholder for agent capability testing sandbox
        print(f"Testing capabilities for agent {agent_id} with data: {test_data}")
        return {"success": True, "results": "Simulated agent test results"}

    def share_agent_to_marketplace(self, agent_id):
        # Placeholder for agent marketplace/sharing system
        print(f"Sharing agent {agent_id} to marketplace.")
