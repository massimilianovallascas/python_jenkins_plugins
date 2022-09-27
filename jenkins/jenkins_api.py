import json
import requests


class JenkinsAPI:

    def __init__(self, file_path, host, port, user, password) -> None:
        self.file_path = file_path
        self.host = host
        self.password = password
        self.port = port
        self.user = user
        self.url = f"http://{self.user}:{self.password}@{self.host}:{self.port}/pluginManager/api/json?depth=1&xpath=/*/*/shortName|/*/*/version&wrapper=plugins"

    def get_plugins(self) -> None:
        response = requests.get(self.url).text
        plugins_list = json.loads(response)
        self._create_file(plugins_list)
    
    def _create_file(self, plugins_list) -> None:
        f = open(self.file_path, "w")
        for plugin in plugins_list["plugins"]:
            f.write(f"{plugin['shortName']}\n")
        f.close()

    def __repr__(self) -> str:
        return f'JenkinsAPI("{self.host}","{self.port}","{self.user}","********")'