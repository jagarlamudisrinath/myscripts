#!/usr/bin/python
from subprocess import check_output,CalledProcessError
vmscommandoutput = check_output(["virsh", "list"])


def cleanup(records):
    records.pop(0)
    records.pop(0)
    records.pop()
    records.pop()


def getvirtualmachinenames(vmlist):
    listelements = vmlist.decode('ascii').split("\n")
    cleanup(listelements)
    vms = []
    for i in listelements:
        vms.append(i.strip().split()[1])
    return vms


def getmacaddress(hostnames):
    macs = []
    for hostname in hostnames:
        maccommandoutput = check_output(["virsh", "domiflist", "{}".format(hostname)])
        listelements2 = maccommandoutput.decode('ascii').split("\n")
        cleanup(listelements2)
        mac = listelements2[0].split(" ")[-1:][0]
        macs.append(mac)
    return macs


def getipaddress():
    ips = []
    macid = []
    ipcommandoutput = check_output(["virsh", "net-dhcp-leases", "default"])
    listelements3 = ipcommandoutput.decode('ascii').split("\n")
    cleanup(listelements3)
    for i in listelements3:
        x = i.split(" ")
        while '' in x:
            x.remove('')
        macid.append(x[2]),ips.append(x[4].split("/")[0])
    mactoips = dict(zip(macid,ips))
    return mactoips


vms = getvirtualmachinenames(vmscommandoutput)

macids = getmacaddress(vms)

hosttomac = dict(zip(vms,macids))

mactoips = getipaddress()

hostentries = []
for i in vms:
    entry = "{} {}".format(mactoips[hosttomac[i]],i)
    hostentries.append(entry)


check_output(["cp", "-prv", "/root/config/hosts", "/root/config/hostsnew"])

f= open(r"/root/config/hostsnew","a+")

for i in hostentries:
    f.write(i+"\n")
f.close()

check_output(["cp", "-prv", "/root/config/hostsnew", "/etc/hosts"])

for i in vms:
    check_output(["scp", "-prv", "/root/config/hostsnew", "root@{}:/etc/hosts".format(i)])
    print("host entries updated in {}".format(i))
