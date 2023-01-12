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
	public class GMKController : GMKDevice
	{
		public GMKController(IUsbDevice usbDevice, DeviceConfig config, TextBox console) : 
			base(0x5740,
				2,
				0x83,
				0x13,
				GMKControllerType.Controller,
				usbDevice,
				config,
				console)
		{
			// Do nothing...
		}
	}
}
