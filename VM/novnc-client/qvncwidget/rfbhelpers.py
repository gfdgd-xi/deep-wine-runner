
import logging
import qvncwidget.rfbconstants as c

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt

class RFBPixelformat:
    def __init__(self,
        bpp=32, depth=24, bigendian=False, truecolor=True,
        redmax=255, greenmax=255, bluemax=255,
        redshift=0, greenshift=0, blueshift=16):

        self.bitspp = bpp
        self.depth = depth
        self.bigendian = 1 if bigendian else 0
        self.truecolor = 1 if truecolor else 0

        self.redmax = redmax
        self.greenmax = greenmax
        self.bluemax = bluemax
        
        self.redshift = redshift
        self.greenshift = greenshift
        self.blueshift = blueshift

    @staticmethod
    def getRGB32():
        return RFBPixelformat(
            bpp=32, depth=32,
            redshift=16, greenshift=8, blueshift=0
        )

    @staticmethod
    def getRGB16():
        return RFBPixelformat(
            bpp=16, depth=16,
            redmax=31, greenmax=63, bluemax=31,
            redshift=11, greenshift=5, blueshift=0
        )

    @staticmethod
    def getRGB555():
        return RFBPixelformat(
            bpp=16, depth=15,
            redmax=31, greenmax=31, bluemax=31,
            redshift=10, greenshift=5, blueshift=0
        )

    def asTuple(self) -> tuple:
        return (
            self.bitspp, self.depth, self.bigendian, self.truecolor,
            self.redmax, self.greenmax, self.bluemax,
            self.redshift, self.greenshift, self.blueshift
        )

    def __str__(self) -> str:
        return ";".join(str(x) for x in self.asTuple())

class RFBRectangle:
    def __init__(self, xPos: int, yPos: int, width: int, height: int):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height

    def asTuple(self) -> tuple:
        return (self.xPos, self.yPos, self.width, self.height)

    def __str__(self) -> str:
        return f"x: {self.xPos} y: {self.yPos} width: {self.width} height: {self.height}"

class RFBInput:

    # thanks to ken3 (https://github.com/ken3) for this
    MOUSE_MAPPING = {
        Qt.LeftButton: 1 << 0,
        Qt.MidButton: 1 << 1,
        Qt.RightButton: 1 << 2,
    }

    @staticmethod
    def fromQKeyEvent(eventID: int, eventStr: str) -> int:
        rfbKey = c.KEY_TRANSLATION_SPECIAL.get(eventID)

        if not rfbKey:
            try:
                rfbKey = ord(eventStr)
            except TypeError:
                logging.warning(f"Unknown keytype: {eventID} | {eventStr}")
                return 0

        return rfbKey

    @staticmethod
    def fromQMouseEvent(eventID: QMouseEvent, pressEvent: bool, mask) -> int:
        _mask = RFBInput.MOUSE_MAPPING.get(eventID.button())

        # FIXME: return previous bitmask in case unknown key is pressed
        # TODO: implement all RFB supported buttons
        if not _mask: return mask
        
        if pressEvent:
            return mask | _mask
        else:
            return mask & ~_mask
