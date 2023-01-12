namespace GMK_Driver_UI
{
    partial class Main
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Main));
            System.Windows.Forms.ListViewItem listViewItem1 = new System.Windows.Forms.ListViewItem("Joystick - 001-002-003", 0);
            this.trayIcon = new System.Windows.Forms.NotifyIcon(this.components);
            this.consoleBox = new System.Windows.Forms.TextBox();
            this.deviceGroupBox = new System.Windows.Forms.GroupBox();
            this.deviceView = new System.Windows.Forms.ListView();
            this.imageList = new System.Windows.Forms.ImageList(this.components);
            this.trayContextMenuStrip = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.openToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.quitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.updateTimer = new System.Windows.Forms.Timer(this.components);
            this.deviceViewContextMenu = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.openToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.closeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.deviceGroupBox.SuspendLayout();
            this.trayContextMenuStrip.SuspendLayout();
            this.deviceViewContextMenu.SuspendLayout();
            this.SuspendLayout();
            // 
            // trayIcon
            // 
            this.trayIcon.Icon = ((System.Drawing.Icon)(resources.GetObject("trayIcon.Icon")));
            this.trayIcon.Text = "GMK Driver";
            this.trayIcon.Visible = true;
            // 
            // consoleBox
            // 
            this.consoleBox.BackColor = System.Drawing.SystemColors.MenuText;
            this.consoleBox.ForeColor = System.Drawing.SystemColors.Window;
            this.consoleBox.Location = new System.Drawing.Point(12, 164);
            this.consoleBox.Multiline = true;
            this.consoleBox.Name = "consoleBox";
            this.consoleBox.ReadOnly = true;
            this.consoleBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.consoleBox.Size = new System.Drawing.Size(655, 150);
            this.consoleBox.TabIndex = 0;
            // 
            // deviceGroupBox
            // 
            this.deviceGroupBox.Controls.Add(this.deviceView);
            this.deviceGroupBox.Location = new System.Drawing.Point(12, 12);
            this.deviceGroupBox.Name = "deviceGroupBox";
            this.deviceGroupBox.Size = new System.Drawing.Size(655, 146);
            this.deviceGroupBox.TabIndex = 1;
            this.deviceGroupBox.TabStop = false;
            this.deviceGroupBox.Text = "Devices";
            // 
            // deviceView
            // 
            this.deviceView.ContextMenuStrip = this.deviceViewContextMenu;
            this.deviceView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.deviceView.HideSelection = false;
            this.deviceView.Items.AddRange(new System.Windows.Forms.ListViewItem[] {
            listViewItem1});
            this.deviceView.LargeImageList = this.imageList;
            this.deviceView.Location = new System.Drawing.Point(3, 16);
            this.deviceView.Name = "deviceView";
            this.deviceView.Size = new System.Drawing.Size(649, 127);
            this.deviceView.TabIndex = 0;
            this.deviceView.TileSize = new System.Drawing.Size(64, 64);
            this.deviceView.UseCompatibleStateImageBehavior = false;
            // 
            // imageList
            // 
            this.imageList.ImageStream = ((System.Windows.Forms.ImageListStreamer)(resources.GetObject("imageList.ImageStream")));
            this.imageList.TransparentColor = System.Drawing.Color.Transparent;
            this.imageList.Images.SetKeyName(0, "icon.png");
            this.imageList.Images.SetKeyName(1, "GMKlogo_transparent_square.ico");
            // 
            // trayContextMenuStrip
            // 
            this.trayContextMenuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.openToolStripMenuItem,
            this.quitToolStripMenuItem});
            this.trayContextMenuStrip.Name = "trayContextMenuStrip";
            this.trayContextMenuStrip.Size = new System.Drawing.Size(113, 48);
            // 
            // openToolStripMenuItem
            // 
            this.openToolStripMenuItem.Name = "openToolStripMenuItem";
            this.openToolStripMenuItem.Size = new System.Drawing.Size(112, 22);
            this.openToolStripMenuItem.Text = "Open...";
            this.openToolStripMenuItem.Click += new System.EventHandler(this.openToolStripMenuItem_Click);
            // 
            // quitToolStripMenuItem
            // 
            this.quitToolStripMenuItem.Name = "quitToolStripMenuItem";
            this.quitToolStripMenuItem.Size = new System.Drawing.Size(112, 22);
            this.quitToolStripMenuItem.Text = "Quit";
            this.quitToolStripMenuItem.Click += new System.EventHandler(this.quitToolStripMenuItem_Click);
            // 
            // updateTimer
            // 
            this.updateTimer.Interval = 2500;
            this.updateTimer.Tick += new System.EventHandler(this.updateTimer_Tick);
            // 
            // deviceViewContextMenu
            // 
            this.deviceViewContextMenu.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.openToolStripMenuItem1,
            this.closeToolStripMenuItem});
            this.deviceViewContextMenu.Name = "deviceViewContextMenu";
            this.deviceViewContextMenu.Size = new System.Drawing.Size(104, 48);
            // 
            // openToolStripMenuItem1
            // 
            this.openToolStripMenuItem1.Name = "openToolStripMenuItem1";
            this.openToolStripMenuItem1.Size = new System.Drawing.Size(103, 22);
            this.openToolStripMenuItem1.Text = "Open";
            // 
            // closeToolStripMenuItem
            // 
            this.closeToolStripMenuItem.Name = "closeToolStripMenuItem";
            this.closeToolStripMenuItem.Size = new System.Drawing.Size(103, 22);
            this.closeToolStripMenuItem.Text = "Close";
            // 
            // Main
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(679, 326);
            this.Controls.Add(this.deviceGroupBox);
            this.Controls.Add(this.consoleBox);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Main";
            this.Text = "GMK Driver";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Main_FormClosing);
            this.Load += new System.EventHandler(this.Main_Load);
            this.deviceGroupBox.ResumeLayout(false);
            this.trayContextMenuStrip.ResumeLayout(false);
            this.deviceViewContextMenu.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.NotifyIcon trayIcon;
        private System.Windows.Forms.TextBox consoleBox;
        private System.Windows.Forms.GroupBox deviceGroupBox;
        private System.Windows.Forms.ListView deviceView;
        private System.Windows.Forms.ContextMenuStrip trayContextMenuStrip;
        private System.Windows.Forms.ToolStripMenuItem openToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem quitToolStripMenuItem;
        private System.Windows.Forms.ImageList imageList;
        private System.Windows.Forms.Timer updateTimer;
        private System.Windows.Forms.ContextMenuStrip deviceViewContextMenu;
        private System.Windows.Forms.ToolStripMenuItem openToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem closeToolStripMenuItem;
    }
}

