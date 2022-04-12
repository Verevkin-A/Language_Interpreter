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
## Arguments processing
At the execution beginning, provided interpret arguments are collected
and validated. For arguments collection was used python library `argparse`.
Given input and source files were checked for existence 
and sufficient reading rights

## XML processing

## Program evaluation

# Testing suit

## Arguments processing

## Test cases searching

## Test cases execution

## Building html with results
