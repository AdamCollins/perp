import configparser
import os
import logging


class Config:

    CONFIG_FILE_LOCATION = "/etc/perp/configuration.ini"

    def __init__(self):
        self.config = configparser.ConfigParser()
        files_read = self.config.read(self.CONFIG_FILE_LOCATION)
        if self.CONFIG_FILE_LOCATION not in files_read:
            logging.warning(
                f"No configuration file found at {self.CONFIG_FILE_LOCATION}"
            )

    def get_config_option(self, section, option):
        """Get the configuration option from the given section.

        If an environment variable exists with the format
        PREP_{SECTION}_{OPTION}, it will override the value in the
        configuration file.

        :param section: The string name of the section to read
        :param option: The string name of the option to read
        :return: The config value
        """
        env_override_option = f"PERP_{section.upper()}_{option.upper()}"

        value = self.config.get(section, option, fallback=None)
        value = os.getenv(env_override_option) or value

        return value