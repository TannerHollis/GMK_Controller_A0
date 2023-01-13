using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Nefarius.ViGEm.Client;
using LibUsbDotNet;
using LibUsbDotNet.LibUsb;
using LibUsbDotNet.Main;
using Nefarius.ViGEm.Client.Targets;
using System.Windows.Forms;
using System.Threading;

namespace GMK_Driver_NET
{
    public class GMKDriver
    {
        private const int GMK_VID = 0x483;
        private const int JOYSTICK_PID = 0x5750;
        private const int CONTROLLER_PID = 0x5740;

        private static DeviceAssociations _deviceAssociations;
        private static List<Thread> _threads = new List<Thread>();
        private static List<GMKDevice> _devices = new List<GMKDevice>();
        private static TextBox _console;
        private static UsbContext _context;
        private static UsbDeviceCollection _deviceCollection;

        public static DeviceAssociations DeviceAssociations { get { return _deviceAssociations; } }
        public static Thread[] Threads { get { return _threads.ToArray(); } }
        public static GMKDevice[] Devices { get { return _devices.ToArray(); } }

        public static void SetConsole(TextBox console)
        {
            _console = console;
        }

        private static void WriteLine(string text)
        {
            List<string> consoleOutputList = new List<string>();
            if (_console != null)
            {
                consoleOutputList = new List<string>();
                consoleOutputList.AddRange(_console.Lines);
                consoleOutputList.Add(text);
                _console.Invoke((MethodInvoker)delegate
                {
                    _console.Lines = consoleOutputList.ToArray();
                    _console.Refresh();
                });
            }
            else
            {
                Console.WriteLine(text);
            }
        }

        public static void Loop()
        {
            using (_context = new UsbContext())
            {
                WriteLine("Scanning devices...");
                List<GMKDevice> newDevices;

                while (true)
                {
                    // Scan for devices and start their respective driver
                    newDevices = ScanAndStartDevices();

                    // Inform user device was connected
                    foreach (GMKDevice device in newDevices)
                    {
                        WriteLine("GMK: " + device.Type + "found. SN: " + device.SerialNumber);
                    }

                    // Wait for device enumeration by polling
                    while(_deviceCollection.Count == _context.List().Count)
                    {
                        Thread.Sleep(500);
                    }
                }
            }
        }

        private static List<GMKDevice> ScanAndStartDevices()
        {
            List<GMKDevice> newDevices = new List<GMKDevice>();

            if (_deviceAssociations == null)
            {
                _deviceAssociations = DeviceAssociations.Load();
            }

            foreach (Thread thread in _threads)
            {
                if(!thread.IsAlive)
                {
                    _threads.Remove(thread);
                }
            }

            foreach(GMKDevice device in _devices)
            {
                if(!device.UsbDevice.IsOpen)
                {
                    _devices.Remove(device);
                }
            }

            _deviceCollection = _context.List();

            foreach(IUsbDevice device in _deviceCollection)
            {
                // Check VID and PID
                bool gmkDeviceFound = device.VendorId == GMK_VID && (device.ProductId == JOYSTICK_PID || device.ProductId == CONTROLLER_PID);
                if (!gmkDeviceFound)
                    continue;
                else
                    device.Open();

                // Check if device already has a driver attached
                gmkDeviceFound = false;
                foreach(GMKDevice gmkDevice in _devices)
                {
                    if (gmkDevice.UsbDevice.Info.SerialNumber.Equals(device.Info.SerialNumber))
                    {
                        gmkDeviceFound = true;
                        break;
                    }
                }

                // If device is already being used, close and continue for loop
                if (gmkDeviceFound)
                {
                    device.Close();
                    continue;
                }

                ConfigAssociation configAssociation = _deviceAssociations.LookupSerialNumber(device.Info.SerialNumber);

                DeviceConfig config;

                if (configAssociation == null)
                {
                    DeviceAssociations.AddNewDevice(device.Info.SerialNumber);
                    config = DeviceConfig.Default;
                    DeviceAssociations.AddConfiguration(device.Info.SerialNumber, config, true);
                }
                else
                {
                    config = DeviceConfig.FromFile(configAssociation.defaultConfigFile);
                }

                if (device.ProductId == JOYSTICK_PID)
                {
                    GMKJoystick joystick = new GMKJoystick(device, config, _console);
                    newDevices.Add(joystick);
                }

                if(device.ProductId == CONTROLLER_PID)
                {
                    GMKController controller = new GMKController(device, config, _console);
                    _devices.Add(controller);
                }

                device.Close();
            }

            foreach(GMKDevice device in newDevices)
            {
                Thread t = new Thread(new ParameterizedThreadStart(Run));
                _threads.Add(t);
                t.Start(device);
            }

            _devices.AddRange(newDevices);
            return newDevices;
        }

        public static void Run(object device)
        {
            GMKDevice gmkDevice = (GMKDevice)device;
            gmkDevice.Run();
        }
    }
}
