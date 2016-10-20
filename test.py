import paramiko
import sys


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('10.30.0.6', username='admin', password='SpassE32', look_for_keys=False, allow_agent=False)
    ssh_conn = ssh.invoke_shell()
    output = ssh_conn.recv(2000)

    if b"authentication" in output:
        ssh_conn.close()
        ssh.close()
        return("Connection closed due to incorrect login credentials")

    enable = 'SpassE32'

    if output[-1] == ">":
        ssh_conn.send("enable\n")
        ssh_conn.send(enable + "\n")
        output = ssh_conn.recv(2000)
        if output[-1] == ">":
            ssh_conn.close()
            ssh.close()
            return("Connection closed due to incorrect enable credentials")

    ssh_conn.send("show clock detail\n")
    output = ssh_conn.recv(20000)
    ssh_conn.close()
    ssh.close()
    print(output)


if __name__ == '__main__':
    sys.exit(main())
