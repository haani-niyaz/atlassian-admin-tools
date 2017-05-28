# atlassian-admin-tools

#### Table of Contents

1. [Description](#description)
2. [Setup - The basics of getting started with [atlassian-admin-tools]](#setup)
    * [What [atlassian-admin-tools] affects](#what-atlassian-admin-tools-affects)
    * [Setup requirements](#setup-requirements)
    * [Beginning with [atlassian-admin-tools]](#beginning-with-atlassian-admin-tools)
3. [Usage - Configuration options and additional functionality](#usage)
4. [Reference](#reference)
5. [Limitations](#limitations)


## Description

Utility program to execute deployment pre-checks and pre-implementation steps.      

### Capabilities:

- Check application process status
- Check if disk space required is sufficient
- Verfiy if a rpm package exists in the repo
- Executes commands as the application user & privileges user (where necessary)
- Shutdown application
- Backup files (as specified in the config file)
- Download deployment files (as specified in the config file)
- Logging to stdout and writes to a log file

## Setup

### What [atlassian-admin-tools] affects 

The application runs in three modes:

#### Program options

Program can be used independently to do the following:
- Verify if required disk space is available
- Check if a RPM package is available in the specified repo

#### App options

Requires specifying application name. With these options you can:

- Shutdown application
- Check application process status

#### Configuration file options

The program reads a json config file which specifies:

- Backup directory
- Files to backup
- Directories to backup
- Files to download for deployment

A sample configuration has been provided in `sample/jira.json`

### Setup Requirements 

#### Validate JSON

The configuration file needs to completed and validated. Use the `validate_json.py` script to validate the file.

`./validate_json.py < /tmp/jira.json`

### Sudo access

You will require `sudo` access to run program.


### Beginning with [atlassian-admin-tools]	

The program accepts an `app` and `file` as input with optional arguments.

## Usage


```
[atlassian-admin-tools]$ sudo bin/run.by
usage: 
    sudo bin/run.py <option>
    sudo bin/run.py <command> <option>
    sudo bin/run.py <command>  <sub-command> <option>


examples:
    sudo bin/run.py -u 1                                 # Check if 1GB of disk space is available in /opt
    sudo bin/run.py --app jira -p                        # Check application process status          
    sudo bin/run.py --app jira --file /tmp/jira.json -bs # Shutdown application and perform backup
    

options:
  -h, --help            show this help message and exit
  -u DISK_SPACE, --space-required=DISK_SPACE
                        Check for free disk space. Specify in GBs. i.e: 1 for
                        1GB
  -i PACKAGE_NAME, --package-info=PACKAGE_NAME
                        Specify rpm package name with REPO_NAME as an argument

  Application operations:
    Format: sudo ./run --app <name> <option>

    -a APP, --app=APP   Specify app name
    -s, --shut-down     Shutdown application
    -p, --status        Check application process status

  Configuration file operations:
    Format: sudo ./run --app <name> --file <path> <option>

    -f FILE, --file=FILE
                        Specify config file path
    -b                  Backup application. Must use with shutdown option.
    -d                  Download deployment files
```


### Example usage

A few examples.


#### Check if rpm package exists

`sudo bin/run.py -i jdk1.8.0_121 epel`


#### Check for free disk space

```
# Check if 1GB of disk space is available
sudo bin/run.py -u 1
```

#### Check process

`sudo bin/run.py --app jira -p`

#### Download files

`sudo run.py --app jira --file /tmp/jira.json -d`

#### Backup app

This will cause the application to stop running as it is a requirement before the backup operation starts. Note that it
is mandatory to supply the `-s` option to perform the backup. 

`sudo bin/run.py --app jira --file /tmp/jira.json.json -bs`


## Reference

### Idempotent

The script is safe to run multiple times as the backup and download operation will not execute again if it has been 
previously done.

### Logging

The program writes log messages to `/var/tmp/atlassian_admin_tools.log` and `stdout`.

Certain output from commands such as `ps`  is sent only `stdout` but there will be a correponding log message 
on the success or failure of the command written to the log file.


## Limitations

- Requires python 2.4 to run.
- Python 2.4 `optparse` module appears to have limited support for `<program> <command> <options> <args>`.
- File system check is only for `/opt` (at the moment anyway)




