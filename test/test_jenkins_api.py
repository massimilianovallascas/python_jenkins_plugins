from genericpath import isfile
import os
import unittest

from jenkins.jenkins_api import *


class TestJenkinsJenkinsAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.file_path = "test/files/plugins_list_test.csv"
        self.password = "password"
        self.host = "localhost"
        self.plugin_list = {"plugins": [{"shortName":"ace-editor"}, {"shortName":"active-directory"}, {"shortName":"ansicolor"}, {"shortName":"ant"},] }
        self.port = 8080
        self.jenkins_repr = 'JenkinsAPI("localhost","8080","root","********")'
        self.user = "root"
        return super().setUp()

    def tearDown(self) -> None:
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        return super().tearDown()

    def test_init(self) -> None:
        jenkins_api = JenkinsAPI(self.file_path, self.host, self.port, self.user, self.password)
        self.assertEqual(f"{jenkins_api}", self.jenkins_repr)

    def test_create_file(self) -> None:
        jenkins_api = JenkinsAPI(self.file_path, self.host, self.port, self.user, self.password)
        jenkins_api._create_file(self.plugin_list)
        f = open(self.file_path, "r")
        self.assertEqual(len(f.readlines()), len(self.plugin_list["plugins"]))
        f.close()


if __name__ == '__main__':
    unittest.main()