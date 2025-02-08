from datetime import datetime as dt
from datetime import timezone,timedelta
import atexit
from log import LogConfig,Message,Log


# Initialize log
config = LogConfig(time_zone_offset=0,max_print_level=7,max_output_level=8,program_name='TestLOG',folder_path='logs')
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
    
    # Program ends
    exit()



# Program Starts:
menu_ui()
