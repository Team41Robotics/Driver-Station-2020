from abc import ABC, abstractmethod
import argparse

from .utils import execute_shell_command

class Task(ABC):
    def __init__(self, name, desc):
        """Init a task with a name and a description"""
        self.name = name
        self.desc = desc
        self.group = None

    def set_group(self, group):
        self.group = group

    @abstractmethod
    def add_arguments(self, parser):
        """Add a rule to parse arguments"""

    @abstractmethod
    def run(self, parsed):
        """Define a job this task will do"""


class CommandExecTask(Task):
    def __init__(self, alias, desc, command):
        super().__init__(alias, desc)
        self.command = command

    def add_arguments(self, parser):
        pass

    def run(self, _parsed):
        retval, _ =  execute_shell_command(self.command)
        return retval
