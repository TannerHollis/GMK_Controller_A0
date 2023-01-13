using System;
using System.Collections.Generic;
using System.ComponentModel;
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

        override public string ToString()
        {
            return input.ToString() + " -> " + output.ToString();
        }

        public ButtonAsButton(ButtonIO input, ButtonIO output)
        {
            this.input = input;
            this.output = output;
        }
    }

    public class ButtonAsJoystick
    {
        public ButtonIO input { get; set; }
        public JoystickIO output { get; set; }
        public Axis axis { get; set; }

        override public string ToString()
        {
            return input.ToString() + " -> " + output.ToString() + ", " + axis.ToString();
        }

        public ButtonAsJoystick(ButtonIO input, JoystickIO output)
        {
            this.input = input;
            this.output = output;
        }
    }

    public class ButtonAsTrigger
    {
        public ButtonIO input { get; set; }
        public TriggerIO output { get; set; }

        override public string ToString()
        {
            return input.ToString() + " -> " + output.ToString();
        }

        public ButtonAsTrigger(ButtonIO input, TriggerIO output)
        {
            this.input = input;
            this.output = output;
        }
    }

    public class ButtonAsKeyboard
    {
        public ButtonIO input { get; set; }
        public byte key { get; set; }

        public override string ToString()
        {
            return input.ToString() + " -> " + (char)key;
        }

        public ButtonAsKeyboard(ButtonIO input, byte key)
        {
            this.input = input;
            this.key = key;
        }
    }

    public class ButtonConfigs
    {
        public List<ButtonAsButton> asButtons { get; set; }
        public List<ButtonAsJoystick> asJoysticks { get; set; }
        public List<ButtonAsTrigger> asTriggers { get; set; }
        public List<ButtonAsKeyboard> asKeyboards { get; set; }
        public ButtonConfigs()
        {
            asButtons = new List<ButtonAsButton>();
            asJoysticks = new List<ButtonAsJoystick>();
            asTriggers = new List<ButtonAsTrigger>();
            asKeyboards = new List<ButtonAsKeyboard>();
        }
    }

    public class JoystickAsButton
    {
        public JoystickIO input { get; set; }
        public ButtonIO output { get; set; }
        public float threshold { get; set;}
        public JoystickAsButton(JoystickIO input, ButtonIO output, float threshold)
        {
            this.input = input;
            this.output = output;
            this.threshold = threshold;
        }
    }

    public class JoystickAsJoystick
    {
        public JoystickIO input { get; set; }
        public JoystickIO output { get; set;}
        public JoystickAsJoystick(JoystickIO input, JoystickIO output)
        {
            this.input = input;
            this.output = output;
        }
    }

    public class JoystickAsTrigger
    {
        public JoystickIO input { get; set;}
        public TriggerIO output { get; set;}
        public JoystickAsTrigger(JoystickIO input, TriggerIO output)
        {
            this.input = input;
            this.output = output;
        }
    }

    public class JoystickAsKeyboard
    {
        public JoystickIO input { get; set; }
        public byte key { get; set; }
        public JoystickAsKeyboard(JoystickIO input, byte key)
        {
            this.input = input;
            this.key = key;
        }
    }

    public class JoystickConfigs
    {
        public List<JoystickAsButton> asButtons { get; set; }
        public List<JoystickAsJoystick> asJoysticks { get; set; }
        public List<JoystickAsTrigger> asTriggers { get; set; }
        public List<JoystickAsKeyboard> asKeyboards { get; set; }
        public JoystickConfigs()
        {
            asButtons = new List<JoystickAsButton>();
            asJoysticks = new List<JoystickAsJoystick>();
            asTriggers = new List<JoystickAsTrigger>();
            asKeyboards = new List<JoystickAsKeyboard>();
        }
    }

    public class TriggerAsButton
    {
        public TriggerIO input { get; set; }
        public ButtonIO output { get; set; }
        public float threshold { get; set; }
        public TriggerAsButton(TriggerIO input, ButtonIO output, float threshold)
        {
            this.input = input;
            this.output = output;
            this.threshold = threshold;
        }
    }

    public class TriggerAsJoystick
    {
        public TriggerIO input { get; set; }
        public JoystickIO output { get; set; }
        public TriggerAsJoystick(TriggerIO input, JoystickIO output)
        {
            this.input = input;
            this.output = output;
        }
    }

    public class TriggerAsTrigger
    {
        public TriggerIO input { get; set; }
        public TriggerIO output { get; set; }
        public TriggerAsTrigger(TriggerIO input, TriggerIO output)
        {
            this.input = input;
            this.output = output;
        }
    }

    public class TriggerAsKeyboard
    {
        public TriggerIO input { get; set; }
        public byte key { get; set; }
        public float threshold { get; set; }
        public TriggerAsKeyboard(TriggerIO input, byte key, float threshold)
        {
            this.input = input;
            this.key = key;
            this.threshold = threshold;
        }
    }

    public class TriggerConfigs
    {
        public List<TriggerAsButton> asButtons { get; set; }
        public List<TriggerAsJoystick> asJoysticks { get; set; }
        public List<TriggerAsTrigger> asTriggers { get; set; }
        public List<TriggerAsKeyboard> asKeyboards { get; set; }
        public TriggerConfigs()
        {
            asButtons = new List<TriggerAsButton>();
            asJoysticks = new List<TriggerAsJoystick>();
            asTriggers = new List<TriggerAsTrigger>();
            asKeyboards = new List<TriggerAsKeyboard>();
        }
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
        RightBumper,
        Up,
        Down,
        Left,
        Right,
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

    public enum Axis
    {
        [Description("X+")]
        XPositive,
        [Description("X-")]
        XNegative,
        [Description("Y+")]
        YPositive,
        [Description("Y-")]
        YNegative
    }

    public class DeviceConfig
    {
        public string name { get; set; }
        public JoystickConfig joystickLeft { get; set; }
        public JoystickConfig joystickRight { get; set; }

        public AxisConfig triggerLeft { get; set; }
        public AxisConfig triggerRight { get; set; }

        public ButtonConfigs buttons { get; set; }
        public JoystickConfigs joysticks { get; set; }
        public TriggerConfigs triggers { get; set; }

        public DeviceConfig(string name)
        {
            this.name = name;
            joystickLeft = new JoystickConfig();
            joystickRight = new JoystickConfig();
            triggerLeft = new AxisConfig();
            triggerRight = new AxisConfig();
            buttons = new ButtonConfigs();
            joysticks = new JoystickConfigs();
            triggers = new TriggerConfigs();
        }

        public class AxisConfig
        {
            public float deadZone { get; set; }
            public float sensitivity { get; set; }
            public bool linear { get; set; }
        }

        public class TriggerConfig
        {
            public AxisConfig axis { get; set; }
            public TriggerConfig()
            {
                axis = new AxisConfig();
            }
        }

        public class JoystickConfig
        {
            public AxisConfig x { get; set; }
            public AxisConfig y { get; set; }
            public JoystickConfig()
            {
                x = new AxisConfig();
                y = new AxisConfig();
            }
        }

        public void ToFile(string file)
        {
            JsonSerializerOptions options = new JsonSerializerOptions();
            options.WriteIndented= true;

            string jsonString = JsonSerializer.Serialize<DeviceConfig>(this, options);
            File.WriteAllText(file, jsonString);
        }

        public static DeviceConfig FromFile(string file)
        {
            string jsonString = File.ReadAllText(file);
            return JsonSerializer.Deserialize<DeviceConfig>(jsonString);
        }

        public static DeviceConfig Default
        {
            get 
            {
                DeviceConfig c = new DeviceConfig("Default_v1.0");

                // Left X
                c.joystickLeft.x.deadZone = 0.1f;
                c.joystickLeft.x.linear = true;
                c.joystickLeft.x.sensitivity = 1.0f;

                // Left Y
                c.joystickLeft.y.deadZone = 0.1f;
                c.joystickLeft.y.linear = true;
                c.joystickLeft.y.sensitivity = 1.0f;

                // Right X
                c.joystickRight.x.deadZone = 0.1f;
                c.joystickRight.x.linear = true;
                c.joystickRight.x.sensitivity = 1.0f;

                // Right Y
                c.joystickRight.y.deadZone = 0.1f;
                c.joystickRight.y.linear = true;
                c.joystickRight.y.sensitivity = 1.0f;

                // LT
                c.triggerLeft.deadZone = 0.1f;
                c.triggerLeft.linear = true;
                c.triggerLeft.sensitivity = 1.0f;

                // RT
                c.triggerLeft.deadZone = 0.1f;
                c.triggerLeft.linear = true;
                c.triggerLeft.sensitivity = 1.0f;

                // Buttons
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.A, ButtonIO.A));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.B, ButtonIO.B));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.X, ButtonIO.X));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.Y, ButtonIO.Y));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.Back, ButtonIO.Back));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.Start, ButtonIO.Start));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.LeftThumb, ButtonIO.LeftThumb));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.Right, ButtonIO.RightThumb));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.LeftBumper, ButtonIO.LeftBumper));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.RightBumper, ButtonIO.RightBumper));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.Up, ButtonIO.Up));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.Down, ButtonIO.Down));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.Left, ButtonIO.Left));
                c.buttons.asButtons.Add(new ButtonAsButton(ButtonIO.Right, ButtonIO.Right));

                // Joysticks
                c.joysticks.asJoysticks.Add(new JoystickAsJoystick(JoystickIO.Left, JoystickIO.Left));
                c.joysticks.asJoysticks.Add(new JoystickAsJoystick(JoystickIO.Right, JoystickIO.Right));

                // Triggers
                c.triggers.asTriggers.Add(new TriggerAsTrigger(TriggerIO.Left, TriggerIO.Left));
                c.triggers.asTriggers.Add(new TriggerAsTrigger(TriggerIO.Right, TriggerIO.Right));

                return c;
            }
            
        }
    }
}
