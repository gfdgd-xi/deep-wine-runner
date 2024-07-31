#! /usr/bin/env python3

import struct

##
# reading
##

def read_float_buff(buffer, big_endian=False) -> float:
    if big_endian:
        return struct.unpack(">f", buffer.read(4))[0]
    else:
        return struct.unpack("<f", buffer.read(4))[0]

def read_double_buff(buffer, big_endian=False) -> float:
    if big_endian:
        return struct.unpack(">d", buffer.read(8))[0]
    else:
        return struct.unpack("<d", buffer.read(8))[0]


def read_uint8_buff(buffer, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">B", buffer.read(1))[0]
    else:
        return struct.unpack("<B", buffer.read(1))[0]

def read_uint16_buff(buffer, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">H", buffer.read(2))[0]
    else:
        return struct.unpack("<H", buffer.read(2))[0]

def read_uint32_buff(buffer, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">I", buffer.read(4))[0]
    else:
        return struct.unpack("<I", buffer.read(4))[0]

def read_uint64_buff(buffer, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">Q", buffer.read(8))[0]
    else:
        return struct.unpack("<Q", buffer.read(8))[0]


def read_sint8_buff(buffer, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">b", buffer.read(1))[0]
    else:
        return struct.unpack("<b", buffer.read(1))[0]

def read_sint16_buff(buffer, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">h", buffer.read(2))[0]
    else:
        return struct.unpack("<h", buffer.read(2))[0]

def read_sint32_buff(buffer, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">i", buffer.read(4))[0]
    else:
        return struct.unpack("<i", buffer.read(4))[0]

def read_sint64_buff(buffer, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">q", buffer.read(8))[0]
    else:
        return struct.unpack("<q", buffer.read(8))[0]

##
# writing
##

def write_float_buff(buffer, value: float, big_endian=False) -> None:
    buffer.write(return_float_bytes(value, big_endian))

def write_double_buff(buffer, value: float, big_endian=False) -> None:
    buffer.write(return_double_bytes(value, big_endian))


def write_uint8_buff(buffer, value: int, big_endian=False) -> None:
    buffer.write(return_uint8_bytes(value, big_endian))

def write_uint16_buff(buffer, value: int, big_endian=False) -> None:
    buffer.write(return_uint16_bytes(value, big_endian))

def write_uint32_buff(buffer, value: int, big_endian=False) -> None:
    buffer.write(return_uint32_bytes(value, big_endian))

def write_uint64_buff(buffer, value: int, big_endian=False) -> None:
    buffer.write(return_uint64_bytes(value, big_endian))


def write_sint8_buff(buffer, value: int, big_endian=False) -> None:
    buffer.write(return_sint8_bytes(value, big_endian))

def write_sint16_buff(buffer, value: int, big_endian=False) -> None:
    buffer.write(return_sint16_bytes(value, big_endian))

def write_sint32_buff(buffer, value: int, big_endian=False) -> None:
    buffer.write(return_sint32_bytes(value, big_endian))

def write_sint64_buff(buffer, value: int, big_endian=False) -> None:
    buffer.write(return_sint64_bytes(value, big_endian))

##
# return bytes
##

def return_float_bytes(value: float, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">f", value)
    else:
        return struct.pack("<f", value)

def return_double_bytes(value: float, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">d", value)
    else:
        return struct.pack("<d", value)


def return_uint8_bytes(value: int, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">B", value)
    else:
        return struct.pack("<B", value)

def return_uint16_bytes(value: int, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">H", value)
    else:
        return struct.pack("<H", value)

def return_uint32_bytes(value: int, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">I", value)
    else:
        return struct.pack("<I", value)

def return_uint64_bytes(value: int, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">Q", value)
    else:
        return struct.pack("<Q", value)


def return_sint8_bytes(value: int, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">b", value)
    else:
        return struct.pack("<b", value)

def return_sint16_bytes(value: int, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">h", value)
    else:
        return struct.pack("<h", value)

def return_sint32_bytes(value: int, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">i", value)
    else:
        return struct.pack("<i", value)

def return_sint64_bytes(value: int, big_endian=False) -> bytes:
    if big_endian:
        return struct.pack(">q", value)
    else:
        return struct.pack("<q", value)

##
# return val
##

def return_float_val(data: bytes, big_endian=False) -> float:
    if big_endian:
        return struct.unpack(">f", data)[0]
    else:
        return struct.unpack("<f", data)[0]

def return_double_val(data: bytes, big_endian=False) -> float:
    if big_endian:
        return struct.unpack(">d", data)[0]
    else:
        return struct.unpack("<d", data)[0]


def return_uint8_val(data: bytes, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">B", data)[0]
    else:
        return struct.unpack("<B", data)[0]

def return_uint16_val(data: bytes, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">H", data)[0]
    else:
        return struct.unpack("<H", data)[0]

def return_uint32_val(data: bytes, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">I", data)[0]
    else:
        return struct.unpack("<I", data)[0]

def return_uint64_val(data: bytes, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">Q", data)[0]
    else:
        return struct.unpack("<Q", data)[0]


def return_sint8_val(data: bytes, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">b", data)[0]
    else:
        return struct.unpack("<b", data)[0]

def return_sint16_val(data: bytes, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">h", data)[0]
    else:
        return struct.unpack("<h", data)[0]

def return_sint32_val(data: bytes, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">i", data)[0]
    else:
        return struct.unpack("<i", data)[0]

def return_sint64_val(data: bytes, big_endian=False) -> int:
    if big_endian:
        return struct.unpack(">q", data)[0]
    else:
        return struct.unpack("<q", data)[0]
