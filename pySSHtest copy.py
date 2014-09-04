import paramiko
import time
import csv
import os
import sys

userinputcommand = raw_input("Enter commands: ")

with open(os.path.join(sys.path[0], "myfile.csv"), "r+") as f:
 reader = csv.reader(f)
 for row in reader:
    ip = row[0]
    username = row[1]
    password = row[2]
    command = userinputcommand + '\n'
    print "Connected to " + ip  
    remote_conn_pre=paramiko.SSHClient()
    remote_conn_pre 
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        remote_conn_pre.connect(ip, username=username, password=password)
        paramiko.ssh_exception.AuthenticationException
        print "SSH Authenticated!!"
        remote_conn = remote_conn_pre.invoke_shell()
        time.sleep(1)
        nulloutput = remote_conn.recv(50000)
        remote_conn.send(' \n')
        time.sleep(1)
        prompt = remote_conn.recv(50000)
        propmt = str(prompt)
        prompt =  prompt.strip()

        
        remote_conn.send(command)
        time.sleep(1)
        commandresult = remote_conn.recv(50000)
        commandresult = str(commandresult)
        commandresult = commandresult.replace(prompt, '')
        commandresult = commandresult.replace(userinputcommand, '')
        commandresult = commandresult.strip()
        print commandresult
        
        print ip + " Done!"
        f = open(os.path.join(sys.path[0], "logs.csv"), 'a+')
        f.write(commandresult + '\n')
        f.close()
       # with open(os.path.join(sys.path[0], "logs.csv"), 'a+') as g:
            #writer = csv.writer(g, delimiter=',')
            #writer.writerow([commandresult])
        print "Data successfully saved!!"
    except:
        raise
        #print "Connection Failed"
        #command = "NONE"
        #commandresult = "SSH FAILED"
        #with open(os.path.join(sys.path[0], "logs.csv"), 'a+') as g:
            #writer = csv.writer(g, delimiter=',')
            #writer.writerow([command,commandresult])
           
