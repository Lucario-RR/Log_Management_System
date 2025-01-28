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
            config: column to return

        Returns:
            pd.Series or pd.DataFrame

        """
        self.log_list = []
        self.config = LogConfig()

    def appendMsg(self,log_msg:Message):
        self.log_list.append(log_msg)
        self.printMsg() # -1 if invalid
        
    def editMsg(self,index:int,new_log_msg:Message):
        self.log_list[index] = new_log_msg
        self.printMsg()

    def exportLog(self):
        pass

    def printMsg(self,index:int=-1):
        if self.config.print_input:
            print(self.log_list[index])

    def sortLog(self):
        pass

    def __str__(self)->str:
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