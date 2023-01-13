using GMK_Driver_NET;
using System;
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
    public partial class ButtonAsButtonControl : UserControl
    {
        private ButtonAsButton _buttonAsButton;

        public ButtonAsButtonControl()
        {
            InitializeComponent();
        }

        public void LoadWidget(ButtonAsButton buttonAsButton)
        {
            _buttonAsButton = buttonAsButton;
            inputButton.Select((int)_buttonAsButton.input, 1);
            outputButton.Select((int)_buttonAsButton.output, 1);
            this.Visible = true;
        }
    }
}
