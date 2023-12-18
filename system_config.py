import yaml

class SystemConfig:
    with open('system_config.yaml', 'r') as file:
        systemn_config = yaml.safe_load(file)

    DEFAULT_VERSION = systemn_config.get('default_version', 'v1')
    REQUIRED_CHATBOT_FIELDS = systemn_config.get('required_chatbot_fields', {})
    REQUIRED_DB_FIELDS = systemn_config.get('required_db_fields', {})
    
    @classmethod
    def get_default_version(cls):
        return cls.DEFAULT_VERSION

    @classmethod
    def get_required_chatbot_fields(cls):
        return cls.REQUIRED_CHATBOT_FIELDS

    @classmethod
    def get_required_db_fields(cls):
        return cls.REQUIRED_DB_FIELDS