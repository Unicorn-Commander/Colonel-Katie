import json
import uuid
from .conversation_manager import ConversationManager
from .rag_config import RAGConfig

class ChatManager:
    def __init__(self, model_manager, interpreter_instance, tts_service, stt_service, rag_manager, config_manager):
        self.model_manager = model_manager
        self.current_model = None
        self.interpreter = interpreter_instance
        self.tts_service = tts_service
        self.stt_service = stt_service
        self.rag_manager = rag_manager
        self.conversation_manager = ConversationManager()
        self.config_manager = config_manager

    def set_current_model(self, model_name):
        # In a real implementation, you'd validate model_name against available models
        # and potentially load/initialize the model.
        available_models = self.model_manager.list_all_models()
        found_model = next((m for m in available_models if m['name'] == model_name), None)
        if found_model:
            self.current_model = found_model
            self.interpreter.llm.model = found_model['name'] # Update interpreter's LLM model
            print(f"Current model set to: {self.current_model['name']} ({self.current_model['source']})")
            return True
        else:
            print(f"Model '{model_name}' not found.")
            return False

    def get_current_model(self):
        return self.current_model

    def new_conversation(self):
        return self.conversation_manager.new_conversation(self.config_manager.get("chat.default_settings", {}))

    def add_message(self, role, content):
        self.conversation_manager.add_message(role, content)

    def get_current_conversation(self):
        return self.conversation_manager.get_current_conversation()

    def export_conversation_json(self, conversation_id, file_path):
        return self.conversation_manager.export_conversation_json(conversation_id, file_path)

    def import_conversation_json(self, file_path):
        return self.conversation_manager.import_conversation_json(file_path)

    def save_chat_settings(self, conversation_id, settings):
        return self.conversation_manager.save_chat_settings(conversation_id, settings)

    def load_chat_settings(self, conversation_id):
        return self.conversation_manager.load_chat_settings(conversation_id)

    def set_default_chat_settings(self, settings):
        self.config_manager.set("chat.default_settings", settings)
        print("Default chat settings updated.")

    def get_default_chat_settings(self):
        return self.config_manager.get("chat.default_settings", {})

    def update_chat_settings(self, settings):
        current_conversation = self.conversation_manager.get_current_conversation()
        if current_conversation:
            self.conversation_manager.save_chat_settings(current_conversation["id"], settings)
            # Apply TTS settings immediately
            if "tts_enabled" in settings:
                self.tts_service.tts_enabled = settings["tts_enabled"]
            if "speech_speed" in settings:
                self.tts_service.engine.setProperty('rate', int(self.tts_service.engine.getProperty('rate') * settings["speech_speed"])) # Apply speed
            if "speech_pitch" in settings:
                # pyttsx3 doesn't have direct pitch control, but we can simulate it or use ElevenLabs
                pass # Placeholder for pitch
            if "wake_word_enabled" in settings:
                if settings["wake_word_enabled"]:
                    self.stt_service.start_wake_word_detection()
                else:
                    self.stt_service.stop_wake_word_detection()
            if "rag_config" in settings:
                rag_config_dict = settings["rag_config"]
                rag_config = RAGConfig.from_dict(rag_config_dict)
                self.rag_manager.set_chunking_strategy(rag_config.chunking_strategy, rag_config.chunk_size, rag_config.chunk_overlap)
                self.rag_manager.set_embedding_model(rag_config.embedding_model_name)
                self.rag_manager.set_vector_database(rag_config.vector_database_type)
                self.rag_manager.set_retrieval_parameters(rag_config.retrieval_top_k, rag_config.retrieval_similarity_threshold)
            print(f"Updated settings for conversation {current_conversation["id"]}: {settings}")

    def get_chat_settings(self):
        current_conversation = self.conversation_manager.get_current_conversation()
        if current_conversation:
            return self.conversation_manager.load_chat_settings(current_conversation["id"])
        return self.get_default_chat_settings()

    def execute_code(self, code):
        # This is a placeholder. Actual integration with OpenInterpreter's
        # execution loop will be more complex.
        print(f"Executing code: {code}")
        # In a real scenario, you'd pass this to the interpreter instance
        # and handle its output.
        # For example: self.interpreter.chat(code)
        return "Code execution simulated."

    def tag_conversation(self, conversation_id, tags):
        self.conversation_manager.tag_conversation(conversation_id, tags)

    def categorize_conversation(self, conversation_id, category):
        self.conversation_manager.categorize_conversation(conversation_id, category)

    def search_conversations(self, query):
        return self.conversation_manager.search_conversations(query)

    def filter_conversations(self, filters):
        return self.conversation_manager.filter_conversations(filters)

    def create_chat_template(self, template_name, messages):
        self.conversation_manager.create_chat_template(template_name, messages)

    def apply_chat_template(self, template_name):
        self.conversation_manager.apply_chat_template(template_name)

    def edit_message(self, conversation_id, message_index, new_content):
        self.conversation_manager.edit_message(conversation_id, message_index, new_content)

    def regenerate_message(self, conversation_id, message_index):
        self.conversation_manager.regenerate_message(conversation_id, message_index)

    def get_conversation_analytics(self):
        return self.conversation_manager.get_conversation_analytics()

    def enable_multi_user_support(self):
        # Placeholder for multi-user support
        print("Enabling multi-user support.")

    def create_shared_conversation_space(self, space_name):
        # Placeholder for shared conversation spaces
        print(f"Creating shared conversation space: {space_name}")

    def show_realtime_collaboration_indicators(self):
        # Placeholder for real-time collaboration indicators
        print("Showing real-time collaboration indicators.")

    def manage_permission_system(self, user_id, permissions):
        # Placeholder for permission management system
        print(f"Managing permissions for user {user_id}: {permissions}")

    def create_team_workspace(self, workspace_name):
        # Placeholder for team workspaces
        print(f"Creating team workspace: {workspace_name}")

    def get_activity_feeds_and_notifications(self, user_id):
        # Placeholder for activity feeds and notifications
        print(f"Getting activity feeds and notifications for user {user_id}.")
        return []
