"""
Set the system configuration.
"""

import yaml

class SystemConfig:
    """
    Class Docstring: Describe the purpose of this class here.
    """
    with open('system_config.yaml', 'r', encoding='utf-8') as file:
        system_config = yaml.safe_load(file)

    DEFAULT_VERSION = system_config.get('default_version', 'v1')
    REQUIRED_CHATBOT_FIELDS = system_config.get('required_chatbot_fields', {})
    REQUIRED_DB_FIELDS = system_config.get('required_db_fields', {})

    @classmethod
    def get_default_version(cls):
        """
        Get the default version.
        """
        return cls.DEFAULT_VERSION

    @classmethod
    def get_required_chatbot_fields(cls):
        """
        Get the required chatbot fields.
        """
        return cls.REQUIRED_CHATBOT_FIELDS

    @classmethod
    def get_required_db_fields(cls):
        """
        Get the required database fields.
        """
        return cls.REQUIRED_DB_FIELDS


if __name__ == '__main__':
    pass