VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   3600
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   5880
   BeginProperty Font 
   EndProperty
   Font            =   "Form1.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   3600
   ScaleWidth      =   5880
   StartUpPosition =   3  '窗口缺省
   Begin VB.DriveListBox Drive1 
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":000F
      Height          =   300
      Left            =   4080
      TabIndex        =   8
      Top             =   1680
      Width           =   975
   End
   Begin VB.ComboBox Combo1 
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":001E
      Height          =   300
      Left            =   4920
      TabIndex        =   7
      Text            =   "Combo1"
      Top             =   840
      Width           =   855
   End
   Begin VB.ListBox List1 
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":002D
      Height          =   420
      Left            =   3720
      TabIndex        =   6
      Top             =   720
      Width           =   975
   End
   Begin VB.OptionButton Option2 
      Caption         =   "Option2"
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":003C
      Height          =   255
      Left            =   1920
      TabIndex        =   5
      Top             =   3240
      Width           =   975
   End
   Begin VB.OptionButton Option1 
      Caption         =   "Option1"
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":004B
      Height          =   255
      Left            =   480
      TabIndex        =   4
      Top             =   3240
      Width           =   975
   End
   Begin VB.CheckBox Check1 
      Caption         =   "Check1"
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":005A
      Height          =   375
      Left            =   2400
      TabIndex        =   3
      Top             =   2520
      Width           =   855
   End
   Begin VB.TextBox Text1 
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":0069
      Height          =   495
      Left            =   2520
      TabIndex        =   2
      Text            =   "Text1"
      Top             =   1680
      Width           =   1335
   End
   Begin VB.CommandButton Command1 
      Caption         =   "Command1"
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":0078
      Height          =   615
      Left            =   2520
      TabIndex        =   1
      Top             =   720
      Width           =   855
   End
   Begin VB.Image Image1 
      BorderStyle     =   1  'Fixed Single
      Height          =   1905
      Left            =   240
      Picture         =   "Form1.frx":0087
      Stretch         =   -1  'True
      Top             =   840
      Width           =   1905
   End
   Begin VB.Label Label1 
      Caption         =   "此程序用于判断 Wine 内是否能正确运行 Visual Basic 6 程序"
      BeginProperty Font 
      EndProperty
      Font            =   "Form1.frx":558B
      Height          =   375
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   5655
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
