import json


class UserConfigurations:
    def __init__(self,path_to_configuration_file):
        self.path_to_configuration_file = path_to_configuration_file
        self.configuration = UserConfigurations.open_configuration_source(self)

    def open_configuration_source(self):
        configuration = json.load(self.path_to_configuration_file)
        return configuration

    def email_configuration(self):
        email_configuration = self.configuration['email']
        return email_configuration

    def instagram_login_configuration(self):
        instagram_login_configuration = self.configuration['credentials']
        return instagram_login_configuration
