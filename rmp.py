import os
import sys
import getpass
import pexpect

USER_ADDITION="-admin"
COM_ADDITION="quantil.com"
RPM_FILES=[]

def validate_rpm_folder(folder):
    if not os.path.isdir(folder):
        print "Not a correct rpm folder"
        return False

    for f in os.listdir(os.getcwd()):
        if f.endswith(".rpm"):
            RPM_FILES.append(os.path.abspath(f))

    if not RPM_FILES:
        return False

    return True

def validate_ssh_address(addr):
    fixed_addr = addr

    addr_split = addr.split("@")

    if addr_split[0] == '':
        user = getpass.getuser()
        user += USER_ADDITION
        addr_split[0] = user

    if not addr_split[1][-1 * len(COM_ADDITION):] is COM_ADDITION :
        addr_split[1] += ".quantil.com"

    return True

def copy_files_to_server(addr):

    for f in RPM_FILES:
        command = "scp"
        command += "    "
        command += f
        command += "    "
        command += addr
        command += ":"
        command += "/tmp"
        os.system(command)

    return True

def install_in_server(addr):
    ssh_command ="ssh [0]".format(addr)

    conn = pexpect.spawn(ssh_command, timeout=300)
    conn.expect("$", timeout=10)

    for f in RPM_FILES:
        command = "rpm"
        command += "    "
        command += "-Uvh"
        command += "    "
        command += os.path.join("/tmp", f)
        conn.sendline(command)
    return

def _main(arg):
    if not validate_ssh_address(arg):
        return

    if not copy_to_server(arg):
         print "did not work"

    if not install_in_server(arg):
        print "could not install"



def main(argv):

    if not validate_rpm_folder(sys.argv[1]):
        return False

    for arg in sys.argv[2:]:
        print arg
        _main(arg)

if __name__ == "__main__":
    main(sys.argv[1:])
