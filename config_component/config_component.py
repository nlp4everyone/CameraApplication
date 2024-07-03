import configparser, os
# Define object
config = configparser.ConfigParser()
default_config_file = "config.ini"

class ConfigManagement():
    @staticmethod
    def load_configs(path :str = default_config_file) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File name: {path} is not existed!")

        # Read file
        config.read(path)
        # Get all section
        sections = config.sections()
        # Empty section
        if len(sections) == 0:
            return {}

        result = {}
        # For section
        for section in sections:
            section_config = ConfigManagement.get_sections_config(section, path = default_config_file)
            result.update(section_config)
        return result

    @staticmethod
    def get_sections_config(session_name: str,path :str = default_config_file) -> dict:
        # Validate
        if not os.path.exists(path):
            raise FileNotFoundError(f"File name: {path} is not existed!")
        assert session_name, "Session name must be string"

        # Read file
        config.read(path)
        if not config.has_section(section = session_name):
            return {}

        # Get option inside session
        options = config.options(section = session_name)
        if len(options) == 0:
            return {}
        # Get option config
        session_config = {str(option):config.get(session_name,option) for option in options}
        # Return in right format
        return {session_name:session_config}

    @staticmethod
    def set_config(section :str,
                      option: str,
                      value :str,
                      path :str = default_config_file) -> None:
        # If there is no section
        if not config.has_section(section): config.add_section(section = section)

        # Set value
        config.set(section = section, option = option,value = value)
        # Add value
        with open(path, "w") as configfile:
            config.write(configfile)
