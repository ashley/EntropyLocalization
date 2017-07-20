import subprocess
import os
import ConfigParser
import re
from filecmp import dircmp

configs = {}

"""
Reads configuration file called parse_defects4j.cfg
"""
def readConfigurations():
    config = ConfigParser.ConfigParser()
    config.read('parse_defects4j.cfg')
    configs["project"] = config.get("Basic","project")
    configs["projectNum"] = config.get("Basic","projectNum")
    configs["version"] = config.get("Basic","version")
    configs["examplesPath"] = config.get("Basic","examplesPath")
    configs["srcPath"] = config.get("Basic","srcPath")
    configs["copiedFiles"] = config.get("Basic", "copiedFiles")
    configs["projectPath"] = config.get("Basic", "projectPath")

"""
Parses defect4j info command
@return {Dictionary} Keys are file names, Values are file paths.
"""
def defects4jInfo():
    bashCommand = "defects4j info -p " + configs["project"] + " -b " + configs["projectNum"]
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
"""
def checkoutFixedProject():
    bashCommand = "defects4j checkout -p " + configs["project"] + " -v " + configs["projectNum"] + "f -w " + configs["examplesPath"]+configs["projectName"] + configs["projectNum"] + "F"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    configs["fixedPath"] = configs["examplesPath"]+configs["projectName"] + configs["projectNum"] + "F"

"""
Bash copies modified files to Copies directory
@param {List} filePaths: list of relative paths
"""
def copyModifiedFiles(filePaths):
    if not os.path.lexists(configs["projectPath"]):
        os.makedirs(configs["projectPath"])

    for name, path in filePaths.items():
        buggyCommand =   ''.join([
                        "scp ", configs["examplesPath"], 
                        configs["project"].lower(),
                        configs["projectNum"]+"Buggy/", 
                        path,
                        " ",
                        configs["projectPath"], "/",
                        configs["projectNum"], "/",
                        name
                        ])
        fixedCommand =   ''.join([
                        "scp ", configs["fixedPath"] ,"/", 
                        path,
                        " ",
                        configs["projectPath"], "/",
                        configs["projectNum"], "/",
                        name
                        ])

        if not os.path.lexists(configs["projectPath"]+"/"+configs["projectNum"]):
            os.makedirs(configs["projectPath"]+"/"+configs["projectNum"])
        if not os.path.lexists(configs["projectPath"]+"/"+configs["projectNum"]+"/b"):
            os.makedirs(configs["projectPath"]+"/"+configs["projectNum"]+"/b")
        if not os.path.lexists(configs["projectPath"]+"/"+configs["projectNum"]+"/f"):
            os.makedirs(configs["projectPath"]+"/"+configs["projectNum"]+"/f")

        process = subprocess.Popen(buggyCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        process = subprocess.Popen(fixedCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()




readConfigurations()
checkoutFixedProject()
copyModifiedFiles(defects4jInfo())
