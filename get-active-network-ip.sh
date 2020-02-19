#!/usr/bin/env bash

for interface in $(ifconfig | grep ^en | cut -d: -f1)
do
  ipconfig getifaddr $interface
done
