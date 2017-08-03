## Evaluation of Fault Localization using Entropy for GenProg4Java

### Compare expressions from GenProg4Java to diff expressions from Defects4J
1. Setup a configuration file called `parse_defects4j.cfg` in this repo with this format:
```
[Basic]
project = Chart
projectNum = 26
version = f
examplesPath = /Users/ashleychen/Desktop/reuse/defects4j/ExamplesCheckOut/
srcPath = source/
copiedFiles = /Users/ashleychen/Desktop/EntropyLocalization/Copies
projectPath =  /Users/ashleychen/Desktop/EntropyLocalization/Copies/Chart
genprogPath = /Users/ashleychen/Documents/workspace/GenProg4Java
jdkSeven = /Library/Java/JavaVirtualMachines/jdkEight1.7.0_80.jdkEight/Contents/Home/bin
jdkEight = /Library/Java/JavaVirtualMachines/jdkEight1.8.0_101.jdkEight/Contents/Home/bin
grammarModelPath = /Users/ashleychen/Desktop/models
```
#### Questions: what are the copiedFiles and projectPath, and how are they different from the ExamplesPath?
#### Specifications:
Attribute | Details
--- | ---
project | Name of project
projectNum | VersionID of project
version | Either b or f
examplesPath | A directory which the script will dump projects in from Defects4J. Create the directory beforehand. 
srcPath | Any additional path that leads to source code files from the project directory
copiedFiles | A directory where multiple project directories will be stored. Create the directory beforehand.
projectPath | The path from copiedFiles to the project directory. Time, Lang, and Math uses src/main/java
genprogPath | Absolute path to where GenProg is located
jdkSeven | Absolute path to where Java 7 is located
jdkEight | Absolute path to where Java 8 is lcoated
grammarModelPath | A directory to where models are located. Create the directory beforehand

2. Run `SourceCodeAggregation.py`. Make sure directories are already existing
3. Run `DiffSourceCode.py`. You will need to manually input the name of the Project and where the directory from `SourceCodeAggregation.py` is located. *Note: Dragging paths to terminal may automatically make a space after the path. Make sure the input is just the path string and there are no spaces*
4. Run `src/clegoues/genprog4java/main/Run.java` from Genprog4Java. Change the hard-coded variables, `examplePath` and `outputPath`.
