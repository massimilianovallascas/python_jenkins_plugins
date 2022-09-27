import requests

from bs4 import BeautifulSoup
from packaging import version


class Plugin:

    def __init__(self, name, jenkins_version) -> None:
        self.base_url = "https://updates.jenkins.io/download/plugins"
        self.jenkins_version = jenkins_version
        self.name = name
        self.url = f"{self.base_url}/{self.name}/"
        self.latest_compatible_version = None
        self.latest_version = None

        self.history = self._get_plugin_history()
        self._get_versions_data()

    def _get_plugin_history(self) -> list:
        history = []

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        artifacts = soup.find('ul', attrs={"class":"artifact-list"})
        for li_tag in artifacts.findAll('li'):
            for div in li_tag.findAll('div', {"class":"core-dependency"}):
                history.append((li_tag.get('id'), div.text.split(' ')[-1]))

        return history

    def _get_versions_data(self) -> None:
        self.latest_version = self.history[0][0]
        for plugin_version in self.history:
            if version.parse(self.jenkins_version) >= version.parse(plugin_version[1]):
                self.latest_compatible_version = plugin_version[0]
                break

    def __repr__(self) -> str:
        return f'Plugin("{self.name}","{self.url}","{self.latest_version}","{self.latest_compatible_version}")'