#!/bin/sh

for F in `ls -1d /sys/class/gpio/gpio*`; do :
  GPIO=`echo $F | sed 's/^[^0-9]*//'`
  echo "$F // $GPIO"
  echo $GPIO >/sys/class/gpio/unexport 2>/dev/null
done
