#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

mkdir /usr/sbin/ipmilcd
g++ lcd.cpp -o /usr/sbin/ipmilcd/lcd
cp ipmilcd.py /usr/sbin/ipmilcd
cp ipmilcd.service /etc/systemd/system
systemctl daemon-reload
systemctl enable ipmilcd.service --now
