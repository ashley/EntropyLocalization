import subprocess
import sys
import os
import ConfigParser
import re
from filecmp import dircmp

configs = {}

"""
Reads configuration file called parse_defects4j.cfg
"""
def readConfigurations():
    try:
        config = ConfigParser.ConfigParser()
        config.read('parse_defects4j.cfg')
        configs["project"] = config.get("Basic","project")
        configs["projectNum"] = config.get("Basic","projectNum")
        configs["version"] = config.get("Basic","version")
        configs["examplesPath"] = config.get("Basic","examplesPath")
        configs["srcPath"] = config.get("Basic","srcPath")
        configs["copiedFiles"] = config.get("Basic", "copiedFiles")
        configs["projectPath"] = config.get("Basic", "projectPath")
        configs["genprogPath"] = config.get("Basic", "genprogPath")
        configs["jdk7"] = configs.get("Basic", "jdk7")
        configs["jdk8"] = configs.get("Basic", "jdk8")
        configs["grammarModelPath"] = configs.get("Basic", "grammarModel")
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
        print "jdk7 = <Absolute Path to JVM 7>"
        print "jdk8 = <Absolute Path to JVM 8>"
        print "grammarModelPath = <Absolute path to a directory where your .tsg files are located>"
        print "------"
        sys.exit()

"""
Parses defect4j info command
@param {String} bugID; index of bug version
@return {Dictionary} Keys are file names, Values are file paths.
"""
def defects4jInfo(bugID):
    bashCommand = "defects4j info -p " + configs["project"] + " -b " + bugID
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #Parsing default defects4j info command
    fileStrings =  ["%s%s%s" % (configs["srcPath"],i[3:].replace('.','/'), ".java") for i in 
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
        "defects4j checkout -p ", configs["project"],
        " -v ", bugID,
        "f -w ", configs["examplesPath"],configs["project"], bugID, "F"
        ])
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    configs["fixedPath"] = configs["examplesPath"] + configs["project"] + bugID + "F"

"""
Bash command to checkout Defects4j projects with GenProg configs. Follow GenProg installation before executing
@param {String} bugID; index of bug version
"""
def checkoutGenProgDefects4j(bugID):
        bashCommand = ''.join([
            "bash ", configs["genprogPath"], "/defects4j-scripts/prepareBug.sh ", configs["project"], "  ",
            bugID, " humanMade 1 ", 
            configs["examplesPath"], " " ,
            configs["jdk7"] , " " ,
            configs["jdk8"], " " ,
            configs["genprogPath"] , " " ,
            configs["grammarModelPath"], "/", configs["project"].lower() , bugID , "b.tsg"
            ])
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output

"""
Bash copies modified files to Copies directory
@param {String} bugID; index of bug version
@param {List} filePaths: list of relative paths
"""
def copyModifiedFiles(filePaths, bugID):
    if not os.path.lexists(configs["projectPath"]):
        os.makedirs(configs["projectPath"])

    #Multiple files may have been modified in each version, hence this iteration
    for name, path in filePaths.items():
        buggyCommand =   ''.join([
                        "scp ", configs["examplesPath"], 
                        configs["project"].lower(),
                        bugID, "Buggy/", 
                        path,
                        " ",
                        configs["projectPath"], "/",
                        bugID, "/",
                        "b", "/",
                        name
                        ])
        fixedCommand =   ''.join([
                        "scp ", configs["fixedPath"] ,"/", 
                        path,
                        " ",
                        configs["projectPath"], "/",
                        bugID,  "/",
                        "/f/",
                        name
                        ])
        if not os.path.lexists(configs["projectPath"]+"/"+bugID):
            os.makedirs(configs["projectPath"]+"/"+bugID)
        if not os.path.lexists(configs["projectPath"]+"/"+bugID+"/b"):
            os.makedirs(configs["projectPath"]+"/"+bugID+"/b")
        if not os.path.lexists(configs["projectPath"]+"/"+bugID+"/f"):
            os.makedirs(configs["projectPath"]+"/"+bugID+"/f")

        process = subprocess.Popen(buggyCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output
        process = subprocess.Popen(fixedCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output

def main():
    readConfigurations()
    #for i in range(1,int(configs["projectNum"])+1):
    i = str(configs["projectNum"])
    checkoutGenProgDefects4j(i)
    checkoutFixedProject(i)
    copyModifiedFiles(defects4jInfo(i), i)

main()
