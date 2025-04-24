namespace TeamVFL_Project_Prototype
{
    partial class Contour
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
            this.checkboxS22 = new System.Windows.Forms.CheckBox();
            this.checkboxS21 = new System.Windows.Forms.CheckBox();
            this.checkboxS12 = new System.Windows.Forms.CheckBox();
            this.checkboxS11 = new System.Windows.Forms.CheckBox();
            this.plotPanel = new System.Windows.Forms.Panel();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.btn_optimize = new System.Windows.Forms.Button();
            this.ShowGraph = new System.Windows.Forms.Button();
            this.Optimize_output = new System.Windows.Forms.RichTextBox();
            this.contour1 = new OxyPlot.WindowsForms.PlotView();
            this.contour2 = new OxyPlot.WindowsForms.PlotView();
            this.contour4 = new OxyPlot.WindowsForms.PlotView();
            this.contour3 = new OxyPlot.WindowsForms.PlotView();
            this.contour5 = new OxyPlot.WindowsForms.PlotView();
            this.contour9 = new OxyPlot.WindowsForms.PlotView();
            this.contour8 = new OxyPlot.WindowsForms.PlotView();
            this.contour7 = new OxyPlot.WindowsForms.PlotView();
            this.contour6 = new OxyPlot.WindowsForms.PlotView();
            this.groupBox1.SuspendLayout();
            this.SuspendLayout();
            // 
            // checkboxS22
            // 
            this.checkboxS22.AutoSize = true;
            this.checkboxS22.Location = new System.Drawing.Point(487, 196);
            this.checkboxS22.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.checkboxS22.Name = "checkboxS22";
            this.checkboxS22.Size = new System.Drawing.Size(52, 20);
            this.checkboxS22.TabIndex = 9;
            this.checkboxS22.Text = "S22";
            this.checkboxS22.UseVisualStyleBackColor = true;
            // 
            // checkboxS21
            // 
            this.checkboxS21.AutoSize = true;
            this.checkboxS21.Location = new System.Drawing.Point(487, 170);
            this.checkboxS21.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.checkboxS21.Name = "checkboxS21";
            this.checkboxS21.Size = new System.Drawing.Size(52, 20);
            this.checkboxS21.TabIndex = 10;
            this.checkboxS21.Text = "S21";
            this.checkboxS21.UseVisualStyleBackColor = true;
            // 
            // checkboxS12
            // 
            this.checkboxS12.AutoSize = true;
            this.checkboxS12.Location = new System.Drawing.Point(487, 144);
            this.checkboxS12.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.checkboxS12.Name = "checkboxS12";
            this.checkboxS12.Size = new System.Drawing.Size(52, 20);
            this.checkboxS12.TabIndex = 11;
            this.checkboxS12.Text = "S12";
            this.checkboxS12.UseVisualStyleBackColor = true;
            // 
            // checkboxS11
            // 
            this.checkboxS11.AutoSize = true;
            this.checkboxS11.Location = new System.Drawing.Point(487, 118);
            this.checkboxS11.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.checkboxS11.Name = "checkboxS11";
            this.checkboxS11.Size = new System.Drawing.Size(52, 20);
            this.checkboxS11.TabIndex = 12;
            this.checkboxS11.Text = "S11";
            this.checkboxS11.UseVisualStyleBackColor = true;
            // 
            // plotPanel
            // 
            this.plotPanel.Location = new System.Drawing.Point(87, 99);
            this.plotPanel.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.plotPanel.Name = "plotPanel";
            this.plotPanel.Size = new System.Drawing.Size(381, 390);
            this.plotPanel.TabIndex = 8;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.btn_optimize);
            this.groupBox1.Controls.Add(this.ShowGraph);
            this.groupBox1.Location = new System.Drawing.Point(41, 27);
            this.groupBox1.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Padding = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.groupBox1.Size = new System.Drawing.Size(509, 562);
            this.groupBox1.TabIndex = 13;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Design Response";
            // 
            // btn_optimize
            // 
            this.btn_optimize.Location = new System.Drawing.Point(275, 482);
            this.btn_optimize.Name = "btn_optimize";
            this.btn_optimize.Size = new System.Drawing.Size(126, 45);
            this.btn_optimize.TabIndex = 13;
            this.btn_optimize.Text = "Optimize";
            this.btn_optimize.UseVisualStyleBackColor = true;
            this.btn_optimize.Click += new System.EventHandler(this.btn_optimize_Click);
            // 
            // ShowGraph
            // 
            this.ShowGraph.Location = new System.Drawing.Point(83, 484);
            this.ShowGraph.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.ShowGraph.Name = "ShowGraph";
            this.ShowGraph.Size = new System.Drawing.Size(123, 41);
            this.ShowGraph.TabIndex = 4;
            this.ShowGraph.Text = "Initialize";
            this.ShowGraph.UseVisualStyleBackColor = true;
            this.ShowGraph.Click += new System.EventHandler(this.ShowGraph_Click);
            // 
            // Optimize_output
            // 
            this.Optimize_output.Location = new System.Drawing.Point(41, 638);
            this.Optimize_output.Name = "Optimize_output";
            this.Optimize_output.Size = new System.Drawing.Size(509, 327);
            this.Optimize_output.TabIndex = 14;
            this.Optimize_output.Text = "";
            // 
            // contour1
            // 
            this.contour1.Location = new System.Drawing.Point(644, 27);
            this.contour1.Name = "contour1";
            this.contour1.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour1.Size = new System.Drawing.Size(275, 275);
            this.contour1.TabIndex = 15;
            this.contour1.Text = "plotView1";
            this.contour1.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour1.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour1.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // contour2
            // 
            this.contour2.Location = new System.Drawing.Point(1040, 27);
            this.contour2.Name = "contour2";
            this.contour2.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour2.Size = new System.Drawing.Size(275, 275);
            this.contour2.TabIndex = 16;
            this.contour2.Text = "plotView1";
            this.contour2.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour2.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour2.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // contour4
            // 
            this.contour4.Location = new System.Drawing.Point(1040, 338);
            this.contour4.Name = "contour4";
            this.contour4.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour4.Size = new System.Drawing.Size(275, 275);
            this.contour4.TabIndex = 18;
            this.contour4.Text = "plotView2";
            this.contour4.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour4.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour4.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // contour3
            // 
            this.contour3.Location = new System.Drawing.Point(1464, 27);
            this.contour3.Name = "contour3";
            this.contour3.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour3.Size = new System.Drawing.Size(275, 275);
            this.contour3.TabIndex = 17;
            this.contour3.Text = "plotView1";
            this.contour3.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour3.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour3.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // contour5
            // 
            this.contour5.Location = new System.Drawing.Point(644, 338);
            this.contour5.Name = "contour5";
            this.contour5.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour5.Size = new System.Drawing.Size(275, 275);
            this.contour5.TabIndex = 19;
            this.contour5.Text = "plotView4";
            this.contour5.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour5.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour5.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // contour9
            // 
            this.contour9.Location = new System.Drawing.Point(1464, 638);
            this.contour9.Name = "contour9";
            this.contour9.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour9.Size = new System.Drawing.Size(275, 275);
            this.contour9.TabIndex = 23;
            this.contour9.Text = "plotView5";
            this.contour9.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour9.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour9.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // contour8
            // 
            this.contour8.Location = new System.Drawing.Point(1040, 638);
            this.contour8.Name = "contour8";
            this.contour8.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour8.Size = new System.Drawing.Size(275, 275);
            this.contour8.TabIndex = 22;
            this.contour8.Text = "plotView1";
            this.contour8.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour8.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour8.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // contour7
            // 
            this.contour7.Location = new System.Drawing.Point(644, 638);
            this.contour7.Name = "contour7";
            this.contour7.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour7.Size = new System.Drawing.Size(275, 275);
            this.contour7.TabIndex = 21;
            this.contour7.Text = "plotView7";
            this.contour7.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour7.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour7.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // contour6
            // 
            this.contour6.Location = new System.Drawing.Point(1464, 338);
            this.contour6.Name = "contour6";
            this.contour6.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.contour6.Size = new System.Drawing.Size(275, 275);
            this.contour6.TabIndex = 20;
            this.contour6.Text = "plotView1";
            this.contour6.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.contour6.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.contour6.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // Contour
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1841, 1003);
            this.Controls.Add(this.contour9);
            this.Controls.Add(this.contour8);
            this.Controls.Add(this.contour7);
            this.Controls.Add(this.contour6);
            this.Controls.Add(this.contour5);
            this.Controls.Add(this.contour4);
            this.Controls.Add(this.contour3);
            this.Controls.Add(this.contour2);
            this.Controls.Add(this.contour1);
            this.Controls.Add(this.Optimize_output);
            this.Controls.Add(this.checkboxS22);
            this.Controls.Add(this.checkboxS21);
            this.Controls.Add(this.checkboxS12);
            this.Controls.Add(this.checkboxS11);
            this.Controls.Add(this.plotPanel);
            this.Controls.Add(this.groupBox1);
            this.Name = "Contour";
            this.Text = "Contour";
            this.groupBox1.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.CheckBox checkboxS22;
        private System.Windows.Forms.CheckBox checkboxS21;
        private System.Windows.Forms.CheckBox checkboxS12;
        private System.Windows.Forms.CheckBox checkboxS11;
        private System.Windows.Forms.Panel plotPanel;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button btn_optimize;
        private System.Windows.Forms.Button ShowGraph;
        private System.Windows.Forms.RichTextBox Optimize_output;
        private OxyPlot.WindowsForms.PlotView contour1;
        private OxyPlot.WindowsForms.PlotView contour2;
        private OxyPlot.WindowsForms.PlotView contour4;
        private OxyPlot.WindowsForms.PlotView contour3;
        private OxyPlot.WindowsForms.PlotView contour5;
        private OxyPlot.WindowsForms.PlotView contour9;
        private OxyPlot.WindowsForms.PlotView contour8;
        private OxyPlot.WindowsForms.PlotView contour7;
        private OxyPlot.WindowsForms.PlotView contour6;
    }
}