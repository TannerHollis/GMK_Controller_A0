using GMK_Driver_NET;
using System;
using System.CodeDom;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GMK_Driver_UI
{
    public partial class configurationEditor : Form
    {
        private GMKDevice _device;
        private DeviceAssociations _associations;
        private ConfigAssociation _configAssociation;
        private List<DeviceConfig> _configs;
        private DeviceConfig _defaultConfig;
        private DeviceConfig _currentConfig;

        private ButtonAsButtonControl _buttonAsButtonControl;

        public configurationEditor(GMKDevice device)
        {
            InitializeComponent();
            _device = device;
            _associations = DeviceAssociations.Load();
            _configAssociation = _associations.LookupSerialNumber(device.SerialNumber);

            _configs = new List<DeviceConfig>();

            foreach(string configFile in _configAssociation.configFiles)
            {
                _configs.Add(DeviceConfig.FromFile(configFile));
            }

            _defaultConfig = DeviceConfig.FromFile(_configAssociation.defaultConfigFile);
        }

        private void LoadWidgets()
        {
            // Add ButtonAsButton Widget
            _buttonAsButtonControl = new ButtonAsButtonControl();
            _buttonAsButtonControl.Dock = DockStyle.Fill;
            _buttonAsButtonControl.Visible = false;
            gridLayout.Controls.Add(_buttonAsButtonControl, 1, 1);
        }

        private void configurationEditor_Load(object sender, EventArgs e)
        {
            LoadConfiguration(_defaultConfig);
        }

        private void LoadConfiguration(DeviceConfig config)
        {
            _currentConfig = config;

            bindingsTreeView.Nodes["Joystick Settings"].Nodes["Left"].Tag = config.joystickLeft;
            bindingsTreeView.Nodes["Joystick Settings"].Nodes["Right"].Tag = config.joystickRight;

            bindingsTreeView.Nodes["Trigger Settings"].Nodes["Left"].Tag = config.triggerLeft;
            bindingsTreeView.Nodes["Trigger Settings"].Nodes["Right"].Tag = config.triggerRight;

            // Get Button Bindings
            {
                TreeNode buttonBindings = bindingsTreeView.Nodes["Bindings"].Nodes["Button Bindings"];
                buttonBindings.Nodes.Clear();

                // Add ButtonAsButtons
                foreach (ButtonAsButton asButton in config.buttons.asButtons)
                {
                    TreeNode node = new TreeNode(asButton.ToString());
                    node.Tag = asButton;
                    buttonBindings.Nodes.Add(node);
                }

                // Add ButtonAsJoysticks
                foreach (ButtonAsJoystick asJoystick in config.buttons.asJoysticks)
                {
                    TreeNode node = new TreeNode(asJoystick.ToString());
                    node.Tag = asJoystick;
                    buttonBindings.Nodes.Add(node);
                }

                // Add ButtonAsTriggers
                foreach (ButtonAsTrigger asTrigger in config.buttons.asTriggers)
                {
                    TreeNode node = new TreeNode(asTrigger.ToString());
                    node.Tag = asTrigger;
                    buttonBindings.Nodes.Add(node);
                }

                // Add JoystickAsKeyboards
                foreach (ButtonAsKeyboard asKeyboard in config.buttons.asKeyboards)
                {
                    TreeNode node = new TreeNode(asKeyboard.ToString());
                    node.Tag = asKeyboard;
                    buttonBindings.Nodes.Add(node);
                }
            }

            // Get Joystick Bindings
            {
                TreeNode joystickBindings = bindingsTreeView.Nodes["Bindings"].Nodes["Joystick Bindings"];
                joystickBindings.Nodes.Clear();

                // Add JoystickAsButtons
                foreach (JoystickAsButton asButton in config.joysticks.asButtons)
                {
                    TreeNode node = new TreeNode(asButton.ToString());
                    node.Tag = asButton;
                    joystickBindings.Nodes.Add(node);
                }

                // Add JoystickAsJoysticks
                foreach (JoystickAsJoystick asJoystick in config.joysticks.asJoysticks)
                {
                    TreeNode node = new TreeNode(asJoystick.ToString());
                    node.Tag = asJoystick;
                    joystickBindings.Nodes.Add(node);
                }

                // Add JoystickAsTriggers
                foreach (JoystickAsTrigger asTrigger in config.joysticks.asTriggers)
                {
                    TreeNode node = new TreeNode(asTrigger.ToString());
                    node.Tag = asTrigger;
                    joystickBindings.Nodes.Add(node);
                }

                // Add JoystickAsKeyboards
                foreach (JoystickAsKeyboard asKeyboard in config.joysticks.asKeyboards)
                {
                    TreeNode node = new TreeNode(asKeyboard.ToString());
                    node.Tag = asKeyboard;
                    joystickBindings.Nodes.Add(node);
                }
            }

            // Get Trigger Bindings
            {
                TreeNode triggerBindings = bindingsTreeView.Nodes["Bindings"].Nodes["Joystick Bindings"];
                triggerBindings.Nodes.Clear();

                // Add TriggerAsButtons
                foreach (TriggerAsButton asButton in config.triggers.asButtons)
                {
                    TreeNode node = new TreeNode(asButton.ToString());
                    node.Tag = asButton;
                    triggerBindings.Nodes.Add(node);
                }

                // Add TriggerAsJoysticks
                foreach (TriggerAsJoystick asJoystick in config.triggers.asJoysticks)
                {
                    TreeNode node = new TreeNode(asJoystick.ToString());
                    node.Tag = asJoystick;
                    triggerBindings.Nodes.Add(node);
                }

                // Add TriggerAsTriggers
                foreach (TriggerAsTrigger asTrigger in config.triggers.asTriggers)
                {
                    TreeNode node = new TreeNode(asTrigger.ToString());
                    node.Tag = asTrigger;
                    triggerBindings.Nodes.Add(node);
                }

                // Add TriggerAsKeyboards
                foreach (TriggerAsKeyboard asKeyboard in config.triggers.asKeyboards)
                {
                    TreeNode node = new TreeNode(asKeyboard.ToString());
                    node.Tag = asKeyboard;
                    triggerBindings.Nodes.Add(node);
                }
            }
        }

        private void bindingsTreeView_Click(object sender, EventArgs e)
        {
            string type = bindingsTreeView.SelectedNode.Tag.GetType().ToString();
            switch (type)
            {
                case "ButtonAsButton":
                    gridLayout.Controls.Add();
                    break;
            }
        }
    }
}
