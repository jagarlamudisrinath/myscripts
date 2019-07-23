#!/usr/bin/python
import sys
from subprocess import check_output,CalledProcessError


hostname = sys.argv[1]
hostname = hostname.replace(" ","").lower()


if len(hostname) <= 6:
    print("VM name should have atlease seven charecters.")
else:
    text = check_output(["virsh", "list", "--all"]).decode("ascii")
    text = text.splitlines()
    text.pop()
    text.pop(0)
    text.pop(0)
    hostnames = []
    status = []
    for i in text:
        i = i.strip().split()
        hostnames.append(i[1])
        status.append(i[2])
    statustable = dict(zip(hostnames,status))
    try:
        vmstat = statustable[hostname]
        if vmstat == "shut":
            try:
                check_output(["virsh", "undefine", "{}".format(hostname)])
                check_output(["rm", "-rf", "/kvm/{}".format(hostname)])
                check_output(["rm", "-rf", "/etc/libvirt/qemu/{}.xml".format(hostname)])
                print("VM Deleted Successfully.")
            except CalledProcessError:
                pass
        
        else:
            check_output(["virsh", "destroy", "{}".format(hostname)])
            try:
                check_output(["virsh", "undefine", "{}".format(hostname)])
                check_output(["rm", "-rf", "/kvm/{}".format(hostname)])
                check_output(["rm", "-rf", "/etc/libvirt/qemu/{}.xml".format(hostname)])
                print("VM Deleted Successfully.")
            except CalledProcessError:
                pass

    except KeyError:
        print("Vm Alredy deleted.")
    
        
