using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Nefarius.ViGEm.Client;
using LibUsbDotNet;
using LibUsbDotNet.LibUsb;
using LibUsbDotNet.Main;

namespace GMK_Driver_NET
{
    public enum GMKControllerType
    {
        JOYSTICK = 0,
        CONTROLLER
    }

    public class GMKDriver
    {
        private ViGEmClient _vigemClient;
        private IUsbDevice _libusbClient;
        private UsbEndpointReader _usbEndpointReader;
        private GMKControllerType _controllerType;

        private int _vid; // Vendor ID
        private int _pid; // Product ID
        private int _ifN; // Interface Number
        private int _endpointIn;

        private const int ENDPOINT_DATA_SIZE = 13;

        public GMKDriver(GMKControllerType controllerType)
        {
            _controllerType = controllerType;
            Initialize();
        }

        private void Initialize()
        {
            _vid = 0x0483;

            switch (_controllerType) 
            {
                case GMKControllerType.JOYSTICK:
                    _pid = 0x5750;
                    _ifN = 0;
                    _endpointIn = 0x81;
                    break;
                
                case GMKControllerType.CONTROLLER:
                    _pid = 0x5740;
                    _ifN = 2;
                    _endpointIn = 0x83;
                    break;
            }
        }

        public bool FindUsbDevice()
        {
            // Create USB Finder instance
            UsbDeviceFinder usbFinder = new UsbDeviceFinder(_vid, _pid);
            
            // Try to find device, with associated VID and PID
            UsbDevice usbDevice = UsbDevice.OpenUsbDevice(usbFinder);
            if (usbDevice == null)
                return false;
            
            // Convert device to interface and claim interface and configure
            _libusbClient = usbDevice as IUsbDevice;
            if(!ReferenceEquals(_libusbClient, null))
            {
                _libusbClient.GetConfiguration(out byte config);
                _libusbClient.SetConfiguration(config);
                _libusbClient.ClaimInterface(_ifN);
            }
            else
                return false;

            _usbEndpointReader = _libusbClient.OpenEndpointReader(ReadEndpointID.Ep01, ENDPOINT_DATA_SIZE, EndpointType.Interrupt);
            if(_usbEndpointReader == null)
                return false;

            return true;
        }

        public void loopRead()
        {
            ErrorCode ec = ErrorCode.None;

            while (ec == ErrorCode.None)
            {
                byte[] readBuffer = new byte[ENDPOINT_DATA_SIZE];
                int bytesRead;
                ec = _usbEndpointReader.Read(readBuffer, 0, out bytesRead);
                Console.WriteLine(BitConverter.ToString(readBuffer, 0, bytesRead));
            }
        }
    }
}
