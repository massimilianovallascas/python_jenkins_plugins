import unittest

from jenkins.plugin import *


class TestJenkinsPlugin(unittest.TestCase):

    def setUp(self) -> None:
        self.jenkins_version = "1.625.3"
        self.plugin = 'active-directory'
        self.plugin_api_response = {'active-directory':'Plugin("active-directory","https://updates.jenkins.io/download/plugins/active-directory/","2.26","2.12")'}
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_plugin(self) -> None:
        plugin = Plugin(self.plugin, self.jenkins_version)
        self.assertEqual(f"{plugin}", self.plugin_api_response[self.plugin])


if __name__ == '__main__':
    unittest.main()