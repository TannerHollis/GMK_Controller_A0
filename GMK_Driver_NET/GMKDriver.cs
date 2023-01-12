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
        public static DeviceAssociations _deviceAssociations;
        public static List<Thread> _threads = new List<Thread>();
        public static List<GMKDevice> _devices = new List<GMKDevice>();

        private static TextBox _console;

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
            WriteLine("Scanning devices...");
            List<GMKDevice> newDevices;
            while (true)
            {
                newDevices = ScanAndStartDevices();
                foreach(GMKDevice device in newDevices)
                {
                    WriteLine("GMK: " + device.Type + "found. SN: " + device.SerialNumber);
                }
                
                Thread.Sleep(5000);
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

            UsbDeviceFinder usbFinder = new UsbDeviceFinder(0x483);

            using(UsbContext context = new UsbContext())
            {
                UsbDeviceCollection results = context.FindAll(usbFinder);

                foreach(IUsbDevice device in results)
                {
                    foreach(GMKDevice gmkDevice in _devices)
                    {
                        if (gmkDevice.UsbDevice.Equals(device))
                        {
                            continue;
                        }
                    }

                    ConfigAssociation configAssociation = _deviceAssociations.LookupSerialNumber(device.Info.SerialNumber);

                    DeviceConfig config;

                    if (configAssociation == null)
                    {
                        config = new DeviceConfig();
                    }
                    else
                    {
                        config = DeviceConfig.FromFile(configAssociation.defaultConfig);
                    }

                    if (device.ProductId == 0x5750)
                    {
                        GMKJoystick joystick = new GMKJoystick(device, config, _console);
                        newDevices.Add(joystick);
                    }

                    if(device.ProductId == 0x5740)
                    {
                        // GMKController controller = new GMKController(device, config, console);
                        //_devices.Add(controller);
                    }
                }
            }

            foreach(GMKDevice device in newDevices)
            {
                Thread t = new Thread(new ParameterizedThreadStart(Run));
                _threads.Add(t);
                t.Start();
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
