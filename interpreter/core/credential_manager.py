import keyring

class CredentialManager:
    SERVICE_ID = "ColonelKatieAPI"

    @staticmethod
    def set_api_key(service_name, api_key):
        try:
            keyring.set_password(CredentialManager.SERVICE_ID, service_name, api_key)
            print(f"API key for {service_name} stored securely.")
        except Exception as e:
            print(f"Error storing API key for {service_name}: {e}")

    @staticmethod
    def get_api_key(service_name):
        try:
            return keyring.get_password(CredentialManager.SERVICE_ID, service_name)
        except Exception as e:
            print(f"Error retrieving API key for {service_name}: {e}")
            return None

    @staticmethod
    def delete_api_key(service_name):
        try:
            keyring.delete_password(CredentialManager.SERVICE_ID, service_name)
            print(f"API key for {service_name} deleted securely.")
        except Exception as e:
            print(f"Error deleting API key for {service_name}: {e}")
