using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace GMK_Driver_NET
{
    public class ButtonAsButton
    {
        public ButtonIO input { get; set; }
        public ButtonIO output { get; set; }
    }

    public class ButtonAsJoystick
    {
        public ButtonIO input { get; set; }
        public JoystickIO output { get; set; }
    }

    public class ButtonAsTrigger
    {
        public ButtonIO input { get; set; }
        public TriggerIO output { get; set; }
    }

    public class ButtonAsKeyboard
    {
        public ButtonIO input { get; set; }
        public byte key { get; set; }
    }

    public class ButtonConfigs
    {
        List<ButtonAsButton> asButtons { get; set; }
        List<ButtonAsJoystick> asJoysticks { get; set; }
        List<ButtonAsTrigger> asTriggers { get; set; }
        List<ButtonAsKeyboard> asKeyboards { get; set; }
    }

    public class JoystickAsButton
    {
        public JoystickIO input { get; set; }
        public ButtonIO output { get; set; }
        public float threshold { get; set;}
    }

    public class JoystickAsJoystick
    {
        public JoystickIO input { get; set; }
        public JoystickIO output { get; set;}
    }

    public class JoystickAsTrigger
    {
        public JoystickIO input { get; set;}
        public TriggerIO output { get; set;}
    }

    public class JoystickAsKeyboard
    {
        public JoystickIO input { get; set; }
        public byte key { get; set; }
    }

    public class JoystickConfigs
    {
        List<JoystickAsButton> asButtons { get; set; }
        List<JoystickAsJoystick> asJoysticks { get; set; }
        List<JoystickAsTrigger> asTriggers { get; set; }
        List<JoystickAsKeyboard> asKeyboards { get; set; }
    }

    public class TriggerAsButton
    {
        public TriggerIO input { get; set; }
        public ButtonIO output { get; set; }
        public float threshold { get; set; }
    }

    public class TriggerAsJoystick
    {
        public TriggerIO input { get; set; }
        public JoystickIO output { get; set; }
    }

    public class TriggerAsTrigger
    {
        public TriggerIO input { get; set; }
        public TriggerIO output { get; set; }
    }

    public class TriggerAsKeyboard
    {
        public TriggerIO input { get; set; }
        public byte key { get; set; }
        public float threshold { get; set; }
    }

    public class TriggerConfigs
    {
        List<TriggerAsButton> asButtons { get; set; }
        List<TriggerAsJoystick> asJoysticks { get; set; }
        List<TriggerAsTrigger> asTriggers { get; set; }
        List<TriggerAsKeyboard> asKeyboards { get; set; }
    }

    public enum ButtonIO
    {
        A,
        B,
        X,
        Y,
        Start,
        Back,
        Xbox,
        LeftThumb,
        RightThumb,
        LeftBumper,
        RightBumper
    }

    public enum JoystickIO
    {
        Left,
        Right
    }

    public enum TriggerIO
    {
        Left,
        Right
    }

    public class DeviceConfig
    {
        public string name { get; set; }
        public string serialNumber { get; set; }
        public JoystickConfig joystickLeft { get; set; }
        public JoystickConfig joystickRight { get; set; }

        public AxisConfig triggerLeft { get; set; }
        public AxisConfig triggerRight { get; set; }

        public ButtonConfigs buttons { get; set; }
        public JoystickConfigs joysticks { get; set; }
        public TriggerConfigs triggers { get; set; }

        public class AxisConfig
        {
            public float deadZone { get; set; }
            public float sensitivity { get; set; }
            public bool linear { get; set; }
        }

        public class TriggerConfig
        {
            public AxisConfig axis { get; set; }
        }

        public class JoystickConfig
        {
            public AxisConfig x { get; set; }
            public AxisConfig y { get; set; }
        }

        public static DeviceConfig FromFile(string file)
        {
            string jsonString = File.ReadAllText(file);
            return JsonSerializer.Deserialize<DeviceConfig>(jsonString);
        }
    }
}
