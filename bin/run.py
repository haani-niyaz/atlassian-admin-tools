#!/usr/bin/env python

"""Run program"""

import os
import sys


if os.getuid() != 0:
    print("Invalid usage. Script must be executed as a privileged user i.e: sudo ./run.py <options>")
    sys.exit(1)

# Append to module path
sys.path.append(
    os.path.dirname(sys.path[0]))

import app

if __name__ == '__main__':
	app.invoke()
