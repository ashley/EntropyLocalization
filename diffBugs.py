import subprocess
import ConfigParser
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

"""
Parses defect4j info command
@return {List} filePaths of modified files
"""
def defects4jInfo():
    bashCommand = "defects4j info -p " + project + " -b " + projectNum
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #Parsing default defects4j info command
    fileStrings =  ["%s%s%s" % (srcPath,i[3:].replace('.','/'), ".java") for i in 
                    output.split("--------------------------------------------------------------------------------")
                    [-2].strip('\n').split("\n")[1:]
                    ]
    return fileStrings

"""
Checkout fixed project into Example directory
@param {String} porjectName: name of project from defects4j
@param {String} versionID: number that identified version of project
"""
def checkoutFixedProject(projectName, versionID):
    bashCommand = "defects4j checkout -p " + projectName + " -v " + versionID + "f -w " + examplesPath+projectName + versionID + "F"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

readConfigurations()

