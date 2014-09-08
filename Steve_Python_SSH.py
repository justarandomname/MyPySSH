#Import Statements#
import paramiko
import time
import datetime
import csv
import os
import os.path
import sys
#Import statements
ip = ""
username = ""
password = ""
errorlog = ""
sourcefile = ""
destfile = ""
jumpbox = ""
command = ""
userinputcommand = ""

#Print commands for testing only
def printtest():
    print ip
    print username
    print password
    #print command
    #print commandresult
    print sourcefile
    print destfile
    print errorlog

def jumper():
   global ip
   global username
   global password
   global jumpbox
   jumpbox = raw_input("Do you need to SSH to a jump box first? (Y/N) ")
   if jumpbox == "Y" or jumpbox == "y":
      ip = raw_input("Type Jumpbox Ip address or FQDN ")
      username = raw_input("Type your username")
      password = raw_input("Type your password - THIS IS NOT ENCRYPTED. IT IS SHOWN ON THE SCREEN!! ")
      paramikossh()
      
   elif jumpbox != "Y" and jumpbox != "N" and jumpbox != "y" and jumpbox != "n":
      print "Not valid!!"
      jumper()
   else:
      print "" #need to work out how to break out of here...
      
         
def createfiles():
      global sourcefile
      global destfile
      global errorlog
      global userinputcommand
      userinputcommand = raw_input("Enter commands here separated by a semi colen! ") #commands to be run on remote system
      #sourcefile = "" # sets sourcefile to be null
      sourcefile = raw_input("Type source directory path here. Leave blank for current dir. File name must be input.csv ") #directory where the source is

      if sourcefile == "": #if source is null, it is set to the current dir
         sourcefile = os.getcwd() + "\input.csv"
      else:
        sourcefile = sourcefile + "\input.csv"
        
      if os.path.isfile(sourcefile) and os.access(sourcefile,os.R_OK): #checks to see if the file actually exists
        print "Source File Exists!"
      else:
        print "Source File does not exist!!"

      destfile = "" # Set dest file to null
      destfile = raw_input("Type destination file file path and name. Leave blank for current dir. ")#directory where the dest is

      if destfile == "": #if dest is null, it is set to current dir
         destfile = os.getcwd() + "\output.csv"
      else:
        destfile = destfile + "\output.csv"

        
      if os.path.isfile(destfile) and os.access(destfile,os.R_OK): #checks to see if the dest file exists, if not, create it. 
         print "Note - Destination file already exists. The program will append to it"
      else:
         with open(destfile, 'ab+') as destcreate:
            writer = csv.writer(destcreate)
            writer.writerow(["IP/FQDN","Username","Password","Command","Command Result","Timestamp"])
         print "Creating Dest file"
         
      errorlog = os.getcwd() + "\errorlog.csv"
      if os.path.isfile(errorlog) and os.access(errorlog,os.R_OK): #checks to see if the errorlog file exists, if not, create it. 
         print "Note - Errorlog file already exists. The program will append to it"
      else:
         with open(errorlog, 'ab+')  as errorcreate:
            writer = csv.writer(errorcreate)
            writer.writerow(["IP/FQDN","Username","Password","Command","Command Result","Timestamp"])
         print "Creating errorlog"



def main():
    print sourcefile
    global sourcefile
    global command
    global userinputcommand
    global ip
    global username
    global password
    with open(sourcefile, 'rb') as f: #gets the source file
       reader = csv.DictReader(f, delimiter = ",") #create instance of csv reader
       for row in reader: #for loop to iterate through the source
          ip = row["ip"]
          username = row['username']
          password = row['password']
          print "Finished reading CSV File!"
          command = userinputcommand
          paramikossh()
          

          
def paramikossh():
          global jumpbox
          global ip
          global username
          global password
          global command
          
          print "Starting SSH Session to " + ip + "!" 
          remote_conn_pre=paramiko.SSHClient() #creates an instance of paramiko SSH Client
          remote_conn_pre 
          remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #auto accepts any missing host keys
          try: #loop to try and preform commands on target
             remote_conn_pre.connect(ip, username=username, password=password)
             print "SSH Authenticated!!"
             remote_conn = remote_conn_pre.invoke_shell()
             time.sleep(3)
             nulloutput = remote_conn.recv(50000)
             remote_conn.send(command + "\n")
             remote_conn.send("\n")
             time.sleep(3)
             commandresult = remote_conn.recv(50000)
             print ip + " Done!"
             with open(destfile, 'ab') as g: #print results to dest file.
              timenow = datetime.datetime.now()
              writer = csv.writer(g)
              writer.writerow([ip,username,password,command,commandresult, timenow])
              print "Data successfully saved!!"
              if jumpbox == "Y" or jumpbox == "y":
                jumpboxssh()
              else:
                print ""
                
          except: """#If any ssh error occurs, print error to errorlog
                if jumpbox == "Y" or jumpbox == "y":
                    print "Connection to Jumpbox failed :("
                    command = "NONE"
                    commandresult = "SSH TO JUMPBOX FAILED"
                    with open(errorlog, 'ab') as g:
                     timenow = datetime.datetime.now()
                     writer = csv.writer(g)
                     writer.writerow([ip,username,password,command,commandresult, timenow])
                    jumper()
                else:
                    print "Connection Failed :( Not sure why..."
                    command = "NONE"
                    commandresult = "SSH FAILED"
                    with open(errorlog, 'ab') as g:
                     timenow = datetime.datetime.now()
                     writer = csv.writer(g)
                     writer.writerow([ip,username,password,command,commandresult, timenow])"""


#############################Not tested##########################################
def jumpboxssh():
    print sourcefile
    global sourcefile
    global command
    global userinputcommand
    global ip
    global username
    global password
    with open(sourcefile, 'rb') as f: #gets the source file
       reader = csv.DictReader(f, delimiter = ",") #create instance of csv reader
       for row in reader: #for loop to iterate through the source
          ip = row["ip"]
          username = row['username']
          password = row['password']
          print "Finished reading CSV File!"
          command = userinputcommand
          try: #loop to try and preform commands on target
             nulloutput = remote_conn.recv(50000)
             remote_conn.send("\n")
             login = ("ssh " + username + "@" + ip + "\n")
             print login
             remote_conn.send(login)
             #testing t = remote_conn.recv(500)
             #testing print t
             remote_conn.send(password + "\n")
             #testing t = remote_conn.recv(500)
             #testing print t
             print "SSH Authenticated!!"
             remote_conn.send(command + "\n")
             commandresult = remote_conn.recv(50000)
             remote_conn.send("exit" + "\n")
             print ip + " Done!"
             with open(destfile, 'ab') as g: #print results to dest file.
              timenow = datetime.datetime.now()
              writer = csv.writer(g)
              writer.writerow([ip,username,password,command,commandresult, timenow])
              print "Data successfully saved!!"
          except: """#If any ssh error occurs, print error to errorlog
                print "Connection Failed :( Not sure why..."
                command = "NONE"
                commandresult = "SSH FAILED"
                with open(errorlog, 'ab') as g:
                 timenow = datetime.datetime.now()
                 writer = csv.writer(g)
                 writer.writerow([ip,username,password,command,commandresult, timenow])"""
#############################Not tested##########################################


def final():
      printfinal = raw_input("All complete!! Press any key to close the program...") #should be printed when all lines in source have been tried
      if printfinal == "*" or "\n":
        sys.exit(0)
      else:
         print "I don't know how you got here...but I'm closing anyway!"
         sys.exit(100)

createfiles()
jumper()

if jumpbox == "y" or jumpbox == "Y":
    ""
else:
   main()
   
final()
