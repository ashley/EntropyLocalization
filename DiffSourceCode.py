import subprocess
import os, sys

"""
Prepare directory and file for writing
"""
def prepareFile():
    projectName = raw_input("Enter the project Name: ")
    # File where results are stored
    if not os.path.lexists("DiffCode"):
            os.makedirs("DiffCode")
    fi = open("DiffCode/" + projectName + ".txt", "wb")
    return fi

"""
Preparation before executing diff command.
@param {File} fi: File for appending results
"""
def prepareDirectory(fi):
    diffPath = raw_input("Enter absolute path to aggregated source code directory: ")
    versions = [version for version in os.listdir(diffPath) if version != ".DS_Store"] #filter out default mac files
    for versionDirectory in versions:
        getDiffData(diffPath + "/" + versionDirectory, versionDirectory, fi)

"""
Calls diff command but does checks to make sure files exist
@param {String} versionPath: Absolute path to the version directory
@param {String} versionID: number that is associated with project
@param {File} fi: File for appending results
"""
def getDiffData(versionPath, versionID, fi):
    before_files = [i for i in os.listdir(versionPath + "/b") if i != ".DS_store"]
    after_files = [i for i in os.listdir(versionPath + "/f") if i != ".DS_Store"]
    version_information = {
            "VersionID" : versionID,
            "path" : versionPath,
            "working" : str(len(before_files) == len(after_files)),
            "results" : ""
            }
    bug_information = {}
    count = 0
    if before_files == after_files: #checks if files' b/f versions exist
        for fileName in before_files:
            appendWorkbook(version_information, fi) #helper function, for easy implementation of Excel sheets
            diffCommand = ''.join([
                "diff ", 
                versionPath, "/b/", fileName,  " ",  
                versionPath, "/f/", fileName
                ])
            process = subprocess.Popen(diffCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            bug_information[fileName] = output
            appendWorkbook(bug_information,fi)
            count += 1

"""
Currently writes in a file. Can be modified to be used with OpenPyxl
@param {Dictionary} inputMap: any map with <String,String> for appending to a file
@param {File} fi: File for appending results
"""
def appendWorkbook(inputMap, fi):
    for key, value in inputMap.items():
        fi.write(key + " : " + value + "\n")

"""
To parse output results from diff command. Future implementation
@param {String} result: output string to parse
"""
def parseOutput(result):
    result = result.split("\n")
    result[0]

def main():
    resultFile = prepareFile()
    prepareDirectory(resultFile)

if __name__ == "__main__":
    main()
