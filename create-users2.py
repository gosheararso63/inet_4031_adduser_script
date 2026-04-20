#!/usr/bin/python3

# INET4031
# Ararso Goshe
# Date Created: 04/17/2026
# Date Last Modified: 04/19/2026
# Description: Script that automates user creation and supports interactive dry-run mode

import os
import re
import sys

# The main function asks whether to run in dry-run mode or normal mode.
# In dry-run mode, commands are printed but not executed.
# In normal mode, commands are executed to create users, set passwords, and assign groups.
def main():
    print("Would you like to run in dry-mode? (Y/N): ", end="", flush=True)
    with open("/dev/tty", "r") as tty:
        mode = tty.readline().strip().upper()

    dry_run = (mode == "Y")

    if dry_run:
        print("[DRY-RUN MODE] System commands will not be executed.\n")

    for line in sys.stdin:

        # Check if the line begins with '#' which means it should be skipped
        match = re.match("^#", line)

        # Remove whitespace and split the line into fields
        fields = line.strip().split(':')

        # If the line is marked as a comment, only report it in dry-run mode
        if match:
            if dry_run:
                print("[SKIPPED] Commented line ignored:", line.strip())
            continue

        # If the line does not have exactly 5 fields, only report it in dry-run mode
        if len(fields) != 5:
            if dry_run:
                print("[SKIPPED] Invalid line with", len(fields), "fields:", line.strip())
            continue

        # Extract the values needed to create the account
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # Split group names into a list
        groups = fields[4].split(',')

        print("==> Creating account for %s..." % (username))
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        if dry_run:
            print("[DRY-RUN MODE] Would have executed:", cmd)
        else:
            os.system(cmd)

        print("==> Setting the password for %s..." % (username))
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

        if dry_run:
            print("[DRY-RUN MODE] Would have executed:", cmd)
        else:
            os.system(cmd)

        for group in groups:
            # Only assign groups when the value is not '-'
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)

                if dry_run:
                    print("[DRY-RUN MODE] Would have executed:", cmd)
                else:
                    os.system(cmd)

if __name__ == '__main__':
    main()







