#!/usr/bin/env python

from optparse import OptionParser, OptionGroup


def main():

    usage = """
        sudo ./%prog <option>
        sudo ./%prog <command> <option>
        sudo ./%prog <command>  <sub-command> <option>


    examples:
        sudo ./%prog -u 1                                 # Check if 1GB of disk space is available in /opt
        sudo ./%prog --app jira -p                        # Check application process status          
        sudo ./%prog --app jira --file /tmp/jira.json -bs # Shutdown application and perform backup

        """

    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--space-required", dest="disk_space", type=float,
                      help="Check for free disk space. Specify in GBs. i.e: 1 for 1GB")
    parser.add_option("-i", "--package-info",
                      dest="package_name", help="Specify rpm package name with REPO_NAME as an argument")

    app_options = OptionGroup(parser, 'Application operations',
                              'Format: sudo ./run --app <name> <option>')
    app_options.add_option("-a", "--app", dest="app", type='choice', choices=['jira', 'bitbucket', 'bamboo', 'crowd'],
                           help="Specify app name")
    app_options.add_option("-s", "--shut-down", action="store_true",
                           dest="shutdown", help="Shutdown application")
    app_options.add_option("-p", "--status", action="store_true", dest="process",
                           help="Check application process status")
    parser.add_option_group(app_options)

    config_file_options = OptionGroup(
        parser, 'Configuration file operations', 'Format: sudo ./run --app <name> --file <path> <option>')
    config_file_options.add_option("-f", "--file", dest="file",
                                   help="Specify config file path")
    config_file_options.add_option("-b", action="store_true", dest="backup",
                                   help="Backup application. Must use with shutdown option.")
    config_file_options.add_option("-d", action="store_true",
                                   dest="download", help="Download deployment files")

    parser.add_option_group(config_file_options)

    return parser
