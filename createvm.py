#!/usr/bin/python
import sys
from subprocess import check_output,CalledProcessError
hostname = sys.argv[1]
hostname = hostname.replace(" ","").lower()

if len(hostname) <= 6:
    print("VM name should have atlease seven charecters.")
else:
    try:
        check_output(["mkdir", "/kvm/{}".format(hostname)])
	check_output(["virt-clone", "--original", "devtemplate", "--name", "{}".format(hostname), "--file", "/kvm/{}/devtemplate.qcow2".format(hostname)])
	print("VM Created Successfully.")
    except CalledProcessError:
        print("VM Alredy exist.")
