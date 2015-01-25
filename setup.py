import os
import sys


if not os.path.isfile(os.getcwd() + "/imports.conf"):
	#imports file is missing,generate empty file
	f=open(os.getcwd() + "/imports.conf", 'w')
	print "please enter the import you wish to have globally included"
	line = sys.stdin.readline()
	f.write(line)
	print "generated import configuration"

if not os.path.isfile(os.getcwd() + "/user.conf"):
	f=open(os.getcwd() + "/user.conf",'w')
	print "generated user configuration file"
	print "enter desired author:"
	data = sys.stdin.readline()
	f.write(data.rstrip('\n'))


#Note it is assumed that the structure of the
#toTEX folders are not modified
if not os.path.isfile(os.getcwd() + "/toTEX.conf"):
    f=open(os.getcwd()+ "/toTEX.conf", 'w')
    #we know the file did not exist previously thus it is safe to print **1 to it as this will be the first entry
    f.write("**1\n")
    print "please enter the root directory which contains the project files"
    print "Note only absolute paths are accepted:"
    data = sys.stdin.readline()
    if not os.path.isdir(''.join(data).rstrip('\n')):
        #user has provided a path that does not exist or is not vissible
        print "invalid path provided, exiting now"
        #clean up the conf file fragment
        os.remove(os.getcwd() + "/toTEX.conf")
        sys.exit()
    else:
        #the file provided is alright
        f.write("#path:"+ ''.join(data))

else:
    if os.path.getsize(os.getcwd()+"/toTEX.conf")==0:
            #if the file exists and is empty something is wrong
            print ".conf file exists but is empty! cleaning up and exiting"
            os.remove(os.getcwd()+"/toTEX.conf")
            sys.exit()
    else:
            #no reason to be running setup utility with no flags
            print ".conf seems in order, exiting"
            sys.exit()


