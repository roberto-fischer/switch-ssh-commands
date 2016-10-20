import paramiko
import sys
import argparse


def main():
    # Defining my input variables
    username = ''
    password = ''
    enable = ''
    hostname = ''
    hosttype = ''
    dirty_commands = ''

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

    # Splitting the commands into an array
    commands = dirty_commands.split(";")

    # Choosing the appropriate function to use depending on the selected device
    if hosttype == "cisco":
            cisco(username, password, enable, hostname, commands)
    elif hosttype == "dell":
            dell(username, password, enable, hostname, commands)
    elif hosttype == "hp":
            hp(username, password, enable, hostname, commands)
    elif hosttype == "a10":
            a10(username, password, enable, hostname, commands)
    else:
        # If nothing was chosen
        print("No proper device selected...")
        sys.exit()


def cisco(user, passw, enable, hostname, commands=[]):
    pass
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=user, password=passw, look_for_keys=False,
                allow_agent=False)
    ssh_conn = ssh.invoke_shell()
    output = ssh_conn.recv(2000)

    if "authentication" in output:
        ssh_conn.close()
        ssh.close()
        return("Connection closed due to incorrect login credentials")

    if enable == "":
        enable = passw

    if output[-1] == ">":
        ssh_conn.send(enable)
        output = ssh_conn.recv(2000)
        if output[-1] == ">":
            ssh_conn.close()
            ssh.close()
            return("Connection closed due to incorrect enable credentials")

    for cmd in output:
        ssh_conn.send(cmd + "\n")
        output = ssh_conn.recv(20000)
    ssh_conn.close()
    ssh.close()
    print(output)
    sys.exit()


def dell(user, passw, enable, hostname, commands=[]):
    pass


def hp(user, passw, enable, hostname, commands=[]):
    pass


def a10(user, passw, enable, hostname, commands=[]):
    pass


if __name__ == '__main__':
    sys.exit(main())
