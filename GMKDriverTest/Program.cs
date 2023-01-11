using GMK_Driver_NET;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GMKDriverTest
{
    internal class Program
    {
        static void Main(string[] args)
        {
            GMKDriver driver = new GMKDriver(GMKControllerType.JOYSTICK);

            if(!driver.FindUsbDevice())
            {
                return;
            }

            driver.loopRead();
        }
    }
}