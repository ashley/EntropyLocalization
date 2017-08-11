import subprocess
import sys
import os
import re
from ConfigParser import SafeConfigParser
from filecmp import dircmp

internalConfiguration = {}

"""
Reads configuration file called parse_defects4j.cfg
@param {String} sectionName: name of the section in configuration file
"""
def readConfigurations():
    try:
	config = SafeConfigParser()
	config.read('parse_defects4j.cfg')
	internalConfiguration["project"] = config.get(sectionName,"project")
	internalConfiguration["projectNum"] = config.get(sectionName,"projectNum")
	internalConfiguration["version"] = config.get(sectionName,"version")
	internalConfiguration["examplesPath"] = config.get(sectionName,"examplesPath")
	internalConfiguration["srcPath"] = config.get(sectionName,"srcPath")
	internalConfiguration["copiedFiles"] = config.get(sectionName, "copiedFiles")
	internalConfiguration["projectPath"] = config.get(sectionName, "projectPath")
	internalConfiguration["genprogPath"] = config.get(sectionName, "genprogPath")
	internalConfiguration["jdkSeven"] = config.get(sectionName, "jdkSeven")        
	internalConfiguration["jdkEight"] = config.get(sectionName, "jdkEight")
	internalConfiguration["grammarModel"] = config.get(sectionName, "grammarModel")
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
    executeCommand(bashCommand)
    fileStrings = parseDefects4JInfo(internalConfiguration["srcPath"])
    #fileNames are found on the end of the path
    fileNames = [i.split('/')[-1] for i in fileStrings]
    filePackage = dict(zip(fileNames, fileStrings))
    return filePackage

"""
Special parsing for defect4j's format
@param {String} outputLog: Given output string from defect's info command
"""
def parseDefects4JInfo(outputLog):
    #Parsing default defects4j info command
    return ["%s%s%s" % (outputLog,i[3:].replace('.','/'), ".java") for i in 
            output.split("--------------------------------------------------------------------------------")
            [-2].strip('\n').split("\n")[1:] ]

"""
Checkout fixed project into Example directory
@param {String} bugID; index of bug version
"""
def checkoutFixedProject(bugID):
    bashCommand = ''.join([
        "defects4j checkout -p ", internalConfiguration["project"],
        " -v ", bugID,
        "f -w ", internalConfiguration["examplesPath"],internalConfiguration["project"], bugID, "Fixed"
        ])
    executeCommand(bashCommand)
    #Must execute bash command to set fixedPath in internal Configs
    internalConfiguration["fixedPath"] = internalConfiguration["examplesPath"] + internalConfiguration["project"] + bugID + "Fixed"

"""
Bash command to checkout Defects4j projects with GenProg internalConfiguration. Follow GenProg installation before executing
@param {String} bugID; index of bug version
"""
def checkoutGenProgDefects4j(bugID):
        bashCommand = ''.join([
            "bash ", internalConfiguration["genprogPath"], "/defects4j-scripts/prepareBug.sh ",
            internalConfiguration["project"], "  ",
            bugID, " humanMade 1 ", 
            internalConfiguration["examplesPath"], " " ,
            internalConfiguration["jdkSeven"] , " " ,
            internalConfiguration["jdkEight"], " " ,
            internalConfiguration["genprogPath"] , " " ,
            internalConfiguration["grammarModel"], "/", internalConfiguration["project"].lower() , bugID , "b.tsg"
            ])
        print executeCommand(bashCommand)

"""
Bash copies modified files to Copies directory
@param {String} bugID: index of bug version
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
        projectIDPath = internalConfiguration["projectPath"]+"/"+bugID
        checkDirectory(projectIDPath)
        checkDirectory(projectIDPath+"/b")
        checkDirectory(projectIDPath+"/f")

        print executeBash(buggyCommand)
        print executeBash(fixedCommand)

"""
Helper function for making directory
@param {Sting} path: path to directory to create
"""
def checkDirectory(path):
    if not os.path.lexists(path):
        os.makedirs(path)

"""
Helper function for executing bash commands
@param {String} command: bash command
@return {String} output: Any output print from bash command execution
"""
def executeBash(command):
    process = subprocess.Popen(commandList.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output

def main():
    readConfigurations()
    projectNum = str(internalConfiguration["projectNum"])
    checkoutGenProgDefects4j(projectNum)
    checkoutFixedProject(projectNum)
    copyModifiedFiles(defects4jInfo(projectNum), projectNum)

if __name__ == "__main__":
    main()
