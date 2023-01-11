﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Nefarius.ViGEm.Client;
using LibUsbDotNet;
using LibUsbDotNet.LibUsb;
using LibUsbDotNet.Main;
using Nefarius.ViGEm.Client.Targets;

namespace GMK_Driver_NET
{
    public enum GMKControllerType
    {
        JOYSTICK = 0,
        CONTROLLER,
        TEST
    }

    internal class ControllerTypeDef
    {

    }

    public class GMKDriver
    {
        private ViGEmClient _vigemClient;
        private IXbox360Controller _xbox360Controller;
        private IUsbDevice _libusbClient;
        XInputController _controller;
        private UsbEndpointReader _usbEndpointReader;
        private GMKControllerType _controllerType;

        private int _vid; // Vendor ID
        private int _pid; // Product ID
        private int _ifN; // Interface Number
        private int _endpointIn;
        private ReadEndpointID _readEndpointID;

        private string _status;

        private const int ENDPOINT_DATA_SIZE = 13;

        public GMKDriver(GMKControllerType controllerType)
        {
            _controllerType = controllerType;
            Initialize();
        }

        private void Initialize()
        {
            switch (_controllerType)
            {
                case GMKControllerType.JOYSTICK:
                    _vid = 0x0483;
                    _pid = 0x5750;
                    _ifN = 0;
                    _endpointIn = 0x81;
                    break;
                
                case GMKControllerType.CONTROLLER:
                    _vid = 0x0483;
                    _pid = 0x5740;
                    _ifN = 2;
                    _endpointIn = 0x83;
                    break;

                case GMKControllerType.TEST:
                    _vid = 0x46;
                    _pid = 0x93;
                    _ifN = 0;
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
            {
                Console.WriteLine("Could not find GMK: " + _controllerType.ToString());
                Console.WriteLine(" VID: " + _vid.ToString() + " PID: " + _pid.ToString());
                return false;
            }
            
            // Convert device to interface and claim interface and configure
            _libusbClient = usbDevice as IUsbDevice;
            if(!ReferenceEquals(_libusbClient, null))
            {
                if(!_libusbClient.GetConfiguration(out byte config))
                {
                    Console.WriteLine("Unable to get device configuration.");
                    return false;
                }

                if(_libusbClient.SetConfiguration(config))
                {
                    Console.WriteLine("Unable to set device configuration.");
                    return false;
                }

                if(_libusbClient.ClaimInterface(_ifN))
                {
                    Console.WriteLine("Unable to claim device interface.");
                    return false;
                }
            }
            else
                return false;

            Console.WriteLine("Active endpoints:");
            bool endpointMatchFound = false;
            _readEndpointID = ReadEndpointID.Ep01;
            foreach(UsbEndpointBase endpoint in _libusbClient.ActiveEndpoints)
            {
                string endpointMatch = string.Empty;
                if(Convert.ToInt32(endpoint.EpNum) == _endpointIn)
                {
                    endpointMatch = " - ENDPOINT MATCH";
                    endpointMatchFound = true;
                }
                Console.WriteLine(" - " + endpoint.ToString() + ":" + endpoint.EpNum.ToString() + endpointMatch);
            }

            if(!endpointMatchFound)
            {
                Console.WriteLine("No matching endpoint found.");
                return false;
            }

            _usbEndpointReader = _libusbClient.OpenEndpointReader(ReadEndpointID.Ep01, ENDPOINT_DATA_SIZE, EndpointType.Interrupt);
            if(_usbEndpointReader == null)
            {
                Console.WriteLine("Unable to open endpoint " + ReadEndpointID.Ep01);
                return false;
            }

            return true;
        }

        

        public void Loop()
        {
            _controller = new XInputController();

            _vigemClient = new ViGEmClient();

            _xbox360Controller = _vigemClient.CreateXbox360Controller();
            
            _xbox360Controller.Connect();
            
            ErrorCode ec = ErrorCode.None;

            byte[] readBuffer = new byte[ENDPOINT_DATA_SIZE];
            int bytesRead;

            while (ec == ErrorCode.None)
            {
                ec = _usbEndpointReader.Read(readBuffer, 0, out bytesRead);

                if(bytesRead == ENDPOINT_DATA_SIZE)
                {
                    Console.WriteLine(BitConverter.ToString(readBuffer, 0, ENDPOINT_DATA_SIZE));
                    _controller.Map(readBuffer);
                    _controller.SetController(_xbox360Controller);
                }
            }
        }
    }
}
