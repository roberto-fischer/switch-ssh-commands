import paramiko
import sys
import time


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('10.30.0.6', username='admin', password='barf', look_for_keys=False, allow_agent=False)
        ssh_conn = ssh.invoke_shell()
    except paramiko.ssh_exception.AuthenticationException:
        print("Connection closed due to incorrect credentials")
        return('0')

    time.sleep(1)
    output = ssh_conn.recv(2000)
    print(output)

    if b"authentication" in output:
        ssh_conn.close()
        ssh.close()
        return("Connection closed due to incorrect login credentials")

    enable = 'SpassE32'

    ssh_conn.send("enable\n")
    ssh_conn.send("SpassE32\n")
    time.sleep(1)
    output = ssh_conn.recv(2000)
    print(output)

    ssh_conn.send("terminal length 0\n")
    time.sleep(1)
    ssh_conn.send("show version\n")
    time.sleep(1)
    output = ssh_conn.recv(20000)
    ssh_conn.send("terminal length 24\n")
    time.sleep(1)
    ssh_conn.close()
    ssh.close()
    print(output)


if __name__ == '__main__':
    sys.exit(main())
