#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

mkdir /usr/sbin/ipmilcd
cp ipmilcd.py lcd.pl /usr/sbin/ipmilcd
cp ipmilcd.service /etc/systemd/system
systemctl daemon-reload
systemctl enable ipmilcd.service
