#!/usr/bin/python3
"""
This module contains the entry point of the command interpreter
"""
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
from models.place import Place
from models.engine.file_storage import FileStorage
import cmd


class HBNBCommand(cmd.Cmd):
    """
    Class that Provides methods for handling cmds in the program CLI
    """
    prompt = "(hbnb) "

    CLASSES = [
            "BaseModel", "User", "State",
            "Amenity", "Place", "City", "Review"
            ]

    def do_create(self, line):
        """
        Creates a new instance of an object

        Usage create <object>
        """
        args = line.split(" ")
        if line == "":
            print("** class name missing **")
        elif line not in HBNBCommand.CLASSES:
            print("** class doesn't exist **")
        else:
            if args[0] == "BaseModel":
                base = BaseModel()
            elif args[0] == "User":
                base = User()
            elif args[0] == "State":
                base = State()
            elif args[0] == "Amenity":
                base = Amenity()
            elif args[0] == "Place":
                base = Place()
            elif args[0] == "City":
                base = City()
            elif args[0] == "Review":
                base = Review()
            print(base.id)
            storage.save()

    def do_show(self, line):
        """
        Prints the string representation of an instance

        Usage: show <object> <id>
        """
        objs = storage.all()
        args = line.split(" ")
        if line == "":
            print("** class name missing **")
        elif args[0] not in HBNBCommand.CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            args[1] = args[1].replace('"', '') \
                    if args[1][0] == '"' else args[1]
            classname_id = args[0] + "." + args[1]
            if classname_id not in objs.keys():
                print("** no instance found **")
            else:
                print(objs[classname_id])

    def do_destroy(self, line):
        """
        Deletes an instance

        Usage: destroy <object> <id>
        """
        objs = storage.all()
        args = line.split(" ")
        if line == "":
            print("** class name missing **")
        elif args[0] not in HBNBCommand.CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            args[1] = args[1].replace('"', '') \
                    if args[1][0] == '"' else args[1]
            classname_id = args[0] + "." + args[1]
            if classname_id not in objs.keys():
                print("** no instance found **")
            else:
                del objs[classname_id]
                storage.save()

    def go_all(self, line):
        """
            Prints all string representation of all instances

            Usage: all <object> | all
        """
        objkt = storage.all()
        args = line.split(" ")
        if args[0] != "":
            if args[0] not in HBNBCommand.CLASSES:
                print("** class doesn't exist **")
            else:
                list_all = []
                for obj in objkt:
                    if obj.startswith(args[0]):
                        list_all.append(str(objkt[obj]))
                print(list_all)
        else:
            list_all = []
            for obj in objkt:
                list_all.append(str(objkt[obj]))
            print(list_all)

    def go_update(self, line):
        """
        Updates an instance by adding or updating attribute

        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        objkt = storage.all()
        args = line.split(" ")
        if line == "":
            print("** class name missing **")
        elif args[0] not in HBNBCommand.CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            args[1] = args[1].replace('"', '') \
                    if args[1][0] == '"' else args[1]
            classname_id = args[0] + "." + args[1]
            if classname_id not in objkt.keys():
                print("** no instance found **")
            elif len(args) < 4:
                print("** value missing **")
            elif len(args) < 3:
                print("** attribute name missing **")
            else:
                args[2] = args[2].replace('"', '').replace("'", "")
                obj = objkt[classname_id]
                if args[3].startswith('"') and args[3].endswith('"') or \
                        args[3].startswith("'") and args[3].endswith("'"):
                    setattr(obj, args[2], str(args[3][1:-1]))
                elif args[3].startswith('"') and not args[3].endswith('"') or \
                        args[3].startswith("'") and not args[3].endswith("'"):
                    strvalue = ""
                    for arg in args[3:]:
                        strvalue += " " + arg
                        if arg.endswith('"') or arg.endswith("'"):
                            break
                    setattr(obj, args[2], str(strvalue[2:-1]))
                elif "." in args[3]:
                    setattr(obj, args[2], float(args[3]))
                else:
                    setattr(obj, args[2], int(args[3]))
                storage.save()

    def go_count(self, line):
        """
            this method Counts the number of objects
        """
        objkt = storage.all()
        args = line.split(" ")
        obj_names = list(map(lambda obj: type(obj).__name__, objkt.values()))
        print("{}".format(obj_names.count(line)))

    def update_mydict(self, command, line):
        x = line.split("{")[1][0:-2].replace(":", "").split(", ")
        for items in x:
            cmmd = command + " " + items
            self.onecmd(cmmd)

    def default(self, line):
        """
        this handles other commands like:
            <class name>.count()
            <class name>.all()
        """
        METHODS = ["all", "count", "show", "destroy", "update"]

        if "." in line:
            command = line[:-1].replace(",", "")\
                    .replace("(", " ").replace(".", " ").split(" ")
            command[0], command[1] = command[1], command[0]
            if command[1] in HBNBCommand.CLASSES and command[0] in METHODS:
                if command[0] == "update" and "{" in line:
                    self.update_mydict(" ".join(command[:3]), line)
                    return None
                self.onecmd(" ".join(command))
                return None
        return cmd.Cmd.default(self, line)

    def go_EOF(self, line):
        """
        End-of-file interpreter

        Usage: CTRL+D
        """
        return True

    def go_quit(self, line):
        """
        also ends the command line interpreter

        Usage: quit
        """
        return True

    def emptyline(self):
        """
        Ignore empty lines (ENTER)
        """
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
