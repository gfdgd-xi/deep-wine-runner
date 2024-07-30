
from PyQt5.QtCore import Qt

## Encoding Type for SetEncodings()
# publicly documented
ENC_RAW      = 0  # Raw
ENC_COPYRECT = 1  # CopyRect
ENC_RRE      = 2  # RRE
ENC_HEXTILE  = 5  # Hextile
ENC_TRLE     = 15 # TRLE
ENC_ZRLE     = 16 # ZRLE

# pseudo-encodings
ENC_CURSOR      = -239 # Cursor position pseudo-encoding
ENC_DESKTOPSIZE = -223 # DesktopSize pseudo-encoding

# additional
ENC_CORRE   = 4
ENC_ZLIB    = 6
ENC_TIGHT   = 7
ENC_ZLIBHEX = 8


## Keycodes for KeyEvent()
KEY_BackSpace = 0xff08
KEY_Tab =       0xff09
KEY_Return =    0xff0d
KEY_Escape =    0xff1b
KEY_Insert =    0xff63
KEY_Delete =    0xffff
KEY_Home =      0xff50
KEY_End =       0xff57
KEY_PageUp =    0xff55
KEY_PageDown =  0xff56
KEY_Left =      0xff51
KEY_Up =        0xff52
KEY_Right =     0xff53
KEY_Down =      0xff54
KEY_F1 =        0xffbe
KEY_F2 =        0xffbf
KEY_F3 =        0xffc0
KEY_F4 =        0xffc1
KEY_F5 =        0xffc2
KEY_F6 =        0xffc3
KEY_F7 =        0xffc4
KEY_F8 =        0xffc5
KEY_F9 =        0xffc6
KEY_F10 =       0xffc7
KEY_F11 =       0xffc8
KEY_F12 =       0xffc9
KEY_F13 =       0xFFCA
KEY_F14 =       0xFFCB
KEY_F15 =       0xFFCC
KEY_F16 =       0xFFCD
KEY_F17 =       0xFFCE
KEY_F18 =       0xFFCF
KEY_F19 =       0xFFD0
KEY_F20 =       0xFFD1
KEY_ShiftLeft = 0xffe1
KEY_ShiftRight = 0xffe2
KEY_ControlLeft = 0xffe3
KEY_ControlRight = 0xffe4
KEY_MetaLeft =  0xffe7
KEY_MetaRight = 0xffe8
KEY_AltLeft =   0xffe9
KEY_AltRight =  0xffea

KEY_Scroll_Lock = 0xFF14
KEY_Sys_Req =   0xFF15
KEY_Num_Lock =  0xFF7F
KEY_Caps_Lock = 0xFFE5
KEY_Pause =     0xFF13
KEY_Super_L =   0xFFEB
KEY_Super_R =   0xFFEC
KEY_Hyper_L =   0xFFED
KEY_Hyper_R =   0xFFEE

KEY_KP_0 =      0xFFB0
KEY_KP_1 =      0xFFB1
KEY_KP_2 =      0xFFB2
KEY_KP_3 =      0xFFB3
KEY_KP_4 =      0xFFB4
KEY_KP_5 =      0xFFB5
KEY_KP_6 =      0xFFB6
KEY_KP_7 =      0xFFB7
KEY_KP_8 =      0xFFB8
KEY_KP_9 =      0xFFB9
KEY_KP_Enter =  0xFF8D

# thanks to ken3 (https://github.com/ken3) for this
KEY_TRANSLATION_SPECIAL = {
    Qt.Key.Key_Backspace:  KEY_BackSpace,
    Qt.Key.Key_Tab:        KEY_Tab,
    Qt.Key.Key_Return:     KEY_Return,
    Qt.Key.Key_Escape:     KEY_Escape,
    Qt.Key.Key_Insert:     KEY_Insert,
    Qt.Key.Key_Delete:     KEY_Delete,
    Qt.Key.Key_Home:       KEY_Home,
    Qt.Key.Key_End:        KEY_End,
    Qt.Key.Key_PageUp:     KEY_PageUp,
    Qt.Key.Key_PageDown:   KEY_PageDown,
    Qt.Key.Key_Left:       KEY_Left,
    Qt.Key.Key_Up:         KEY_Up,
    Qt.Key.Key_Right:      KEY_Right,
    Qt.Key.Key_Down:       KEY_Down,
    Qt.Key.Key_F1:         KEY_F1,
    Qt.Key.Key_F2:         KEY_F2,
    Qt.Key.Key_F3:         KEY_F3,
    Qt.Key.Key_F4:         KEY_F4,
    Qt.Key.Key_F5:         KEY_F5,
    Qt.Key.Key_F6:         KEY_F6,
    Qt.Key.Key_F7:         KEY_F7,
    Qt.Key.Key_F8:         KEY_F8,
    Qt.Key.Key_F9:         KEY_F9,
    Qt.Key.Key_F10:        KEY_F10,
    Qt.Key.Key_F11:        KEY_F11,
    Qt.Key.Key_F12:        KEY_F12,
    Qt.Key.Key_F13:        KEY_F13,
    Qt.Key.Key_F14:        KEY_F14,
    Qt.Key.Key_F15:        KEY_F15,
    Qt.Key.Key_F16:        KEY_F16,
    Qt.Key.Key_F17:        KEY_F17,
    Qt.Key.Key_F18:        KEY_F18,
    Qt.Key.Key_F19:        KEY_F19,
    Qt.Key.Key_F20:        KEY_F20,
    Qt.Key.Key_Shift:      KEY_ShiftLeft,
    Qt.Key.Key_Control:    KEY_ControlLeft,
    Qt.Key.Key_Meta:       KEY_MetaLeft,
    Qt.Key.Key_Alt:        KEY_AltLeft,
    Qt.Key.Key_ScrollLock: KEY_Scroll_Lock,
    Qt.Key.Key_SysReq:     KEY_Sys_Req,
    Qt.Key.Key_NumLock:    KEY_Num_Lock,
    Qt.Key.Key_CapsLock:   KEY_Caps_Lock,
    Qt.Key.Key_Pause:      KEY_Pause,
    Qt.Key.Key_Super_L:    KEY_Super_L,
    Qt.Key.Key_Super_R:    KEY_Super_R,
    Qt.Key.Key_Hyper_L:    KEY_Hyper_L,
    Qt.Key.Key_Hyper_R:    KEY_Hyper_R,
    Qt.Key.Key_Enter:      KEY_KP_Enter,
}

# Authentication protocol types
AUTH_FAIL =		0
AUTH_NONE = 	1
AUTH_VNCAUTH = 	2

# Authentication result types
SMSG_AUTH_OK        = 0
SMSG_AUTH_FAIL      = 1
SMSG_AUTH_TOOMANY   = 2

# Server message types
SMSG_FBUPDATE = 		0
SMSG_SETCOLORMAP = 		1
SMSG_BELL = 			2
SMSG_SERVERCUTTEXT = 	3


# Client message types
CMSG_SETPIXELFORMAT = 	0
CMSG_SETENCODINGS =		2
CMSG_FBUPDATEREQ = 		3
CMSG_KEYEVENT =			4
CMSG_POINTEREVENT =		5
CMSG_CLIENTCUTTEXT =	6
