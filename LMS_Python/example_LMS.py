from datetime import datetime as dt
from datetime import timezone,timedelta
import atexit
from log import LogLevel,LogConfig,Message,Log


# Initialize log
config = LogConfig(
    time_zone_offset=0,   # Set your timezone in int
    max_print_level=7,    # Maximum level for print out
    max_output_level=8,   # Maximum level for save to log file
    program_name='TestLOG', # Your Program Name
    folder_path='logs'    # Folder for storing logs
)
log = Log(config)

# While terminate
def normalTermination():
    global log
    log.appendMsg(Message(level=7,msg="Program exit as expected, log file saved!"))

atexit.register(normalTermination)



# Program classes and functions
def menu_ui():
    global log
    log.appendMsg(Message(level=5,msg="Example warning message 1"))
    log.appendMsg(Message(level=8,msg="Example debug message 2"))
    #log.appendMsg(Message(level=7, msg="Info message with user defined time", time=dt(2025,2,8,20,21,00)))
    # Program ends
    exit()



# Program Starts:
menu_ui()
