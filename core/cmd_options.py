#!/usr/bin/env python

from optparse import OptionParser, OptionGroup


def main():

    usage = """
        sudo bin/%prog <option> <arg>
        sudo bin/%prog <option> <arg1> <arg2>
        sudo bin/%prog <option> <arg> <option>
        sudo bin/%prog <option1> <arg> <option2> <arg>

    examples:
        sudo bin/%prog -u 1                                 # Check if 1GB of disk space is available in /opt
        sudo bin/%prog -i jre epel                          # Check if the package jre exists in epel yum repo
        sudo bin/%prog --app jira -p                        # Check application process status          
        sudo bin/%prog --app jira --file /tmp/jira.json -sb # Shutdown application and perform backup
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
                                   help="Backup directories and files. Must use with shutdown option.")
    config_file_options.add_option("-d", action="store_true",
                                   dest="download", help="Download deployment files")
    config_file_options.add_option("-k", action="store_true",
                                   dest="keep", help="Save directories and files prior to rollback")


    parser.add_option_group(config_file_options)

    return parser
