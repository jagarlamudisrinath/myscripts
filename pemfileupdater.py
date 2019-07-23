#!/usr/bin/bash
from subprocess import check_output
keys = check_output("ls -l ~/.ssh/pemfiles/*.pem", shell=True)
text = keys.decode('ascii')
uid = check_output("whoami", shell=True)
f = open(r"/home/{}/.ssh/config".format(uid.decode('ascii').split('\n')[0]),"w")


for line in text.splitlines():
    file = (line.split('/')[5])
    
    user = file.split("-")[1]
    ip = file.split("-")[2].split(".")
    ipadd = "{}.{}.{}.{}".format(ip[0],ip[1],ip[2],ip[3])
    host = file.split("-")[0]+ip[3]
    f.write("Host {}".format(host))
    f.write("\n HostName {}".format(ipadd))
    f.write("\n User {}".format(user))
    f.write("\n IdentityFile {}\n".format(line.split()[-1:][0]))

f.close()

