namespace GMK_Driver_UI
{
    partial class configurationEditor
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
            System.Windows.Forms.ListViewItem listViewItem1 = new System.Windows.Forms.ListViewItem(new string[] {
            "Default_v1.0",
            "Default"}, -1);
            System.Windows.Forms.TreeNode treeNode1 = new System.Windows.Forms.TreeNode("Left");
            System.Windows.Forms.TreeNode treeNode2 = new System.Windows.Forms.TreeNode("Right");
            System.Windows.Forms.TreeNode treeNode3 = new System.Windows.Forms.TreeNode("Joystick Settings", new System.Windows.Forms.TreeNode[] {
            treeNode1,
            treeNode2});
            System.Windows.Forms.TreeNode treeNode4 = new System.Windows.Forms.TreeNode("Left");
            System.Windows.Forms.TreeNode treeNode5 = new System.Windows.Forms.TreeNode("Right");
            System.Windows.Forms.TreeNode treeNode6 = new System.Windows.Forms.TreeNode("TriggerSettings", new System.Windows.Forms.TreeNode[] {
            treeNode4,
            treeNode5});
            System.Windows.Forms.TreeNode treeNode7 = new System.Windows.Forms.TreeNode("Button Bindings");
            System.Windows.Forms.TreeNode treeNode8 = new System.Windows.Forms.TreeNode("Joystick Bindings");
            System.Windows.Forms.TreeNode treeNode9 = new System.Windows.Forms.TreeNode("TriggerBindings");
            System.Windows.Forms.TreeNode treeNode10 = new System.Windows.Forms.TreeNode("Bindings", new System.Windows.Forms.TreeNode[] {
            treeNode7,
            treeNode8,
            treeNode9});
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(configurationEditor));
            this.gridLayout = new System.Windows.Forms.TableLayoutPanel();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.deviceTypeLabel = new System.Windows.Forms.Label();
            this.deviceType = new System.Windows.Forms.Label();
            this.serialNumberLabel = new System.Windows.Forms.Label();
            this.configsView = new System.Windows.Forms.ListView();
            this.configName = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.defaultConfig = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.serialNumber = new System.Windows.Forms.Label();
            this.bindingsTreeView = new System.Windows.Forms.TreeView();
            this.imageList1 = new System.Windows.Forms.ImageList(this.components);
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.bindingEditorContextMenu = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.addToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.buttonToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.buttonAsButtonToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.buttonAsJoystickToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.buttonAsTriggerToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.joystickToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.triggerToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.joystickAsButtonToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.joystickAsJoystickToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.joystickAsTriggerToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.buttonAsKeyboardToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.joystickAsKeyboardToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.triggerAsButtonToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.triggerAsJoystickToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.triggerAsTriggerToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.triggerAsKeyboardToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.removeBindingToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.gridLayout.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.bindingEditorContextMenu.SuspendLayout();
            this.SuspendLayout();
            // 
            // gridLayout
            // 
            this.gridLayout.ColumnCount = 2;
            this.gridLayout.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 28.98719F));
            this.gridLayout.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 71.0128F));
            this.gridLayout.Controls.Add(this.tableLayoutPanel2, 0, 0);
            this.gridLayout.Controls.Add(this.configsView, 0, 1);
            this.gridLayout.Controls.Add(this.bindingsTreeView, 1, 1);
            this.gridLayout.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridLayout.Location = new System.Drawing.Point(0, 0);
            this.gridLayout.Name = "gridLayout";
            this.gridLayout.RowCount = 2;
            this.gridLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50.37879F));
            this.gridLayout.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 49.62121F));
            this.gridLayout.Size = new System.Drawing.Size(859, 528);
            this.gridLayout.TabIndex = 0;
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.ColumnCount = 2;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 32.66331F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 67.33669F));
            this.tableLayoutPanel2.Controls.Add(this.serialNumber, 1, 2);
            this.tableLayoutPanel2.Controls.Add(this.serialNumberLabel, 0, 2);
            this.tableLayoutPanel2.Controls.Add(this.deviceTypeLabel, 0, 1);
            this.tableLayoutPanel2.Controls.Add(this.deviceType, 1, 1);
            this.tableLayoutPanel2.Controls.Add(this.pictureBox1, 0, 0);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 3);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 3;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(243, 260);
            this.tableLayoutPanel2.TabIndex = 0;
            // 
            // deviceTypeLabel
            // 
            this.deviceTypeLabel.AutoSize = true;
            this.deviceTypeLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.deviceTypeLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.deviceTypeLabel.Location = new System.Drawing.Point(3, 210);
            this.deviceTypeLabel.Name = "deviceTypeLabel";
            this.deviceTypeLabel.Size = new System.Drawing.Size(73, 25);
            this.deviceTypeLabel.TabIndex = 0;
            this.deviceTypeLabel.Text = "Device:";
            this.deviceTypeLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // deviceType
            // 
            this.deviceType.AutoSize = true;
            this.deviceType.Dock = System.Windows.Forms.DockStyle.Fill;
            this.deviceType.Location = new System.Drawing.Point(82, 210);
            this.deviceType.Name = "deviceType";
            this.deviceType.Size = new System.Drawing.Size(158, 25);
            this.deviceType.TabIndex = 1;
            this.deviceType.Text = "Device Type";
            this.deviceType.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // serialNumberLabel
            // 
            this.serialNumberLabel.AutoSize = true;
            this.serialNumberLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.serialNumberLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.serialNumberLabel.Location = new System.Drawing.Point(3, 235);
            this.serialNumberLabel.Name = "serialNumberLabel";
            this.serialNumberLabel.Size = new System.Drawing.Size(73, 25);
            this.serialNumberLabel.TabIndex = 2;
            this.serialNumberLabel.Text = "SN:";
            this.serialNumberLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // configsView
            // 
            this.configsView.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.configName,
            this.defaultConfig});
            this.configsView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.configsView.FullRowSelect = true;
            this.configsView.HideSelection = false;
            this.configsView.Items.AddRange(new System.Windows.Forms.ListViewItem[] {
            listViewItem1});
            this.configsView.Location = new System.Drawing.Point(3, 269);
            this.configsView.MultiSelect = false;
            this.configsView.Name = "configsView";
            this.configsView.Size = new System.Drawing.Size(243, 256);
            this.configsView.TabIndex = 1;
            this.configsView.UseCompatibleStateImageBehavior = false;
            this.configsView.View = System.Windows.Forms.View.Details;
            // 
            // configName
            // 
            this.configName.Text = "Configuration Name";
            this.configName.Width = 120;
            // 
            // defaultConfig
            // 
            this.defaultConfig.Text = "Default Config";
            this.defaultConfig.Width = 98;
            // 
            // serialNumber
            // 
            this.serialNumber.AutoSize = true;
            this.serialNumber.Dock = System.Windows.Forms.DockStyle.Fill;
            this.serialNumber.Location = new System.Drawing.Point(82, 235);
            this.serialNumber.Name = "serialNumber";
            this.serialNumber.Size = new System.Drawing.Size(158, 25);
            this.serialNumber.TabIndex = 3;
            this.serialNumber.Text = "Serial Number";
            this.serialNumber.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // bindingsTreeView
            // 
            this.bindingsTreeView.ContextMenuStrip = this.bindingEditorContextMenu;
            this.bindingsTreeView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.bindingsTreeView.FullRowSelect = true;
            this.bindingsTreeView.Indent = 20;
            this.bindingsTreeView.Location = new System.Drawing.Point(252, 269);
            this.bindingsTreeView.Name = "bindingsTreeView";
            treeNode1.Name = "leftJoystick";
            treeNode1.Text = "Left";
            treeNode2.Name = "rightJoystick";
            treeNode2.Text = "Right";
            treeNode3.Name = "joystickSettings";
            treeNode3.Text = "Joystick Settings";
            treeNode4.Name = "leftTrigger";
            treeNode4.Text = "Left";
            treeNode5.Name = "rightTrigger";
            treeNode5.Text = "Right";
            treeNode6.ImageIndex = 1;
            treeNode6.Name = "triggerSettings";
            treeNode6.Text = "TriggerSettings";
            treeNode7.Name = "buttonBindings";
            treeNode7.Text = "Button Bindings";
            treeNode8.Name = "joystickBindings";
            treeNode8.Text = "Joystick Bindings";
            treeNode9.Name = "triggerBindings";
            treeNode9.Text = "TriggerBindings";
            treeNode10.ImageKey = "trigger.png";
            treeNode10.Name = "bindings";
            treeNode10.Text = "Bindings";
            this.bindingsTreeView.Nodes.AddRange(new System.Windows.Forms.TreeNode[] {
            treeNode3,
            treeNode6,
            treeNode10});
            this.bindingsTreeView.Size = new System.Drawing.Size(604, 256);
            this.bindingsTreeView.TabIndex = 1;
            this.bindingsTreeView.Click += new System.EventHandler(this.bindingsTreeView_Click);
            // 
            // imageList1
            // 
            this.imageList1.ImageStream = ((System.Windows.Forms.ImageListStreamer)(resources.GetObject("imageList1.ImageStream")));
            this.imageList1.TransparentColor = System.Drawing.Color.Transparent;
            this.imageList1.Images.SetKeyName(0, "button.png");
            this.imageList1.Images.SetKeyName(1, "joystick.png");
            this.imageList1.Images.SetKeyName(2, "trigger.png");
            // 
            // pictureBox1
            // 
            this.pictureBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureBox1.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.tableLayoutPanel2.SetColumnSpan(this.pictureBox1, 2);
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(3, 3);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(237, 204);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBox1.TabIndex = 4;
            this.pictureBox1.TabStop = false;
            // 
            // bindingEditorContextMenu
            // 
            this.bindingEditorContextMenu.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.addToolStripMenuItem,
            this.removeBindingToolStripMenuItem});
            this.bindingEditorContextMenu.Name = "bindingEditorContextMenu";
            this.bindingEditorContextMenu.Size = new System.Drawing.Size(162, 48);
            // 
            // addToolStripMenuItem
            // 
            this.addToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.buttonToolStripMenuItem,
            this.joystickToolStripMenuItem,
            this.triggerToolStripMenuItem});
            this.addToolStripMenuItem.Name = "addToolStripMenuItem";
            this.addToolStripMenuItem.Size = new System.Drawing.Size(161, 22);
            this.addToolStripMenuItem.Text = "Add Binding";
            // 
            // buttonToolStripMenuItem
            // 
            this.buttonToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.buttonAsButtonToolStripMenuItem,
            this.buttonAsJoystickToolStripMenuItem,
            this.buttonAsTriggerToolStripMenuItem,
            this.buttonAsKeyboardToolStripMenuItem});
            this.buttonToolStripMenuItem.Name = "buttonToolStripMenuItem";
            this.buttonToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.buttonToolStripMenuItem.Text = "Button";
            // 
            // buttonAsButtonToolStripMenuItem
            // 
            this.buttonAsButtonToolStripMenuItem.Name = "buttonAsButtonToolStripMenuItem";
            this.buttonAsButtonToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.buttonAsButtonToolStripMenuItem.Text = "ButtonAsButton";
            // 
            // buttonAsJoystickToolStripMenuItem
            // 
            this.buttonAsJoystickToolStripMenuItem.Name = "buttonAsJoystickToolStripMenuItem";
            this.buttonAsJoystickToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.buttonAsJoystickToolStripMenuItem.Text = "ButtonAsJoystick";
            // 
            // buttonAsTriggerToolStripMenuItem
            // 
            this.buttonAsTriggerToolStripMenuItem.Name = "buttonAsTriggerToolStripMenuItem";
            this.buttonAsTriggerToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.buttonAsTriggerToolStripMenuItem.Text = "ButtonAsTrigger";
            // 
            // joystickToolStripMenuItem
            // 
            this.joystickToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.joystickAsButtonToolStripMenuItem,
            this.joystickAsJoystickToolStripMenuItem,
            this.joystickAsTriggerToolStripMenuItem,
            this.joystickAsKeyboardToolStripMenuItem});
            this.joystickToolStripMenuItem.Name = "joystickToolStripMenuItem";
            this.joystickToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.joystickToolStripMenuItem.Text = "Joystick";
            // 
            // triggerToolStripMenuItem
            // 
            this.triggerToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.triggerAsButtonToolStripMenuItem,
            this.triggerAsJoystickToolStripMenuItem,
            this.triggerAsTriggerToolStripMenuItem,
            this.triggerAsKeyboardToolStripMenuItem});
            this.triggerToolStripMenuItem.Name = "triggerToolStripMenuItem";
            this.triggerToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.triggerToolStripMenuItem.Text = "Trigger";
            // 
            // joystickAsButtonToolStripMenuItem
            // 
            this.joystickAsButtonToolStripMenuItem.Name = "joystickAsButtonToolStripMenuItem";
            this.joystickAsButtonToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.joystickAsButtonToolStripMenuItem.Text = "JoystickAsButton";
            // 
            // joystickAsJoystickToolStripMenuItem
            // 
            this.joystickAsJoystickToolStripMenuItem.Name = "joystickAsJoystickToolStripMenuItem";
            this.joystickAsJoystickToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.joystickAsJoystickToolStripMenuItem.Text = "JoystickAsJoystick";
            // 
            // joystickAsTriggerToolStripMenuItem
            // 
            this.joystickAsTriggerToolStripMenuItem.Name = "joystickAsTriggerToolStripMenuItem";
            this.joystickAsTriggerToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.joystickAsTriggerToolStripMenuItem.Text = "JoystickAsTrigger";
            // 
            // buttonAsKeyboardToolStripMenuItem
            // 
            this.buttonAsKeyboardToolStripMenuItem.Name = "buttonAsKeyboardToolStripMenuItem";
            this.buttonAsKeyboardToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.buttonAsKeyboardToolStripMenuItem.Text = "ButtonAsKeyboard";
            // 
            // joystickAsKeyboardToolStripMenuItem
            // 
            this.joystickAsKeyboardToolStripMenuItem.Name = "joystickAsKeyboardToolStripMenuItem";
            this.joystickAsKeyboardToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.joystickAsKeyboardToolStripMenuItem.Text = "JoystickAsKeyboard";
            // 
            // triggerAsButtonToolStripMenuItem
            // 
            this.triggerAsButtonToolStripMenuItem.Name = "triggerAsButtonToolStripMenuItem";
            this.triggerAsButtonToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.triggerAsButtonToolStripMenuItem.Text = "TriggerAsButton";
            // 
            // triggerAsJoystickToolStripMenuItem
            // 
            this.triggerAsJoystickToolStripMenuItem.Name = "triggerAsJoystickToolStripMenuItem";
            this.triggerAsJoystickToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.triggerAsJoystickToolStripMenuItem.Text = "TriggerAsJoystick";
            // 
            // triggerAsTriggerToolStripMenuItem
            // 
            this.triggerAsTriggerToolStripMenuItem.Name = "triggerAsTriggerToolStripMenuItem";
            this.triggerAsTriggerToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.triggerAsTriggerToolStripMenuItem.Text = "TriggerAsTrigger";
            // 
            // triggerAsKeyboardToolStripMenuItem
            // 
            this.triggerAsKeyboardToolStripMenuItem.Name = "triggerAsKeyboardToolStripMenuItem";
            this.triggerAsKeyboardToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.triggerAsKeyboardToolStripMenuItem.Text = "TriggerAsKeyboard";
            // 
            // removeBindingToolStripMenuItem
            // 
            this.removeBindingToolStripMenuItem.Name = "removeBindingToolStripMenuItem";
            this.removeBindingToolStripMenuItem.Size = new System.Drawing.Size(161, 22);
            this.removeBindingToolStripMenuItem.Text = "Remove Binding";
            // 
            // configurationEditor
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(859, 528);
            this.Controls.Add(this.gridLayout);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "configurationEditor";
            this.Text = "Configuration Editor";
            this.Load += new System.EventHandler(this.configurationEditor_Load);
            this.gridLayout.ResumeLayout(false);
            this.tableLayoutPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.bindingEditorContextMenu.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TableLayoutPanel gridLayout;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private System.Windows.Forms.Label serialNumberLabel;
        private System.Windows.Forms.Label deviceTypeLabel;
        private System.Windows.Forms.Label deviceType;
        private System.Windows.Forms.ListView configsView;
        private System.Windows.Forms.ColumnHeader configName;
        private System.Windows.Forms.ColumnHeader defaultConfig;
        private System.Windows.Forms.Label serialNumber;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.TreeView bindingsTreeView;
        private System.Windows.Forms.ContextMenuStrip bindingEditorContextMenu;
        private System.Windows.Forms.ImageList imageList1;
        private System.Windows.Forms.ToolStripMenuItem addToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem buttonToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem buttonAsButtonToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem buttonAsJoystickToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem buttonAsTriggerToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem buttonAsKeyboardToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem joystickToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem joystickAsButtonToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem joystickAsJoystickToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem joystickAsTriggerToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem joystickAsKeyboardToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem triggerToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem triggerAsButtonToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem triggerAsJoystickToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem triggerAsTriggerToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem triggerAsKeyboardToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem removeBindingToolStripMenuItem;
    }
}