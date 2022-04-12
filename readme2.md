Documentation of Project Implementation for 2 task of IPP 2021/2022<br/>
Name and surname: Aleksandr Verevkin<br/>
Login: xverev00<br/>

## OOP and design patterns (NVI extension)
Both interpretation and testing suit were designed applying 
**O**bject-**O**riented **P**rograming. 
All parts of the programs were treated as individual objects(classes)
which inherit and communicate with each other.

XML interpretation using *structural design pattern* `Facade` 
that provide unified interface
for subsystem interfaces and reduce overall complexity of the system.
The `Facade` pattern also simplify interpret subsystem for 
future customization and maintenance.

In addition, for general program instance(frames, stacks and counters information) 
was used *creational design pattern* `Singleton`
over global variables. The `Singleton` pattern allows single program instance
to share between all other classes, which making system easier for
implementing, understanding and future maintaining. <br/>
####Singleton implementation:
```python
class Program:
    __instance = None
    @staticmethod
    def get_instance():
        if Program.__instance is None:
            Program()
        return Program.__instance
    
    def __init__(self):
        Program.__instance = self
```

# Interpret
All interpret parts were treated as different subsystems, 
which were unified in facade class, 
applying `Facade` design pattern architecture.
- ## Arguments processing
At the execution beginning, provided interpret arguments are collected
and validated. For arguments collection was used python module `argparse`.
Given input and source files were checked for existence 
and sufficient reading permissions.

- ## XML processing
After the arguments have been collected, all elements with instructions and 
corresponding arguments are picked, validated and sorted from the 
provided XML source file. To simplify searching in XML document, 
was used python module `xml.etree.ElementTree`.

- ## Program evaluation
When all instructions and labels are saved, program execution can start.
All frames, stacks and counters are initialized in the `Singleton` program instance.
Instructions one by one are evaluated and processed.

# Testing suit

- ## Arguments processing
The script arguments are processed first. File paths are validated for 
existence and sufficient rights to read and execute. Optional parameters 
are set and checked for forbidden combinations. For easier arguments processing
was used php function `getopt`.

- ## Test cases searching and execution
After all arguments have been saved, in the chosen or set by default directory
searching for tests is started. Depending on the `--recursive` parameter,
subdirectories are also checked for tests. Each found test case is 
saved into array as `TestItem` object.

Array with tests is looped trough. Each saved test case is evaluated.
Tests return codes and outputs are saved for future reference.

- ## Building html with results
Class `CreateHTML` is responsible for creating and saving output html/css file 
with test results. For each test result is created a row with all needed information 
from the test case for debugging possibility. Output page is made using 
php built-in `DOM(Document Object Model)` parser.
