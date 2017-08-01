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
jdk7 = /Library/Java/JavaVirtualMachines/jdk1.7.0_80.jdk/Contents/Home/bin
jdk8 = /Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home/bin
```
#### Questions: what are the copiedFiles and projectPath, and how are they different from the ExamplesPath?

2. Run `SourceCodeAggregation.py`. Make sure directories are already existing
3. Run `DiffSourceCode.py`. You may need to create a directory caleld `DiffCode` first
4. Run `src/clegoues/genprog4java/main/Run.java` from Genprog4Java. Change the hard-coded variables, `examplePath` and `outputPath`.
