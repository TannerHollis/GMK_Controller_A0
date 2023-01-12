using GMK_Driver_NET;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GMK_Driver_UI
{
    public partial class Main : Form
    {
        Thread mainThread;
        bool allowClosing = false;

        private static void ThreadProc(object consoleOutputObject)
        {
            TextBox consoleOutput = (TextBox)consoleOutputObject;

            int ret;

            GMKControllerType controllerType = GMKControllerType.Joystick;

            while (true)
            {
                ret = MainLoop(controllerType, consoleOutput);

                if (ret == -1)
                {
                    controllerType = (controllerType == GMKControllerType.Joystick) ?
                        GMKControllerType.Controller :
                        GMKControllerType.Joystick;
                }

                if (controllerType == GMKControllerType.Joystick)
                {
                    Thread.Sleep(5000);
                }
            }
        }

        private static int MainLoop(GMKControllerType controllerType, TextBox consoleOutput)
        {
            GMKDriver driver = new GMKDriver(controllerType, consoleOutput);

            if (!driver.FindUsbDevice())
            {
                return -1;
            }

            driver.Loop();

            return 0;
        }

        public Main()
        {
            InitializeComponent();

            mainThread = new Thread(new ParameterizedThreadStart(ThreadProc));
        }

        private void Main_Load(object sender, EventArgs e)
        {
            mainThread.Start(consoleBox);
        }

        private void Main_FormClosing(object sender, FormClosingEventArgs e)
        {
            if(e.CloseReason == CloseReason.UserClosing)
            {   
                this.Hide();
                if(!allowClosing)
                {
                    trayIcon.Visible = true;
                    e.Cancel = true;
                    trayIcon.ContextMenuStrip = trayContextMenuStrip;
                }
            }
        }

        private void Main_Exit(object sender, EventArgs e)
        {
            mainThread.Abort();
            allowClosing = true;
            this.Close();
        }

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Show();
            trayIcon.Visible = false;
        }

        private void quitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Main_Exit(sender, e);
        }
    }
}
