import sys
import os
import re
import time
import subprocess
import shlex

def convert(inFile, outFile, outfilepath, root):
    #@param takes a pointer to the origin file and the output file
    outFile.write('\\documentclass[12pt]{article}\n')
    #TODO make a configurable file for imports <- HERE
    outFile.write ('\\begin{document}\n')
    #TODO make a the same configurable file do author <- HERE
    outFile.write('\\title{Latex'+time.strftime("%c") + '}\n')
    outFile.write('\\maketitle\n')
    for line in inFile:
        if line[0] == '-':
            outFile.write(line+'\\\\')
    outFile.write('i\n\\end{document}')
    command= 'pdflatex ' + outfilepath
    os.chdir(root)
    proc= subprocess.Popen(shlex.split(command))
    proc.communicate
    return



def comp(filepath, root):
    #takes the path to a .txt file and dynamically generates the latex file
    outpath = filepath.rstrip('.txt')+'.tex'
    if True:
        f = open(filepath, 'r')
        if not os.path.isfile(outpath):
            print outpath
            print filepath
            #texfile does not exists
            out = open(outpath, 'w')
            convert(f, out, outpath, root)
        elif True: #os.path.getmtime(filepath) > os.path.getmtime(outpath):
            #proceed normally
            out = open(outpath, 'w')
            convert(f, out, outpath, root)
        else:
            return
    if False:
        print "error in opening files for compilation, exiting"
    return


def default( list ):
    #Default behavior for the toTEX program occurs as a subroutine or when program is called with no arguments
    #Default will recursively search the directory structure beneath the roots in the .conf file
    #Default only looks at the directories who's id's are in the list provided
    #Default assumes that the .conf file exists
    flag = False
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
