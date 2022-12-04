#!/bin/bash
echo -e "123456\n123456\n\n\n\n\n\n\n\n\n" | adduser "$1"
echo -e "123456\n123456\n" | passwd root