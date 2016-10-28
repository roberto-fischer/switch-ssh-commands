#!/usr/bin/python
import paramiko
import sys
import argparse
import time


def main():
    # Defining my input variables
    # Building the argument parser
    parser = argparse.ArgumentParser(description='Send commands to network devices')
    parser.add_argument("-e", "--enable", action="store", dest="enable",
                        help="The user's enable password if different from regular password")
    parser.add_argument("-d", "--device", action="store", dest="hosttype", choices=["cisco", "dell", "hp", "a10"],
                        help="Choose a device to run commands against")
    parser.add_argument("-u", "--user", action="store", dest="username", help="Username to login as")
    parser.add_argument("-p", "--pass", action="store", dest="password", help="The user's password")
    parser.add_argument("-H", "--host", action="store", dest="hostname", help="The remote host")
    parser.add_argument("-c", "--command", action="store", dest="dirty_commands",
                        help="Commands to be run on the remote device. Separate multiple commands with ;")

    items = parser.parse_args()

    log = '/tmp/sw-cmds/' + items.hostname
    print(log)
    # Splitting the commands into an array
    commands = items.dirty_commands.split(";")
    print(items.enable, items.username, items.password, items.hostname, items.dirty_commands)
#    Choosing the appropriate function to use depending on the selected device
    if items.hosttype == "cisco" or items.hosttype == "a10":
            result = cisco(items.username, items.password, items.enable, items.hostname, commands)
    elif items.hosttype == "dell":
            result = dell(items.username, items.password, items.enable, items.hostname, commands)
    elif items.hosttype == "hp":
            result = hp(items.username, items.password, items.enable, items.hostname, commands)
    else:
        # If nothing was chosen
        print("No proper device selected...")
        sys.exit()

#   result = cisco(items.username, items.password, items.enable, items.hostname, commands)
    target = open(log, 'w')
    target.write(result)
    target.close()
    sys.exit()


def cisco(user, passw, enable, hostname, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("/tmp/paramiko.log")

    try:
        ssh.connect(hostname, username=user, password=passw, look_for_keys=False, allow_agent=False)
        ssh_conn = ssh.invoke_shell()
    except paramiko.ssh_exception.AuthenticationException:
        print("Connection closed due to incorrect credentials")
        return('0')

    time.sleep(1)
    output = ssh_conn.recv(2000)
    if enable == "":
        enable = passw

    if output[-1] == ">":
        ssh_conn.send("enable\n")
        ssh_conn.send(enable + "\n")
        output = ssh_conn.recv(2000)
        if output[-1] == ">":
            ssh_conn.close()
            ssh.close()
            return("Connection closed due to incorrect enable credentials")
    time.sleep(1)
    ssh_conn.send("terminal length 0\n")
    time.sleep(1)
    for cmd in commands:
        ssh_conn.send(cmd + "\n")
        time.sleep(1)
        output = output + ssh_conn.recv(50000)
        print output
    ssh_conn.send("terminal length 24\n")
    time.sleep(1)
    ssh_conn.close()
    ssh.close()
    print(output)
    return(output)


def dell(user, passw, enable, hostname, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko.util.log_to_file("/tmp/paramiko.log")

    try:
        ssh.connect(hostname, username=user, password=passw, look_for_keys=True, allow_agent=False,
                    key_filename="./id_rsa")
        ssh_conn = ssh.invoke_shell()
    except paramiko.ssh_exception.AuthenticationException:
        print("Connection closed due to incorrect credentials")
        return('0')

    time.sleep(1)
    output = ssh_conn.recv(2000)
    if enable == "":
        enable = passw

    if output[-1] == ">":
        ssh_conn.send("enable\n")
        ssh_conn.send(enable + "\n")
        output = ssh_conn.recv(2000)
        if output[-1] == ">":
            ssh_conn.close()
            ssh.close()
            return("Connection closed due to incorrect enable credentials")
    time.sleep(1)
    ssh_conn.send("terminal length 0\n")
    time.sleep(1)
    for cmd in commands:
        ssh_conn.send(cmd + "\n")
        time.sleep(1)
        output = output + ssh_conn.recv(50000)
        print output
    ssh_conn.send("terminal length 24\n")
    time.sleep(1)
    ssh_conn.close()
    ssh.close()
    print(output)
    return(output)


def hp(user, passw, enable, hostname, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=user, password=passw, look_for_keys=False, allow_agent=False)
        ssh_conn = ssh.invoke_shell()
    except paramiko.ssh_exception.AuthenticationException:
        print("Connection closed due to incorrect credentials")
        return('0')

    time.sleep(1)
    ssh_conn.send(" screen-length disable\n")
    time.sleep(1)
    output = ''

    for cmd in commands:
        ssh_conn.send(" " + cmd + "\n")
        time.sleep(1)
        output = output + ssh_conn.recv(50000)
        print output
    time.sleep(1)
    ssh_conn.send(" screen-length disable\n")
    time.sleep(1)
    ssh_conn.close()
    ssh.close()
    print(output)
    return(output)


if __name__ == '__main__':
    sys.exit(main())
