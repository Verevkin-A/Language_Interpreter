"""Main program information"""


class Program:
    """Contains code info

    Program class use Singleton pattern,
    so all program instances between all modules
    are the same
    """
    __instance = None

    @staticmethod
    def get_instance():
        if Program.__instance is None:
            Program()
        return Program.__instance

    def __init__(self):
        if Program.__instance is None:
            Program.__instance = self
