import subprocess
import sys
import os
import re
from ConfigParser import SafeConfigParser
from filecmp import dircmp

internalConfiguration = {}

"""
Reads configuration file called parse_defects4j.cfg
"""
def readConfigurations():
    try:
	config = SafeConfigParser()
	config.read('parse_defects4j.cfg')
	internalConfiguration["project"] = config.get("Basic","project")
	internalConfiguration["projectNum"] = config.get("Basic","projectNum")
	internalConfiguration["version"] = config.get("Basic","version")
	internalConfiguration["examplesPath"] = config.get("Basic","examplesPath")
	internalConfiguration["srcPath"] = config.get("Basic","srcPath")
	internalConfiguration["copiedFiles"] = config.get("Basic", "copiedFiles")
	internalConfiguration["projectPath"] = config.get("Basic", "projectPath")
	internalConfiguration["genprogPath"] = config.get("Basic", "genprogPath")
	internalConfiguration["jdkSeven"] = config.get("Basic", "jdkSeven")        
	internalConfiguration["jdkEight"] = config.get("Basic", "jdkEight")
	internalConfiguration["grammarModel"] = config.get("Basic", "grammarModel")
    except:
        print "Error with Configuration file. Please make sure it meets these specifications: "
        print "FileName: parse_defects4j.cfg   File Path: same directory as diffBugs.py"
        print "---CONFIG SPECIFICATION---"
        print "[Basic]"
        print "project = <name of projet according to Defects4j>"
        print "projectNum = <number of version IDs to iterate>"
        print "version = <b or f>"
        print "examplesPath = <absolute path to directory with GenProg defects4j projects>"
        print "srcPath = <relative path from project directory to source code path>"
        print "copiedFiles = <absolute path to resulting directory>"
        print "projectPath = <Absolute Path to resulting project directory>"
        print "genprogPath = <Absolute Path to GenProg4java>"
        print "jdkSeven = <Absolute Path to JVM 7>"
        print "jdkEight = <Absolute Path to JVM 8>"
        print "grammarModel = <Absolute path to a directory where your .tsg files are located>"
        print "------"
        sys.exit()
"""
Parses defect4j info command
@param {String} bugID; index of bug version
@return {Dictionary} Keys are file names, Values are file paths.
"""
def defects4jInfo(bugID):
    bashCommand = "defects4j info -p " + internalConfiguration["project"] + " -b " + bugID
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #Parsing default defects4j info command
    fileStrings =  ["%s%s%s" % (internalConfiguration["srcPath"],i[3:].replace('.','/'), ".java") for i in 
                    output.split("--------------------------------------------------------------------------------")
                    [-2].strip('\n').split("\n")[1:]
    
                    ]
    fileNames = [i.split('/')[-1] for i in fileStrings]
    filePackage = dict(zip(fileNames, fileStrings))
    return filePackage

"""
Checkout fixed project into Example directory
@param {String} bugID; index of bug version
"""
def checkoutFixedProject(bugID):
    bashCommand = ''.join([
        "defects4j checkout -p ", internalConfiguration["project"],
        " -v ", bugID,
        "f -w ", internalConfiguration["examplesPath"],internalConfiguration["project"], bugID, "F"
        ])
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    internalConfiguration["fixedPath"] = internalConfiguration["examplesPath"] + internalConfiguration["project"] + bugID + "F"

"""
Bash command to checkout Defects4j projects with GenProg internalConfiguration. Follow GenProg installation before executing
@param {String} bugID; index of bug version
"""
def checkoutGenProgDefects4j(bugID):
        bashCommand = ''.join([
            "bash ", internalConfiguration["genprogPath"], "/defects4j-scripts/prepareBug.sh ", internalConfiguration["project"], "  ",
            bugID, " humanMade 1 ", 
            internalConfiguration["examplesPath"], " " ,
            internalConfiguration["jdkSeven"] , " " ,
            internalConfiguration["jdkEight"], " " ,
            internalConfiguration["genprogPath"] , " " ,
            internalConfiguration["grammarModel"], "/", internalConfiguration["project"].lower() , bugID , "b.tsg"
            ])
        print bashCommand
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output

"""
Bash copies modified files to Copies directory
@param {String} bugID; index of bug version
@param {List} filePaths: list of relative paths
"""
def copyModifiedFiles(filePaths, bugID):
    if not os.path.lexists(internalConfiguration["projectPath"]):
        os.makedirs(internalConfiguration["projectPath"])

    #Multiple files may have been modified in each version, hence this iteration
    for name, path in filePaths.items():
        buggyCommand =   ''.join([
                        "scp ", internalConfiguration["examplesPath"], 
                        internalConfiguration["project"].lower(),
                        bugID, "Buggy/", 
                        path,
                        " ",
                        internalConfiguration["projectPath"], "/",
                        bugID, "/",
                        "b", "/",
                        name
                        ])
        fixedCommand =   ''.join([
                        "scp ", internalConfiguration["fixedPath"] ,"/", 
                        path,
                        " ",
                        internalConfiguration["projectPath"], "/",
                        bugID,  "/",
                        "/f/",
                        name
                        ])
        if not os.path.lexists(internalConfiguration["projectPath"]+"/"+bugID):
            os.makedirs(internalConfiguration["projectPath"]+"/"+bugID)
        if not os.path.lexists(internalConfiguration["projectPath"]+"/"+bugID+"/b"):
            os.makedirs(internalConfiguration["projectPath"]+"/"+bugID+"/b")
        if not os.path.lexists(internalConfiguration["projectPath"]+"/"+bugID+"/f"):
            os.makedirs(internalConfiguration["projectPath"]+"/"+bugID+"/f")

        process = subprocess.Popen(buggyCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output
        process = subprocess.Popen(fixedCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output

def main():
    readConfigurations()
    #for i in range(1,int(internalConfiguration["projectNum"])+1):
    i = str(internalConfiguration["projectNum"])
    checkoutGenProgDefects4j(i)
    checkoutFixedProject(i)
    copyModifiedFiles(defects4jInfo(i), i)

main()
