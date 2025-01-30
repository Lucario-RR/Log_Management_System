from datetime import datetime as dt

class LogConfig:
    def __init__(self):
        # I/O
        self.print_input = False
        self.max_print_level = 8
        self.file_path = 'logs/'
        self.timezone = ''
        # Processing

        # General
        self.timezone = 0


class LogLevel:
    def __init__(self,level:int):
        """
        A class which stores level of log message, output level as string while print out

        Args:
            level: an int value representing urgent levels

        Level indication:
            1: Emergency
            2: Alert
            3: Critical
            4: Error
            5: Warning
            6: Notice
            7: Informational
            8: Debug

        Ref:
            PSR-3: Logger Interface https://www.php-fig.org/psr/psr-3/
        """
        self.log_level = level

    def __str__(self)->str:
        """
        Output level as string while print out

        Returns:
            Each level in string
        """
        if self.log_level == 1:
            return("EMERGENCY")
        elif self.log_level == 2:
            return("ALERT")
        elif self.log_level == 3:
            return("CRITICAL")
        elif self.log_level == 4:
            return("ERROR")
        elif self.log_level == 5:
            return("WARNING")
        elif self.log_level == 6:
            return("NOTICE")
        elif self.log_level == 7:
            return("INFO")
        elif self.log_level == 8:
            return("DEBUG")



class Message:
    def __init__(self,time:dt=dt.now(),level:int=7,msg:str=""):
        """
        One line of log message, minimum unit of Class Log

        Args:
            time: Time of this message, default time now
            level: Urgency of this line, default 7
            msg: message content, default ""

        Example:
        Message(level=8,msg="Message Content")
        2025-01-01 00:00:00.000 [DEBUG] Message Content
        """
        self.time = time 
        self.level = LogLevel(level)
        self.msg = msg

    def changeTime(self,new_time:dt=dt.now()):
        """
        Change the time of an exist line

        Args:
            new_time: new time in datetime
        """
        self.time = new_time

    def changeLevel(self,new_level:int=7):
        """
        Change the urgency of an exist line

        Args:
            new_level: new target level
        """
        self.level.log_level = new_level

    def changeMsg(self,new_msg:str=""):
        """
        Change the message content of an exist line

        Args:
            new_msg: new message
        """
        self.msg = new_msg

    def __str__(self)->str:
        """
        Output formated message with time HH:MM:SS.xxx

        Returns:
            1 log message in format
        """
        return f"{self.time.strftime("%H:%M:%S.%f")[:-3]}[{self.level}] {self.msg}" # [:-3] used to take first 3 digit of microsecond



class Log:
    def __init__(self):
        """
        Log class conbines every log message and has some basic methods to do

        Args:
            log_list: a list of Class Message

        Returns:
            pd.Series or pd.DataFrame

        """
        self.log_list = []
        self.config = LogConfig()

    def appendMsg(self,log_msg:Message):
        """
        Add a new log message to Log

        Args:
            log_msg: One line of log message in Class Message frmat
        """
        self.log_list.append(log_msg)
        self.afterOperation()
        
    def replaceMsg(self,index:int,new_log_msg:Message):
        """
        Replace the message at index position with a new message of data type Class Message
        
        Args:
            index: Identify which line to be replaced
            new_log_msg: New message in data type Class Message
        """
        self.log_list[index] = new_log_msg
        self.afterOperation(index)

    def removeMsg(self,index:int):
        """
        Remove the log message at index line

        Args:
            index: Identify which line to be removed
        """
        self.log_list.pop(index)
        # Save after removing
        self.export()
    
    def afterOperation(self,index:int=-1):
        """
        Does everything after append, modify message
        
        Args:
            index: Identify line to perform print, check order, default -1
        """
        # Print Message
        self.printMsg(index)
        # Check order
        if self.checkOrder(index):
            # Save if in order
            self.save()
        else:
            # Sort and export if not in order
            self.sort()
            self.export()

    def printMsg(self,index:int=-1):
        """
        Print last log message if required in Class Config

        Args:
            index: Identify which line to be printed, default -1
        """
        if self.config.print_input:
            print(self.log_list[index])

    def checkOrder(self,index:int)->bool:
        """
        Check if append message is in time order. Default check one line before and after.

        Arg:
            index: Identify position to check, set 0 to check everything
        """
        if index == 0:
            # Check everything
            if self.sort():
                pass
                ### Show sorted already
            else:
                ### Show now sorted
                pass
        else:
            # Check if reach two end
            # And handling edges
            # Check front and last
            pass

    def sort(self)->bool:
        """
        Check if sorted, if not sort it by datetime using built in function
        Return True or False to indicate sorted already

        Returns:
            True or False
        """
        # Pre-sort the list
        temp = sorted(self.log_list, key=lambda line:line.time)
        
        # If sorted
        if self.log_list == temp:
            return True
        # If not sorted, add pre-sorted to it
        else:
            self.log_list = temp
            return False
        

    def save(self):
        """
        Save the last message to system, used when a new line has append
        """
        try:
            with open(self.config.file_path,'a') as file:
                file.append(f"{self.log_list[-1]}\n")
        except FileExistsError:
            ### Raise file error
            pass

    def export(self):
        """
        Save the whole log to file, used when message in the middle has modified
        """
        try:
            with open(self.config.file_path,'w') as file:
                for msg in self.log_list:
                    file.append(f"{msg}\n")
        except FileExistsError:
            ### Raise file error
            pass

    def __str__(self)->str:
        """
        Output one message per line

        Returns:
            1 log message per line for all log messages
        """
        return "\n".join(self.log_list)



"""
For a log it can:

Configs:

"""
"""
    Introduction

    Args:
        data: intraday data
        col: column to return

    Returns:
        pd.Series or pd.DataFrame
    
    Examples:

"""