# Installation and Usage Instruction for Python

## Installation
Simpily download `log.py` file in repository and leave it in your own project folder.  
You may also clone or download the repository:
```bash
$ git clone https://github.com/your-repo/Log_Management_System.git
```

## Usage
### 1. Initialize
You may use `example.py` template in the repository or use following code to setup log system:
```python
from log_system import LogConfig, Log, Message

config = LogConfig(
    time_zone_offset=0,   # Set your timezone in int
    max_print_level=7,    # Maximum level for print out
    max_output_level=8,   # Maximum level for save to log file
    program_name='MyApp', # Your Program Name
    folder_path='logs'    # Folder for storing logs
)
log = Log(config)
```
Note that for `max_print_level` and `max_output_level`, the int value you may refer to reference part at the end of documentation.

I am strongly recommend you importing `datetime` module, as this may be helpful to add message with a given time.
```python
from datetime import datetime as dt
```
If you wish to indicate a message after program finished normally (e.g. not killed), you may add following code at initialize section:
```Python
import atexit

# While terminate
def normalTermination():
    global log
    log.appendMsg(Message(level=7,msg="Program exit as expected, log file saved!"))

atexit.register(normalTermination)
```

### 2. Add Log Messages
Examples on adding messages, time value will be the moment adding message:
```python
log.appendMsg(Message(level=8, msg="Debugging application"))
log.appendMsg(Message(level=4, msg="An error occurred!"))
```

You may also bring a timestamp for message rather than now:
```Python
log.appendMsg(Message(level=7, msg="Info message with user defined time", time=dt(2025,2,8,20,21,00)))
```

Please remember to global log if you are using inside a function:
```Python
def menu():
    global log
```

### 3. Replace Log Messages
You may edit a message's level or content directly.  
But I would suggest replacing with a new Message:
```python
log.replaceMsg(1, Message(level=5, msg="Updated warning message"))
#Parameter: (position index to replace, Message)
```

### 4. Remove Log Messages
```Python
log.removeMsg(0)  # Provide int index
```

### 5. Save Logs
Logs are automatically saved. You may manually export all logs just in case:
```python
log.export()
```