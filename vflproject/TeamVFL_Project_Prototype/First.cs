﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TeamVFL_Project_Prototype
{
    public partial class First : Form
    {
        public First()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Home homeWindow = new Home();
            homeWindow.Show();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Contour contour = new Contour();    
            contour.Show();
        }
    }
}
