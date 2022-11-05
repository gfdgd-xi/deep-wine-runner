/*
 * Created by SharpDevelop.
 * User: gfdgd xi
 * Date: 2022/11/5
 * Time: 17:22
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace CheckNet
{
	/// <summary>
	/// Description of MainForm.
	/// </summary>
	public partial class MainForm : Form
	{
		public MainForm()
		{
			//
			// The InitializeComponent() call is required for Windows Forms designer support.
			//
			InitializeComponent();
			
			//
			// TODO: Add constructor code after the InitializeComponent() call.
			//
		}
		void Button1Click(object sender, EventArgs e)
		{
			colorDialog1.ShowDialog();
			pictureBox1.BackColor = colorDialog1.Color;
		}
		void Button2Click(object sender, EventArgs e)
		{
			MessageBox.Show("这是一个对话框", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
			MessageBox.Show("这是一个对话框", "提示", MessageBoxButtons.OK, MessageBoxIcon.Question);
			MessageBox.Show("这是一个对话框", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
			MessageBox.Show("这是一个对话框", "提示", MessageBoxButtons.OK, MessageBoxIcon.Warning);
		}
		void Button3Click(object sender, EventArgs e)
		{
			fontDialog1.ShowDialog();
			label1.Font = fontDialog1.Font;
		}
		void Button4Click(object sender, EventArgs e)
		{
			openFileDialog1.ShowDialog();
		}
		void Button5Click(object sender, EventArgs e)
		{
			saveFileDialog1.ShowDialog();
		}
	}
}
