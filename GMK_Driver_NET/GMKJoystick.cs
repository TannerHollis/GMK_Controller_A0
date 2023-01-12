using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using LibUsbDotNet;
using LibUsbDotNet.LibUsb;
using LibUsbDotNet.Main;

namespace GMK_Driver_NET
{
    public class GMKJoystick : GMKDevice
    {
		public GMKJoystick(IUsbDevice usbDevice, DeviceConfig config, TextBox console) : 
			base(0x5750, 
				0, 
				0x81,
				0x13,
				GMKControllerType.Joystick,
				usbDevice, 
				config,
				console)
		{
			// Do nothing...
		}
    }
}
