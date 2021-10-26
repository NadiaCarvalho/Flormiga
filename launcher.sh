#!/bin/bash

amixer -c0 set 'Headphone',0 100% && sudo /usr/bin/pd -nogui -verbose -open main.pd