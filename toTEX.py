import sys
import os
import re
import time
import subprocess
import shlex

#constant parameter set to the original working directory
originPath=""

def convert(inFile, outFile, outfilepath, root):
    print "converting: " + outfilepath
    #@param takes a pointer to the origin file and the output file
    try:
        f = open( os.path.join(originPath,"imports.conf"), 'r')
    except:
        print "File structure damaged please run setup.py"
        sys.exit()
    for line in f:
        outFile.write("\include{" + line.rstrip('\n') + '}\n')
     
    
    outFile.write('\\documentclass[12pt]{article}\n')
    outFile.write('\\begin{document}\n')

    try:
        f2= open( os.path.join(originPath,"user.conf"), 'r')    
    except:
        print "File structure damaged please run setup.py"
        sys.exit()    
    for line in f2:
        outFile.write("\\author{" + line.rstrip('\n') + "}\n")

    outFile.write('\\title{Latex'+ outfilepath.rstrip(".tex") + '}\n')
    outFile.write('\\maketitle\n')
    flag = False
    for line in inFile:
	line = line.lstrip()
	if line[0] == '-':
	    if not flag:
                outFile.write('\\begin{enumerate}\n')
                flag = True
	    outFile.write('\\item\n' + line[1:])  
	else:
            if flag:
                outFile.write('\\end{enumerate')
                flag = False
	    if line[0] != '-' and line[0] != '\n':
            	outFile.write(line)

    if flag:
	outFile.write('\n\\end{enumerate}')
	
    outFile.write('\n\\end{document}')
    command= 'pdflatex ' + outfilepath
    os.chdir(root)
    proc= subprocess.Popen(shlex.split(command))
    proc.communicate
    os.remove
    return



def comp(filepath, root):
    #takes the path to a .txt file and dynamically generates the latex file
    outpath = (filepath.rstrip('.txt')+'.tex').rstrip('\n')
    try:
        f = open(filepath, 'r')
        if not os.path.isfile(outpath):
            print outpath
            print filepath
            #texfile does not exists
            out = open(outpath, 'w')
            convert(f, out, outpath, root)
        elif os.path.getmtime(filepath) > os.path.getmtime(outpath):
            #proceed normally
            out = open(outpath, 'w')
            convert(f, out, outpath, root)
        else:
            return
    except:
        print "error in opening files for compilation, exiting " + outpath
    return


def default( list ):
    #Default behavior for the toTEX program occurs as a subroutine or when program is called with no arguments
    #Default will recursively search the directory structure beneath the roots in the .conf file
    #Default only looks at the directories who's id's are in the list provided
    #Default assumes that the .conf file exists
    flag = False
    originPath = os.getcwd()
    try:
        f = open(os.path.join(os.getcwd(), 'toTEX.conf'), 'r')
    except:
        print "please run setup.py to create configuration file"
        sys.exit()
    for line in f:
        a= re.compile("^-?[0-9]+$")
        numString  = (''.join(line).strip('**')).rstrip('\n')
        pathString = (''.join(line).strip('#path:')).rstrip('\n')
        if a.match(numString) :
            if numString in list :
                flag = True
            else:
                #we are not concerned with this particular directory so continue
                continue
        else:
            #our line is a path
            if flag :
                #we should go into this directory
                for root, subFolders, files in os.walk(pathString) :
                    #we handle the sub directories first
                    for tfile in files:
                        if tfile.endswith(".txt" ):
                            comp(os.path.join(root, tfile), root)
                        else:
                            #this is not thefile you are looking for!
                            continue
                flag = False
            else:
                #the line is a directory but we need not look at it
                continue

    #we are done
    return



default(['1'])
