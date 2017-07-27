import subprocess
import os, sys

def prepareDirectory():
    examplePath = raw_input("Enter absolute path to checkedout directory: ")
    projectName = raw_input("Enter the project name: ")
    limit = int(raw_input("Enter bug input: "))
    for version in range(limit):
        JARCommand = ''.join([
            "java -jar GenProg_Probability.jar ",
            examplePath, "/", projectName.lower(), str(version), "Buggy",
            "/defects4j.config"
            ])
        print "COMMAND: " + JARCommand
        process = subprocess.Popen(JARCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        saveResults(output,str(version),projectName)

def saveResults(results, bugID, projectName):
    if not os.path.lexists(projectName+"_Names"):
        os.makedirs(projectName+"_Names")
    fi = open(projectName+"_Names""/"+projectName+"_Names" + bugID + ".txt",'wb')
    fi.write(results)

def main():
    prepareDirectory()

main()
