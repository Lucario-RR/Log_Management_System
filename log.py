from datetime import datetime as dt
from datetime import timezone,timedelta
import os

class LogConfig:
    def __init__(self,time_zone_offset:int=0,max_print_level:int=8,max_output_level:int=8,program_name:str='',folder_path:str='logs'):
        """
        A class of all the configs

        Args:
            time_zone_offset: int value of timezone
            max_print_level: indicate the max level of message to show in command line
            max_output_level: indicate the max level of message to save to file
            program_name: name of your project/program, used for create log file name
            folder_path: path for storing logfiles
        
        Public Variables:
        self.timezone
        self.max_print_level
        self.max_output_level
        self.program_name
        self.folder_path
        self.file_path
        self.__print__
        """

        # General
        self.timezone = timezone(timedelta(hours=time_zone_offset))

        # I/O
        self.max_print_level = max_print_level
        self.max_output_level = max_output_level
        self.program_name = program_name
        self.folder_path = folder_path
        self.file_path = f"{self.folder_path}/[{self.program_name}]{dt.now(self.timezone).strftime('%Y%m%d_%H%M%S')}.log"
        os.makedirs(self.folder_path, exist_ok=True) # Create the folder if itdoesn't exist
    
    def __str__(self)->str:
        pass



class LogLevel:
    def __init__(self,level:int):
        """
        A class which stores level of log message, output level as string while print out

        Args:
            level: an int value representing urgent levels

        Private Variables and Methods:
            intLogLevel(self)->int
            self.__log_level
            self.__level_mapping
            __str__(self)->str

        Ref:
            PSR-3: Logger Interface https://www.php-fig.org/psr/psr-3/
        """
        self.log_level = level
        self.__level_mapping = {
            1: "EMERGENCY",
            2: "ALERT",
            3: "CRITICAL",
            4: "ERROR",
            5: "WARNING",
            6: "NOTICE",
            7: "INFO",
            8: "DEBUG",
        }

    def intLevel(self)->int:
        """
        Output level as int for comparing levels

        Returns:
            log_level in int
        """
        return self.log_level

    def __str__(self)->str:
        """
        Output level as string while print out

        Returns:
            Each level in string
        """
        return self.__level_mapping[self.log_level]



class Message:
    def __init__(self,time:dt=dt.now(),level:int=7,msg:str=""):
        """
        One line of log message, minimum unit of Class Log

        Args:
            time: Time of this message, default time now
            level: Urgency of this line, default 7
            msg: message content, default ""

        Public Variables and Methods:
            changeTime(self,new_time:dt=dt.now())
            changeLevel(self,new_level:int=7)
            changeMsg(self,new_msg:str="")

        Private Variables and Methods:


        Call Example:
        Message(level=8,msg="Message Content 1")
        2025-01-01 00:00:00.000 [DEBUG] Message Content 1
        Message(level=5,msg="Message Content 2")
        2025-01-01 00:00:00.000 [WARNING] Message Content 2
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
        return f"{self.time.strftime('%H:%M:%S.%f')[:-3]}[{self.level}] {self.msg}" # [:-3] used to take first 3 digit of microsecond



class Log:
    def __init__(self,config:LogConfig):
        """
        Log class conbines every log message and has some basic methods to do

        Args:
            config: initialized configs with Class LogConfig

        Public Variables and Methods:
            self.log_list
            self.config
            appendMsg(self,log_msg:Message)
            replaceMsg(self,index:int,new_log_msg:Message)
            removeMsg(self,index:int)
            printMsg(self,index:int=-1)
            export(self)

        Private Variables and Methods:
            __afterOperation(self,index:int=-1)
            __checkOrder(self,index:int)->bool
            __sort(self)->bool
            __save(self)
            __str__(self)->str
        """
        self.log_list = []
        self.config = config

    def appendMsg(self,log_msg:Message):
        """
        Add a new log message to Log

        Args:
            log_msg: One line of log message in Class Message frmat
        """
        self.log_list.append(log_msg)
        self.__afterOperation()
        
    def replaceMsg(self,index:int,new_log_msg:Message):
        """
        Replace the message at index position with a new message of data type Class Message
        
        Args:
            index: Identify which line to be replaced
            new_log_msg: New message in data type Class Message
        """
        self.log_list[index] = new_log_msg
        self.__afterOperation(index)

    def removeMsg(self,index:int):
        """
        Remove the log message at index line

        Args:
            index: Identify which line to be removed
        """
        self.log_list.pop(index)
        # Save after removing
        self.export()
    
    def __afterOperation(self,index:int=-1):
        """
        Does everything after append, modify message
        1. Print message
        2. Check order and sort if needed
        3. Save / Export on demand
        
        Args:
            index: Identify line to perform print, check order, default -1
        """
        # Print Message
        self.printMsg(index)
        # Check order
        if self.__checkOrder(index):
            # Save if in order
            self.__save()
        else:
            # Export if not in order
            self.export()

    def printMsg(self,index:int=-1):
        """
        Print last log message if required in Class Config

        Args:
            index: Identify which line to be printed, default -1
        """
        if self.log_list[index].level.log_level <= self.config.max_print_level:
            print(self.log_list[index])

    def __checkOrder(self,index:int)->bool:
        """
        Check if append message is in time order. Default check one line before and after.
        If sorted, return True
        If not sorted, sort it and return False

        Arg:
            index: Identify position to check, set 0 to check everything
        """
        if index == 0:
            # Check everything
            if self.__sort():
                return True
            else:
                return False
        # Return True if only one item
        elif len(self) == 1:
            return True
        else:
            # If n-1 <= n
            if self.log_list[index-1].time <= self.log_list[index].time:
                try:
                    # AND NOT n+1 < n
                    if self.log_list[index+1].time < self.log_list[index].time:
                        self.__sort()
                        return False
                # For cases that index item not found
                except IndexError:
                    pass
                # AND n+1 < n
                return True
            # If n-1 > n, False
            else:
                self.__sort()
                return False

    def __sort(self)->bool:
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
        
    def __save(self):
        """
        Save the last message to system, used when a new line has append
        """
        if self.log_list[-1].level.log_level <= self.config.max_output_level:
            try:
                with open(self.config.file_path,'a') as file:
                    file.write(f"{self.log_list[-1]}\n")
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
                    if msg.level.log_level <= self.config.max_output_level:
                        file.write(f"{msg}\n")
        except FileExistsError:
            ### Raise file error
            pass

    def __str__(self)->str:
        """
        Output one message per line

        Returns:
            1 log message per line for all log messages
        """
        if len(self.log_list) == 0:
            return "Empty log!"
        return "\n".join(str(msg) for msg in self.log_list)
    
    def __len__(self)->int:
        return len(self.log_list)



# Testing 
# Initialize
config = LogConfig(time_zone_offset=0,max_print_level=7,max_output_level=7,program_name='TestLOG',folder_path='logs')
log = Log(config)
log.appendMsg(Message(level=5,msg="Message Content 1",time=dt(2025,1,1,12,0,0)))
print("1")
print(log)
log.appendMsg(Message(level=5,msg="Message Content 2",time=dt(2025,1,1,14,0,0)))
print("2")
print(log)
log.appendMsg(Message(level=5,msg="Message Content 3",time=dt(2025,1,1,13,0,0)))
print("3")
print(log)
print(len(log))

"""
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