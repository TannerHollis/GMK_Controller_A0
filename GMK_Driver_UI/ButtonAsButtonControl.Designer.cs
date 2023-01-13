namespace GMK_Driver_UI
{
    partial class ButtonAsButtonControl
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

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.outputButton = new System.Windows.Forms.ComboBox();
            this.outputButtonLabel = new System.Windows.Forms.Label();
            this.inputButtonLabel = new System.Windows.Forms.Label();
            this.inputButton = new System.Windows.Forms.ComboBox();
            this.tableLayoutPanel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 2;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 29.69799F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 70.30202F));
            this.tableLayoutPanel1.Controls.Add(this.outputButton, 1, 1);
            this.tableLayoutPanel1.Controls.Add(this.outputButtonLabel, 0, 1);
            this.tableLayoutPanel1.Controls.Add(this.inputButtonLabel, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.inputButton, 1, 0);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 2;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 46.64311F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 53.35689F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(596, 283);
            this.tableLayoutPanel1.TabIndex = 0;
            // 
            // outputButton
            // 
            this.outputButton.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.outputButton.FormattingEnabled = true;
            this.outputButton.Items.AddRange(new object[] {
            "A",
            "B",
            "X",
            "Y",
            "Start",
            "Back",
            "Xbox",
            "LeftThumb",
            "RightThumb",
            "LeftBumper",
            "RightBumper",
            "Up",
            "Down",
            "Left",
            "Right"});
            this.outputButton.Location = new System.Drawing.Point(180, 197);
            this.outputButton.Name = "outputButton";
            this.outputButton.Size = new System.Drawing.Size(121, 21);
            this.outputButton.TabIndex = 3;
            // 
            // outputButtonLabel
            // 
            this.outputButtonLabel.AutoSize = true;
            this.outputButtonLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.outputButtonLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.outputButtonLabel.Location = new System.Drawing.Point(3, 132);
            this.outputButtonLabel.Name = "outputButtonLabel";
            this.outputButtonLabel.Size = new System.Drawing.Size(171, 151);
            this.outputButtonLabel.TabIndex = 1;
            this.outputButtonLabel.Text = "Output Button";
            this.outputButtonLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // inputButtonLabel
            // 
            this.inputButtonLabel.AutoSize = true;
            this.inputButtonLabel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.inputButtonLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.inputButtonLabel.Location = new System.Drawing.Point(3, 0);
            this.inputButtonLabel.Name = "inputButtonLabel";
            this.inputButtonLabel.Size = new System.Drawing.Size(171, 132);
            this.inputButtonLabel.TabIndex = 0;
            this.inputButtonLabel.Text = "Input Button";
            this.inputButtonLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // inputButton
            // 
            this.inputButton.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.inputButton.FormattingEnabled = true;
            this.inputButton.Items.AddRange(new object[] {
            "A",
            "B",
            "X",
            "Y",
            "Start",
            "Back",
            "Xbox",
            "LeftThumb",
            "RightThumb",
            "LeftBumper",
            "RightBumper",
            "Up",
            "Down",
            "Left",
            "Right"});
            this.inputButton.Location = new System.Drawing.Point(180, 55);
            this.inputButton.Name = "inputButton";
            this.inputButton.Size = new System.Drawing.Size(121, 21);
            this.inputButton.TabIndex = 2;
            // 
            // ButtonAsButtonControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.tableLayoutPanel1);
            this.Name = "ButtonAsButtonControl";
            this.Size = new System.Drawing.Size(596, 283);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.Label outputButtonLabel;
        private System.Windows.Forms.Label inputButtonLabel;
        private System.Windows.Forms.ComboBox outputButton;
        private System.Windows.Forms.ComboBox inputButton;
    }
}
