import subprocess
import os, sys

fi = open("Results.txt", "wb")

def prepareDirectory():
    diffPath = raw_input("Enter absolute path to aggregated source code directory: ")
    versions = [version for version in os.listdir(diffPath) if version != ".DS_Store"] #filter out default mac files
    for versionDirectory in versions:
        getDiffData(diffPath + "/" + versionDirectory, versionDirectory)

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
    if before_files == after_files:
        for fileName in before_files:
            appendWorkbook(version_information)
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

def appendWorkbook(inputMap):
    for key, value in inputMap.items():
        fi.write(key + " : " + value + "\n")

def parseOutput(result):
    result = result.split("\n")
    result[0]

def main():
    prepareDirectory()

main()
