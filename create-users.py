#!/usr/bin/python3

# INET4031
# Ararso Goshe
# Date Created: 04/17/2026
# Date Last Modified: 04/19/2026

# Import os to execute Linux system commands, re to detect comment lines,
# and sys to read input line by line from standard input
import os
import re
import sys

# The main function reads each line of input and processes valid user entries
def main():
    for line in sys.stdin:

        # This checks if the line starts with '#' which is used to mark comments in the input file
        # Lines starting with '#' are intentionally skipped so they are not processed as user data
        match = re.match("^#", line)

        # This removes extra whitespace and splits the line into parts using ':' as a delimiter
        # Each line is expected to contain exactly 5 fields (username, password, last name, first name, groups)
        fields = line.strip().split(':')

        # This condition skips any line that is either a comment OR does not have exactly 5 fields
        # It relies on the match result (for comments) and the length of fields (for proper formatting)
        # If true, the line is ignored to prevent errors and ensure only valid data is processed
        if match or len(fields) != 5:
            continue

        # These lines extract user information from the fields list
        # The gecos value formats the user's full name in a way that matches how /etc/passwd stores user details
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # This splits the group field into multiple groups using commas
        # This allows a user to be assigned to more than one group
        groups = fields[4].split(',')

        # This print statement gives feedback showing which user is currently being processed
        print("==> Creating account for %s..." % (username))

        # This builds the command used to create a new user account in Linux without prompting for a password
        # The command is stored in the variable "cmd"
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        # This prints and executes the command to create the user
        print(cmd)
        os.system(cmd)

        # This print statement shows that the script is now setting the password for the user
        print("==> Setting the password for %s..." % (username))

        # This builds a command that sends the password into the passwd program automatically
        # It uses echo and a pipe to avoid manual password entry
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

        # This prints and executes the command to set the password
        print(cmd)
        os.system(cmd)

        for group in groups:
            # This checks if the group value is not '-'
            # A '-' means no group should be assigned, so it is skipped
            # If it is a real group name, the user will be added to that group
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))

                # This builds the command to add the user to a specific group
                cmd = "/usr/sbin/adduser %s %s" % (username, group)

                # This prints and executes the command to assign the user to the group
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
