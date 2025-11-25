# Log Management System

## Overview
The **Log Management System** is a multi language (Python or C#) logging utility designed to store, manage, and display log messages efficiently. It provides features such as logging messages with different urgency levels, saving logs to a file, and printing them to the console based on configurable settings.

## Features
- Configurable logging settings (timezone, log levels, file storage location)
- Log message management (append, replace, remove)
- Configurable output to console and file
- Use [PSR-3: Logger Interface](https://www.php-fig.org/psr/psr-3/) to identify the importance of a log message
- Introduced **Status Code** which can quickly identify the position of code where output to log (C# feature only for now)
- Ensures log integrity and order via automated sorting based on timestamps and validation

## Status Code
(This is a unique feature on C# version, where Python version will adapt this soon.)

A status code is used to pointing the location of message. It consists a minimum of 5 digits:

Short version: `A B CCC`  
Long version: `A B CCCDD`

| Digit | Value Accepted | Definition |
|-------|----------------|------------|
| A     | 1-9, 0 & A-E reserved for extension| A fixed single integer digit, indicates the level of log message, by using the table above. 9 is used for consol debug only. |
| B     | A-Z | Status code use a single char digit, inticates the category of log message, e.g. network, database connection... |
| CCC    | 0x000-0xFFF | A minimum of 3 digits HEX value, indicates the details of each message means. A maximum of 16^3 = 4096 status may be record under each category. Code may vary across different projects. |
| CCCDD    | 0x00000-0xFFFFF | Optional DD. CCCDD may be used if 3 digits HEX are running out. This extends the total status to 16^5 = 1048576. |

## Status Code in Hex
A Hex version of status code is also available, it is extremely useful when working in languages like C family.

The minumum length of status code **A B CCC** is 6 Hex digits, i.e. 3 bytes.  
The maximum length of **A B CCCDD** is 8 Hex digits, i.e. 4 bytes.

| Digit | Hex Length | Hex Value Accepted |
|-------|------------|--------------------|
| A     | 1 | 0x1-0x9, 0x0 & 0xA-0xE reserved |
| B     | 2 | 0x41-0x5A |
| CCC   | 3 | 0x000-0xFFF|
| CCCDD | 5 | 0x00000-0xFFFFF|

## Status Code Category
This is only suggestion for definition of char in digit B. This may vary across different projects, apart from `L` has been used for this LMS.

| SC | Hex Value | Definition |
|----|-----------|------------|
| A | 0x41 |  |
| B | 0x42 |  |

## Installation and Usage
Please check the corresponding README for Python and C#, as they have different grammar on installation or calling LMS.

Currently C# has slightly extra feature than Python. (C# uses status code where Python only uses log levels)


## File Output Format
We aim to have exactly the same format for output, however due to slightly different features provided on two platforms, this section will be slightly different now.

### Python
Log messages are stored in `logs/[your_program_name]_YYYYMMDD_HHMMSS.log` (default path) in the following format:
```
HH:MM:SS.mmm [LEVEL] Message Content
```
Example:
```
14:30:45.123 [INFO] Application started.
14:32:00.456 [ERROR] Failed to connect to database.
```

### C#
AI is generating

# Reference
## Log Levels
This log system uses [PSR-3: Logger Interface](https://www.php-fig.org/psr/psr-3/) for state log levels, here is a list:
| Level | Name       |
|-------|-----------|
| 1     | EMERGENCY |
| 2     | ALERT     |
| 3     | CRITICAL  |
| 4     | ERROR     |
| 5     | WARNING   |
| 6     | NOTICE    |
| 7     | INFO      |
| 8     | DEBUG     |

# Development log
### v2.0.0 on 25 NOV 2025
- LMS on C# released
- Edit README, add information on Status Code.
- Some of the markdown document is incomplete, will be fixed in next version

### v1.0.0 on 08 FEB 2025
- First stable version released and this README created

---
Developed by **[Github@Lucario-RR](https://github.com/Lucario-RR)** on 08 FEB 2025

