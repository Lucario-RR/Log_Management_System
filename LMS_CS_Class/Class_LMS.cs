using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;

namespace Log_Management_System
{
    public class LogConfig
    {
        public TimeSpan timezone;
        public int max_console_level;
        public int max_output_level;
        public string program_name;
        public string folder_path;
        public string file_path;

        public LogConfig(int time_zone_offset = 0, int max_console_level = 8, int max_output_level = 8, string program_name = "", string folder_path = "logs")
        {
            this.timezone = TimeSpan.FromHours(time_zone_offset);
            this.max_console_level = max_console_level;
            this.max_output_level = max_output_level;
            this.program_name = program_name ?? "";
            this.folder_path = folder_path ?? "logs";

            Directory.CreateDirectory(this.folder_path);
            string stamp = DateTimeOffset.UtcNow.ToOffset(this.timezone).ToString("yyyyMMdd_HHmmss", CultureInfo.InvariantCulture);
            this.file_path = Path.Combine(this.folder_path, $"[{this.program_name}]{stamp}.log");
        }

        public override string ToString()
        {
            return $"LogConfig(tz={this.timezone}, max_console_level={this.max_console_level}, max_output_level={this.max_output_level}, program_name={this.program_name}, file_path={this.file_path})";
        }
    }

    // StatusCode class
    public class StatusCode
    {
        public int A { get; private set; }
        public byte B { get; private set; }
        public uint Detail { get; private set; }

        public StatusCode(int a, byte b, uint detail)
        {
            if (a < 0 || a > 0xF) throw new ArgumentOutOfRangeException(nameof(a), "A must fit 1 hex digit (0x0-0xF).");
            this.A = a;
            this.B = b;
            this.Detail = detail;
        }

        public static StatusCode ParseHex(string hex)
        {
            if (hex == null) throw new ArgumentNullException(nameof(hex));
            string h = hex.Trim().Replace(" ", "").Replace("0x", "").Replace("0X", "");
            if (h.Length < 6)
            {
                throw new FormatException("Status code hex too short. Expect A(1)+B(2)+detail(>=3 hex digits).");
            }

            int a = Convert.ToInt32(h.Substring(0, 1), 16);
            byte b = Convert.ToByte(h.Substring(1, 2), 16);
            string detailHex = h.Substring(3);
            uint detail = Convert.ToUInt32(detailHex, 16);

            return new StatusCode(a, b, detail);
        }

        public string ToHexString()
        {
            int detailDigits = 3;
            if (this.Detail > 0xFFF) detailDigits = 5;
            string detailHex;
            if (this.Detail <= 0xFFF) detailHex = this.Detail.ToString("X3", CultureInfo.InvariantCulture);
            else if (this.Detail <= 0xFFFF) detailHex = this.Detail.ToString("X4", CultureInfo.InvariantCulture);
            else detailHex = this.Detail.ToString("X5", CultureInfo.InvariantCulture);

            return $"{this.A:X1}{this.B:X2}{detailHex}";
        }

        public string ToDisplayString()
        {
            string detailPart;
            if (this.Detail <= 0xFFF) detailPart = this.Detail.ToString("X3", CultureInfo.InvariantCulture);
            else if (this.Detail <= 0xFFFF) detailPart = this.Detail.ToString("X4", CultureInfo.InvariantCulture);
            else detailPart = this.Detail.ToString("X5", CultureInfo.InvariantCulture);

            char maybeChar = (char)this.B;
            bool printable = this.B >= 32 && this.B <= 126;

            string bPart = printable ? maybeChar.ToString() : this.B.ToString("X2");
            return $"{this.A:X1}{bPart}{detailPart}";
        }

        public int GetLevelA()
        {
            return this.A;
        }

        public override string ToString()
        {
            return ToHexString();
        }
    }

    public class Message
    {
        public DateTimeOffset time;
        public StatusCode status_code;
        public string msg;

        public Message(DateTimeOffset? time = null, StatusCode status_code = null, string msg = "")
        {
            this.time = time ?? DateTimeOffset.UtcNow;
            if (status_code == null)
            {
                status_code = new StatusCode(7, (byte)'L', 0x000);
            }
            this.status_code = status_code;
            this.msg = msg ?? "";
        }

        public void changeTime(DateTimeOffset? new_time = null)
        {
            this.time = new_time ?? DateTimeOffset.UtcNow;
        }

        public void changeStatusCode(StatusCode new_status)
        {
            this.status_code = new_status;
        }

        public void changeMsg(string new_msg = "")
        {
            this.msg = new_msg ?? "";
        }

        public void changeLevel(int new_level)
        {
            this.status_code = new StatusCode(new_level, this.status_code.B, this.status_code.Detail);
        }

        public override string ToString()
        {
            string timeStr = this.time.ToOffset(this.time.Offset).ToString("yyyy-MM-dd HH:mm:ss.fff", CultureInfo.InvariantCulture);
            string statusDisplay = this.status_code.ToDisplayString();
            return $"{timeStr}[{statusDisplay}] {this.msg}";
        }

        public int LevelA()
        {
            return this.status_code.GetLevelA();
        }
    }

    public class Log
    {
        public List<Message> log_list;
        public LogConfig config;

        public Log(LogConfig config)
        {
            this.config = config;
            this.log_list = new List<Message>();
            // initial message (mirrors python initial append)
            var startStatus = new StatusCode(7, (byte)'L', 0x000);
            this.appendMsg(new Message(time: DateTimeOffset.UtcNow.ToOffset(this.config.timezone), status_code: startStatus, msg: "Program Start! Log system initialized!"));

            // Internal: record that log file path is set (internal 'L' section)
            this._addInternal(7, (byte)'L', 0x100, $"Log file created at {this.config.file_path}");
        }

        // Helper for adding internal messages (B='L' usage for internal messages)
        private void _addInternal(int a, byte b, uint detail, string text)
        {
            var internalStatus = new StatusCode(a, b, detail);
            var internalMsg = new Message(time: DateTimeOffset.UtcNow.ToOffset(this.config.timezone), status_code: internalStatus, msg: text);
            // Display in Consol once only
            if (internalMsg.LevelA() <= this.config.max_console_level)
            {
                Console.WriteLine(internalMsg.ToString());
            }
        }

        public void appendMsg(Message log_msg)
        {
            this.log_list.Add(log_msg);

            // Internal: record append operation (B='L', internal detail 0x101)
            int idx = this.log_list.Count - 1;
            string safeText = log_msg.msg.Length > 120 ? log_msg.msg.Substring(0, 120) + "..." : log_msg.msg;
            this.__afterOperation();
            this._addInternal(9, (byte)'L', 0x101, $"Appended message at index {idx}: level={log_msg.LevelA()} code={log_msg.status_code.ToDisplayString()} text='{safeText}'");
        }

        public void replaceMsg(int index, Message new_log_msg)
        {
            if (index < 0 || index >= this.log_list.Count) throw new IndexOutOfRangeException();
            var old = this.log_list[index];
            this.log_list[index] = new_log_msg;

            // Internal: record replace operation
            string oldText = old.msg.Length > 80 ? old.msg.Substring(0, 80) + "..." : old.msg;
            string newText = new_log_msg.msg.Length > 80 ? new_log_msg.msg.Substring(0, 80) + "..." : new_log_msg.msg;
            
            this._addInternal(7, (byte)'L', 0x102, $"Replaced message at index {index}: old(level={old.LevelA()} code={old.status_code.ToDisplayString()}) '{oldText}' -> new(level={new_log_msg.LevelA()} code={new_log_msg.status_code.ToDisplayString()}) '{newText}'");
        }

        public void removeMsg(int index)
        {
            if (index < 0 || index >= this.log_list.Count) throw new IndexOutOfRangeException();
            this.log_list.RemoveAt(index);

            // Internal: record removal
            this._addInternal(7, (byte)'L', 0x103, $"Removed message at index {index}.");

            // Save after removing
            this.export();
        }

        private void __afterOperation(int index = -1)
        {
            this.printMsg(index);
            if (this.__checkOrder(index))
            {
                this.__save();
            }
            else
            {
                this.export();
            }
        }

        public void printMsg(int index = -1)
        {
            if (this.log_list.Count == 0) return;
            int idx = index;
            if (index == -1) idx = this.log_list.Count - 1;
            if (idx < 0 || idx >= this.log_list.Count) return;
            var msg = this.log_list[idx];

            if (msg.LevelA() <= this.config.max_console_level)
            {
                Console.WriteLine(msg.ToString());
            }
        }

        private bool __checkOrder(int index)
        {
            if (index == 0)
            {
                return this.__sort();
            }
            if (this.log_list.Count == 1) return true;
            if (index < 0) index = this.log_list.Count - 1;
            if (index - 1 >= 0)
            {
                if (this.log_list[index - 1].time <= this.log_list[index].time)
                {
                    try
                    {
                        if (this.log_list[index + 1].time < this.log_list[index].time)
                        {
                            this.__sort();
                            return false;
                        }
                    }
                    catch (ArgumentOutOfRangeException) { /* no-op */ }
                    return true;
                }
                else
                {
                    this.__sort();
                    return false;
                }
            }
            return true;
        }

        private bool __sort()
        {
            var temp = this.log_list.OrderBy(m => m.time).ToList();
            bool equal = temp.SequenceEqual(this.log_list);
            if (!equal)
            {
                // Internal: record that we detected unsorted log entries and performed sort
                this._addInternal(5, (byte)'L', 0x110, "Detected unsorted log entries; performed sort.");

                this.log_list = temp;
                return false;
            }
            return true;
        }

        private void __save()
        {
            if (this.log_list.Count == 0) return;
            var last = this.log_list[this.log_list.Count - 1];
            if (last.LevelA() <= this.config.max_output_level)
            {
                try
                {
                    // Internal: attempt to save last line
                    this._addInternal(9, (byte)'L', 0x120, $"Attempting to save last line to file: {this.config.file_path}");

                    using (var sw = new StreamWriter(this.config.file_path, true, Encoding.UTF8))
                    {
                        sw.WriteLine(last.ToString());
                    }

                    // Internal: saved last line
                    this._addInternal(9, (byte)'L', 0x121, $"Saved last line to file: {this.config.file_path}");
                }
                catch (IOException ex)
                {
                    var errStatus = new StatusCode(4, (byte)'F', 0x001);
                    this.log_list.Add(new Message(time: DateTimeOffset.UtcNow.ToOffset(this.config.timezone), status_code: errStatus, msg: $"IOException while saving last line of log: {ex.Message}"));
                    this.printMsg(this.log_list.Count - 1);
                }
            }
        }

        public void export()
        {
            try
            {
                // Internal: export started
                int countBefore = this.log_list.Count;
                this._addInternal(8, (byte)'L', 0x130, $"Export started: writing up to {countBefore} messages to {this.config.file_path}");

                using (var sw = new StreamWriter(this.config.file_path, false, Encoding.UTF8))
                {
                    int written = 0;
                    foreach (var msg in this.log_list)
                    {
                        if (msg.LevelA() <= this.config.max_output_level)
                        {
                            sw.WriteLine(msg.ToString());
                            written += 1;
                        }
                    }
                    // Internal: export finished (write a message after writing but do not call export again)
                    this._addInternal(7, (byte)'L', 0x131, $"Export finished: wrote {written} message(s) to {this.config.file_path}");
                }
            }
            catch (IOException ex)
            {
                var errStatus = new StatusCode(4, (byte)'F', 0x002);
                this.log_list.Add(new Message(time: DateTimeOffset.UtcNow.ToOffset(this.config.timezone), status_code: errStatus, msg: $"IOException while exporting log: {ex.Message}"));
                this.printMsg(this.log_list.Count - 1);
            }
        }

        public override string ToString()
        {
            if (this.log_list.Count == 0) return "Empty log!";
            var sb = new StringBuilder();
            foreach (var m in this.log_list)
            {
                sb.AppendLine(m.ToString());
            }
            return sb.ToString().TrimEnd('\r', '\n');
        }

        public int __len__() => this.log_list.Count;
    }
}
