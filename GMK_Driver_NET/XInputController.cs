using Nefarius.ViGEm.Client.Targets;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Nefarius.ViGEm.Client.Targets.Xbox360;

namespace GMK_Driver_NET
{
    public class XInputController
    {
        bool up;
        bool down;
        bool left;
        bool right;
        bool start;
        bool back;
        bool lth;
        bool rth;
        bool lb;
        bool rb;
        bool xbox;
        bool _reserved;
        bool a;
        bool b;
        bool x;
        bool y;
        Int16 leftX;
        Int16 leftY;
        Int16 rightX;
        Int16 rightY;
        char triggerLeft;
        char triggerRight;

        UInt16 buttons;

        private bool GetBit(byte b, int bitNumber)
        {
            return (b & (1 << bitNumber - 1)) != 0;
        }

        public void Map(byte[] bytes)
        {
            buttons = (UInt16)(bytes[2] << 8 | bytes[1]);
            up = GetBit(bytes[1], 0);
            down = GetBit(bytes[1], 1);
            left = GetBit(bytes[1], 2);
            right = GetBit(bytes[1], 3);
            start = GetBit(bytes[1], 4);
            back = GetBit(bytes[1], 5);
            lth = GetBit(bytes[1], 6);
            rth = GetBit(bytes[1], 7);
            lb = GetBit(bytes[2], 0);
            rb = GetBit(bytes[2], 1);
            xbox = GetBit(bytes[2], 2);
            _reserved = GetBit(bytes[2], 3);
            a = GetBit(bytes[2], 4);
            b = GetBit(bytes[2], 5);
            x = GetBit(bytes[2], 6);
            y = GetBit(bytes[2], 7);

            leftX = (Int16)(bytes[4] << 8 | bytes[3]);
            leftY = (Int16)(-1 * (bytes[6] << 8 | bytes[5]));

            rightX = (Int16)(bytes[8] << 8 | bytes[7]);
            rightY = (Int16)(bytes[10] << 8 | bytes[9]);

            triggerLeft = (char)bytes[11];
            triggerRight = (char)bytes[12];
        }

        public void SetController(in IXbox360Controller controller)
        {
            controller.SetButtonsFull(buttons);
            controller.SetAxisValue(Xbox360Axis.LeftThumbX, leftX);
            controller.SetAxisValue(Xbox360Axis.LeftThumbY, leftY);
            controller.SetAxisValue(Xbox360Axis.RightThumbX, rightX);
            controller.SetAxisValue(Xbox360Axis.RightThumbY, rightY);
            controller.SetSliderValue(Xbox360Slider.LeftTrigger, Convert.ToByte(triggerLeft));
            controller.SetSliderValue(Xbox360Slider.RightTrigger, Convert.ToByte(triggerRight));
        }
    }
}
