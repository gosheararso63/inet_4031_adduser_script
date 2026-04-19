# inet_4031_adduser_script

# Automated User Creation Script

## Program Description
This project automates the creation of Linux user accounts from a structured input file. The script reads user information line by line, creates accounts, sets passwords, and assigns users to groups based on the values provided in the input file.

## Program Operation
The script reads input from `create-users.input` through standard input. Each valid line must contain 5 colon-separated fields in the following format:

`username:password:last:first:groups`

Lines that begin with `#` are treated as comments and skipped. Lines that do not contain exactly 5 fields are also skipped.

To run the script after making it executable:

```bash
sudo ./create-users.py < create-users.input
