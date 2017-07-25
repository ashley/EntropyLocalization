import subprocess
import os, sys

# File where results are stored
fi = open("Results.txt", "wb")

"""
Preparation before executing diff command.
"""
def prepareDirectory():
    diffPath = raw_input("Enter absolute path to aggregated source code directory: ")
    versions = [version for version in os.listdir(diffPath) if version != ".DS_Store"] #filter out default mac files
    for versionDirectory in versions:
        getDiffData(diffPath + "/" + versionDirectory, versionDirectory)

"""
Calls diff command but does checks to make sure files exist
@param {String} versionPath: Absolute path to the version directory
@param {String} versionID: number that is associated with project
"""
def getDiffData(versionPath, versionID):
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
            appendWorkbook(version_information) #helper function, for easy implementation of Excel sheets
            diffCommand = ''.join([
                "diff ", 
                versionPath, "/b/", fileName,  " ",  
                versionPath, "/f/", fileName
                ])
            process = subprocess.Popen(diffCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            bug_information[fileName] = output
            appendWorkbook(bug_information)
            count += 1

"""
Currently writes in a file. Can be modified to be used with OpenPyxl
@param {Dictionary} inputMap: any map with <String,String> for appending to a file
"""
def appendWorkbook(inputMap):
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
    prepareDirectory()

