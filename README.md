# atlassian-admin-tools

#### Table of Contents

1. [Description](#description)
2. [Setup - The basics of getting started with [atlassian-admin-tools]](#setup)
    * [What [atlassian-admin-tools] affects](#what-atlassian-admin-tools-affects)
    * [Setup requirements](#setup-requirements)
    * [Beginning with [atlassian-admin-tools]](#beginning-with-atlassian-admin-tools)
3. [Usage - Configuration options and additional functionality](#usage)
4. [Limitations - OS compatibility, etc.](#limitations)
5. [Development - Guide for contributing to the module](#development)


## Description

Provide an utility to to execute deployment pre-checks and pre-implementation steps.      

### Capabilities:

- Stop service prior to backup
- Check service process
- Executes commands as the application user
- Backup files (as specified in the config file)
- Download deployment files (as specified in the config file)
- Logging to stdout and writes to file

## Setup

### What [atlassian-admin-tools] affects 

The application reads a json config file which specifies:

- Files to backup
- Backup directory
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
[atlassian-admin-tools]$ sudo ./run.py 
usage: 
	run.py --app <jira|bamboo|bitbucket|crowd> --file <filename>.json [options] 

	Backup Example
	--------------
	run.py --app jira --file /tmp/jira.json -bs
	

options:
  -h, --help            show this help message and exit
  -a APP, --app=APP     Specify app name
  -f FILE, --file=FILE  Specify config file path
  -b                    Backup application. Must use with shutdown flag.
  -p                    Check application process
  -s                    Shutdown application
  -d                    Download deployment files

```


### Example usage

A few examples.

#### Check process

`sudo ./run.py --app jira --file /tmp/jira.json.json -p`

#### Download files

`sudo run.py --app jira --file /tmp/jira.json -d`

#### Backup app

This will cause the application to stop running as it is a requirement before backup the operation starts. This is the only state changing action the program executes.

`sudo ./run.py --app jira --file /tmp/jira.json.json -bs`


## Limitations

- Requires python `2.4` to run.


## Development

### TO-DO

- Include json validation as a program option
- Module vs. Class split
- Refactor project structure
- Refactor error handling
- Clean up orphaned tar file if `tar.add()` fails
- Inlcude unit testing


