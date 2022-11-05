/*
 * Created by SharpDevelop.
 * User: gfdgd xi
 * Date: 2022/11/5
 * Time: 18:08
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace CheckNetAndIE
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
			webBrowser1.Navigate("https://gfdgd-xi.github.io");
		}
		void Button2Click(object sender, EventArgs e)
		{
			webBrowser1.Navigate("https://bbs.deepin.org/user/239113");
		}
		void Button3Click(object sender, EventArgs e)
		{
			webBrowser1.Navigate("https://spark-app.store/");
		}
		void Button4Click(object sender, EventArgs e)
		{
			webBrowser1.Navigate("https://gitee.com/gfdgd-xi");
		}
		void Button5Click(object sender, EventArgs e)
		{
			webBrowser1.Navigate("https://github.com/gfdgd-xi");
		}
		void Button6Click(object sender, EventArgs e)
		{
			webBrowser1.Navigate(textBox1.Text);
		}
	}
}
