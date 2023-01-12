using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Configuration;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using LibUsbDotNet;
using LibUsbDotNet.LibUsb;
using LibUsbDotNet.Main;
using Nefarius.ViGEm.Client.Targets;
using Nefarius.ViGEm.Client;

namespace GMK_Driver_NET
{
    public enum GMKError
    {
        OK,
        InvalidEndpoint,
        AlreadyOpen,
        Disconnected,
        ClaimError,
        ReadTimeout,
    }
    public enum  GMKControllerType{
        Joystick = 0,
        Controller,
        Undefined
    }

    public abstract class GMKDevice
    {
        private int _vid = 0x483;
        private int _pid;
        private int _interfaceN;
        private int _endpoint;
        private uint _endpointBufferSize;
        private GMKControllerType _type;
        private IUsbDevice _usbDevice;
        private DeviceConfig _config;
        private TextBox _consoleOutput;
        private string _serialNumber;

        public int VID { get { return _vid; } }
        public int PID { get { return _pid; } }
        public int Interface { get { return _interfaceN; } }
        public int Endpoint { get { return _endpoint; } }
        public DeviceConfig Config { get { return _config; } }
        public GMKControllerType Type { get { return _type; } }
        public IUsbDevice UsbDevice { get { return _usbDevice; } }
        public string SerialNumber { get { return _serialNumber; } }

        public GMKDevice(int pid,
            int interfaceN,
            int endpoint,
            uint endpointBufferSize,
            GMKControllerType type,
            IUsbDevice usbDevice,
            DeviceConfig config,
            TextBox consoleOutput)
        {
            _pid = pid;
            _interfaceN = interfaceN;
            _endpoint = endpoint;
            _endpointBufferSize = endpointBufferSize;
            _type = type;
            _usbDevice = usbDevice;
            _config = config;
            _consoleOutput = consoleOutput;
            _serialNumber = _usbDevice.Info.SerialNumber;
        }

        public GMKDevice(int pid,
            int interfaceN,
            int endpoint,
            uint endpointBufferSize,
            GMKControllerType type,
            IUsbDevice usbDevice,
            string deviceConfigFile,
            TextBox consoleOutput)
        {
            _pid = pid;
            _interfaceN = interfaceN;
            _endpoint = endpoint;
            _endpointBufferSize = endpointBufferSize;
            _type = type;
            _usbDevice = usbDevice;
            _config = DeviceConfig.FromFile(deviceConfigFile);
            _consoleOutput = consoleOutput;
            _serialNumber = _usbDevice.Info.SerialNumber;
        }

        public GMKError Run()
        {
            GMKError ret;

            ret = Connect();
            if(ret != GMKError.OK)
            {
                return ret;
            }

            ret = Configure();
            if(ret != GMKError.OK)
            {
                return ret;
            }

            ret = Loop();

            _usbDevice.Close();

            return ret;
        }
        private GMKError Connect()
        {
            if (!_usbDevice.IsOpen)
            {
                _usbDevice.Open();
                return GMKError.OK;
            }
            else
            {
                WriteLine("Device is already open.");
                return GMKError.AlreadyOpen;
            }
        }

        private GMKError Configure()
        {
            int configuration = _usbDevice.Configuration;
            _usbDevice.SetConfiguration(configuration);
            if(!_usbDevice.ClaimInterface(_interfaceN))
            {
                WriteLine("Unabled to claim interface.");
                return GMKError.ClaimError;
            }
            return GMKError.OK;
        }

        private void WriteLine(string text)
        {
            text = _type + ":" + _serialNumber + " - " + text;
            List<string> consoleOutputList = new List<string>();
            if (_consoleOutput != null)
            {
                consoleOutputList = new List<string>();
                consoleOutputList.AddRange(_consoleOutput.Lines);
                consoleOutputList.Add(text);
                _consoleOutput.Invoke((MethodInvoker)delegate
                {
                    _consoleOutput.Lines = consoleOutputList.ToArray();
                    _consoleOutput.Refresh();
                });
            }
            else
            {
                Console.WriteLine(text);
            }
        }

        private GMKError Loop()
        {
            UsbEndpointReader usbEndpointReader = _usbDevice.OpenEndpointReader((ReadEndpointID)_endpoint);

            if(usbEndpointReader == null)
            {
                WriteLine("Unable to open read endpoint.");
                return GMKError.InvalidEndpoint;
            }
            else
            {
                WriteLine("Successfully opened device. Starting driver...");
            }

            XInputController controller = new XInputController();
            ViGEmClient vigemClient = new ViGEmClient();
            IXbox360Controller xbox360Controller = vigemClient.CreateXbox360Controller();

            xbox360Controller.Connect();

            Error ec = Error.Success;

            byte[] readBuffer = new byte[_endpointBufferSize];
            int bytesRead;

            while (ec == Error.Success)
            {
                ec = usbEndpointReader.Read(readBuffer, 0, out bytesRead);

                if (bytesRead == _endpointBufferSize)
                {
                    controller.Map(readBuffer);
                    controller.SetController(xbox360Controller);
                }
            }

            if(ec == Error.Timeout)
            {
                return GMKError.ReadTimeout;
            }

            if(ec == Error.Io || ec == Error.NotFound || ec == Error.NoDevice || ec == Error.Busy)
            {
                return GMKError.Disconnected;
            }

            return GMKError.OK;
        }
    }
}
