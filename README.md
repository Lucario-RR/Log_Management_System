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

| SC Sufix | Hex Value | Definition |
|----------|-----------|------------|
| A | 0x41 | Application & Logic |
| B | 0x42 | Background Processing |
| C | 0x43 | Core |
| D | 0x44 | Data |
| E | 0x45 |  |
| F | 0x46 | Files (I/O) |
| G | 0x47 |  |
| H | 0x48 |  |
| I | 0x49 |  |
| J | 0x50 |  |
| K | 0x51 |  |
| L | 0x52 | Logs LMS |
| M | 0x53 |  |
| N | 0x54 | Network |
| O | 0x55 | Observability |
| P | 0x56 |  |
| Q | 0x57 |  |
| R | 0x58 |  |
| S | 0x59 | Security, Serialization |
| T | 0x60 | Testing |
| U | 0x61 | User Interaction GUI/CLI |
| V | 0x62 |  |
| W | 0x63 |  |
| X | 0x64 |  |
| Y | 0x65 |  |
| Z | 0x66 |  |


### **1. Core System / Infrastructure** `C`

* Dependency Injection
* Configuration
* Configuration Hot Reload
* Environment Manager
* Logging
* Error Handling
* Secrets Manager
* Feature Flags
* Versioning
* Licensing
* Installer / Updater


### **2. Networking & Communication** `N`

* Network
* API Layer
* Messaging
* Event Bus
* Messaging Protocols
* Notifications
* Webhooks (implicit under messaging)
* Load Balancer
* Rate Limiter
* Connection Pooling
* Retry / Circuit Breaker


### **3. Data & Storage** `D`
#### Database `D1xx`

#### File IO `D2xx`
* 21x = Filesystem Availability
* 22x = Data Integrity
* 23x = Disk/Device
* 24x = Permissions / Security
* 25x = Path / Structure
* 26x = I/O Operations
* 27x = Metadata / Attributes
* 28x = Lifecycle / Success
* 29x = Low-level Debug / Syscall

| SC Value  | Hex Value | Definition                                      | Template                                                                           | Notes                  |
| --------- | --------- | ----------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------- |
| **1D210** | 0x144210  | Filesystem unavailable / mount lost             | `Filesystem unavailable: mount {mount} inaccessible; path={path}; reason={reason}` | Service unusable       |
| **1D220** | 0x144220  | Hardware failure / disk failure                 | `Disk failure detected on {device}; affected={paths}`                              | Requires human action  |
| **1D230** | 0x144230  | Massive corruption / ransomware indicator       | `Mass corruption detected; affected={paths}; user={user}`                          | Catastrophic           |
| **2D221** | 0x244221  | Integrity compromised (multiple checksum fails) | `Integrity check failed for {path}; expected={expected}; actual={actual}`          | Action needed          |
| **2D231** | 0x244231  | Storage quota exceeded (critical)               | `Quota exceeded on {volume}; used={used}; limit={limit}`                           | Blocking new writes.   |
| **2D240** | 0x244240  | Unauthorized mass access                        | `Unauthorized access to {directory} by {actor}; count={count}`                     | Security risk          |
| **3D212** | 0x344212  | Filesystem corruption detected                  | `Filesystem corruption at {path}; error={error_code}`                              | Severe degradation     |
| **3D260** | 0x344260  | Unrecoverable write failure / data loss         | `Unrecoverable write failure to {path}; bytes={bytes}; errno={errno}`              | Data lost              |
| **3D261** | 0x344261  | DB file I/O critical                            | `DB I/O failure on {db_path}; op={operation}; errno={errno}`                       | Critical system file   |
| **4D250** | 0x444250  | File not found                                  | `File not found: {path}; caller={caller}`                                          | Common error           |
| **4D240** | 0x444240  | Permission denied                               | `Permission denied on {path}; user={user}; mode={mode}`                            | Authentication issue   |
| **4D232** | 0x444232  | No space left on device                         | `Write failed: no space left; path={path}; required={bytes}`                       | Critical but expected  |
| **4D262** | 0x444262  | I/O exception                                   | `I/O error {op} {path}; errno={errno}; reason={reason}`                            | Generic I/O fail       |
| **4D263** | 0x444263  | I/O timeout                                     | `{operation} timeout at {path}; duration={duration}s`                              | Slow storage           |
| **4D251** | 0x444251  | Invalid path / filename too long                | `Invalid path: {path}; max={max_length}`                                           | Bad input              |
| **4D252** | 0x444252  | Symlink loop or broken link                     | `Symlink error at {path}; reason={reason}`                                         | Path error             |
| **4D233** | 0x444233  | Write attempted on read-only filesystem         | `Write denied on read-only FS; path={path}; mount={mount}`                         | Misconfigured FS       |
| **5D260** | 0x544260  | Partial read/write                              | `Partial {operation} for {path}: expected={expected} got={actual}`                 | Non-fatal              |
| **5D234** | 0x544234  | Disk nearly full                                | `Disk usage high on {volume}: {pct}% used`                                         | Warning before failure |
| **5D241** | 0x544241  | Weak permissions                                | `Weak permissions on {path}: mode={mode}`                                          | Security soft issue    |
| **5D253** | 0x544253  | Deprecated path/API used                        | `Deprecated API used for {path}; removal={version}`                                | Maintenance            |
| **5D222** | 0x544222  | Checksum mismatch (non-critical)                | `Checksum mismatch: {path}; expected={expected}; actual={actual}`                  | Optional data          |
| **5D235** | 0x544235  | Inode pool nearly full                          | `High inode usage on {volume}: {used}/{total}`                                     | Host-level warning     |
| **5D236** | 0x544236  | NFS/SMB latency                                 | `Network FS latency high for {path}; rtt={ms}ms`                                   | Network FS issue       |
| **6D280** | 0x644280  | File created                                    | `File created: {path}; size={bytes}; by={user}`                                    | Normal event           |
| **6D261** | 0x644261  | Large file op completed                         | `{operation} complete: {path}; size={bytes}`                                       | Notice-level           |
| **6D270** | 0x644270  | Permission changed                              | `Permissions changed: {path}; from={old} to={new}`                                 | Audit                  |
| **6D281** | 0x644281  | File archived / rotated                         | `Rotated {path} → {archive}`                                                       | Log rotation           |
| **7D260** | 0x744260  | Read success                                    | `Read {bytes} bytes from {path} in {duration_ms}ms`                                | Routine                |
| **7D261** | 0x744261  | Write success                                   | `Wrote {bytes} bytes to {path}`                                                    | Routine                |
| **7D262** | 0x744262  | File opened                                     | `Opened {path} for {mode}; fd={fd}`                                                | Routine                |
| **7D263** | 0x744263  | File closed                                     | `Closed fd={fd} for {path}`                                                        | Audit                  |
| **7D282** | 0x744282  | File renamed                                    | `Renamed {old} → {new}`                                                            | Lifecycle              |
| **7D283** | 0x744283  | Symlink created                                 | `Symlink {link} → {target}`                                                        | Lifecycle              |
| **8D260** | 0x844260  | Detailed I/O trace                              | `{operation} at offset={offset} bytes={bytes}; path={path}`                        | Development            |
| **8D261** | 0x844261  | Syscall return + errno                          | `syscall {call} returned {ret}; errno={errno}`                                     | Low-level debugging    |
| **8D262** | 0x844262  | FD table snapshot                               | `FDTABLE: open_fds={count}`                                                        | Diagnostics            |
| **8D263** | 0x844263  | Lock contention details                         | `Lock contention on {path}; holder={pid} waiters={count}`                          | Debugging              |
| **8D264** | 0x844264  | Buffer flush diagnostics                        | `Flush buffer for {path}: size={size}`                                             | Low-level              |



* ORM / Data Access
* Migrations
* Storage (Local/Cloud)
* Temporary Storage
* Data Pipeline
* Data Transformation
* Data Validation
* Backup / Restore
* Search Index
* Transaction Manager


### **4. Security**

* Security
* Authentication
* Authorization
* Encryption
* Permissions
* Input Sanitization (under security)
* Session Management


### **5. Serialization / Data Formats**

* Serialization (JSON/XML/Proto/etc.)
* Parsing
* Compression


### **6. Application Logic** `A`

* Business Logic
* Domain Models
* Validation
* Rules Engine
* Workflow Engine
* State Machine


### **7. Execution & Performance**

* Threading
* Concurrency Controls
* Memory Management
* Profiling
* Resource Manager
* Asset Loader


### **8. Background Processing** `B`

* Background Jobs
* Scheduler
* Queue Processing
* Batch Processing


### **9. Observability**

* Monitoring
* Metrics
* Tracing
* Health Checks
* Crash Reporter
* Telemetry
* Debugging Tools


### **10. User Interaction** `U`

* UI
* CLI
* Localization
* Reporting
* Analytics


### **11. Build / Deployment / DevOps**

* Build System
* Deployment
* Containerization
* CI/CD (under deployment)


### **12. Testing** `T`

* Testing
* Unit Tests
* Integration Tests
* Mocking
* Test Data Generation


### **13. Extra / Advanced Modules**

* Machine Learning Module
* Simulation Engine




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

