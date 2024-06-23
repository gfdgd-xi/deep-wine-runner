#!/bin/bash
bottlePath=./system-bottle
gitPath=deep-wine-runner-qemu-system
sudo chroot $bottlePath bash -c "cd $gitPath ; $@"