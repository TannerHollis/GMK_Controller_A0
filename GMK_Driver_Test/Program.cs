using GMK_Driver_NET;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Reflection;

namespace GMKDriverTest
{
    internal class Program
    {
        static void Main(string[] args)
        {
            DeviceConfig config = DeviceConfig.Default;
            config.ToFile("test.json");
            
            GMKDriver.Loop();
        }
    }
}