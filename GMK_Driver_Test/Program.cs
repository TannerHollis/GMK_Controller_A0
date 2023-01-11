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
        static int Main(string[] args)
        {
            GMKDriver driver = new GMKDriver(GMKControllerType.TEST);

            if(!driver.FindUsbDevice())
            {
                Console.ReadLine();
                return -1;
            }

            driver.Loop();

            return 0;
        }
    }
}