import unittest

from jenkins.plugin import *
from main import *

class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins_version = "1.625.3"
        self.plugin_api_response = {'active-directory':'Plugin("active-directory","https://updates.jenkins.io/download/plugins/active-directory/","2.26","2.12")'}
        self.plugin_list = ['active-directory']
        self.source_file = "test/files/plugins_list.csv"
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_plugin_from_file(self) -> None:
        plugin_list = get_plugins_from_file(self.source_file)
        self.assertEqual(len(plugin_list), 164)

    def test_process_plugins(self) -> None:
        plugins_data = process_plugins(self.plugin_list, self.jenkins_version)
        self.assertEqual(f"{plugins_data[self.plugin_list[0]]}", self.plugin_api_response[self.plugin_list[0]])
 

if __name__ == '__main__':
    unittest.main()