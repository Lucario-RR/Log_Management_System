using Log_Management_System;

/// <summary>
/// C# port of the Python log system. Method and variable names attempt to remain
/// the same as the Python original where practical (e.g. appendMsg, replaceMsg, log_list).
/// </summary>
namespace Log_Management_System_Demo
{
    public static class Program
    {
        public static void Main(string[] args)
        {
            // Initialize log system
            var cfg = new LogConfig(time_zone_offset: 0, max_console_level: 8, max_output_level: 8, program_name: "LMS_Demo", folder_path: "logs");
            var logger = new Log(cfg);

            // Examples
            // Append a debug message (A=8, type 'N' for network, detail 0x0A0)
            var s1 = new StatusCode(8, (byte)'N', 0x0A0);
            logger.appendMsg(new Message(time: DateTimeOffset.UtcNow.ToOffset(cfg.timezone), status_code: s1, msg: "Network initialized."));

            // Append an error message (A=4, type 'D' for db, detail 0x00F)
            var s2 = new StatusCode(4, (byte)'D', 0x00F);
            logger.appendMsg(new Message(time: DateTimeOffset.UtcNow.AddSeconds(1).ToOffset(cfg.timezone), status_code: s2, msg: "DB connection failed."));

            // Replace the second message (index 1)
            var s3 = new StatusCode(5, (byte)'L', 0x010); // WARNING, type C
            var changed = new Message(time: DateTimeOffset.UtcNow.AddSeconds(2).ToOffset(cfg.timezone), status_code: s3, msg: "New message.");
            logger.replaceMsg(0, changed);

            // Export whole log
            logger.export();
        }
    }
}
