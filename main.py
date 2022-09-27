import argparse
import getpass
import sys

from alive_progress import alive_bar
from jenkins.jenkins_api import JenkinsAPI
from jenkins.plugin import Plugin


def parse() -> list:

    class Password(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            if values is None:
                values = getpass.getpass()

            setattr(namespace, self.dest, values)

    parser = argparse.ArgumentParser(description='Get Jenkins plugin latest compatible version.')

    parser.add_argument("-d", "--download", action="store_true", required=False, help="Download plugins list from Jenkins API")
    parser.add_argument("-df", "--destination-file", default="plugins_compatibility.csv", required=False, help="Source file")
    parser.add_argument("-jh", "--jenkins-host", required="-d" in sys.argv or "--download" in sys.argv, type=str, help="Jenkins host")
    parser.add_argument("-jp", "--jenkins-port", default=8080, required=False, type=int, help="Jenkins port")
    # parser.add_argument("-jpwd", "--jenkins-password", required="-d" in sys.argv or "--download" in sys.argv, type=str, help="Jenkins password")
    parser.add_argument("-jpwd", "--jenkins-password", action=Password, dest="jenkins_password", nargs="?", required="-d" in sys.argv or "--download" in sys.argv, help="Enter your password")
    parser.add_argument("-jusr", "--jenkins-user", required="--download" in sys.argv, type=str, help="Jenkins user")
    parser.add_argument("-jv", "--jenkins-version", type=str, required=True, help="Current Jenkins version")
    parser.add_argument("-sf", "--source-file", default="plugins_list.csv", required=False, help="Source file")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    args = parser.parse_args()
    
    return args.download, args.destination_file, args.jenkins_host, args.jenkins_port, args.jenkins_password, args.jenkins_user, args.jenkins_version, args.source_file


def get_plugins_from_file(file_path) -> list:
    plugins_list = []
    data_separator = ";"
    f = open(file_path, "r")
    for line in f:
        if "Plugin" not in line:
            plugins_list.append(line.strip().split(data_separator)[0])
    f.close()

    return plugins_list


def process_plugins(plugins_list, jenkins_version) -> dict:
    plugins_data = {}
    with alive_bar(len(plugins_list), dual_line=True, title="API requests") as bar:
        for plugin_name in plugins_list:
            bar.text = f"Processing {plugin_name}"
            plugins_data[plugin_name] = Plugin(plugin_name, jenkins_version)
            bar()

    return plugins_data


def write_file(destination_file, plugins_data, jenkins_version) -> None:
    f = open(destination_file, "w")
    for _, plugin_object in plugins_data.items():
        if plugin_object.latest_compatible_version:
            f.write(f"{plugin_object.name},{plugin_object.latest_compatible_version}\n")
        else:
            print(f"Plugin '{plugin_object.name}' is not compatible with Jenkins version {jenkins_version}")
    f.close


def main() -> bool:
    download, destination_file, jenkins_host, jenkins_port, jenkins_password, jenkins_user, jenkins_version, source_file = parse()
    
    if download:
        jenkins_api = JenkinsAPI(source_file, jenkins_host, jenkins_port, jenkins_user, jenkins_password)
        jenkins_api.get_plugins()

    plugins_list = get_plugins_from_file(source_file)
    plugins_data = process_plugins(plugins_list, jenkins_version)
    write_file(destination_file, plugins_data, jenkins_version)
    
    return True


if __name__ == "__main__":
    main()