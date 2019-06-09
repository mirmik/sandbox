#!/usr/bin/ruby

require "serialport"

sport = SerialPort.new("/dev/ttyUSB0", 115200)

loop do
	p sport.read 1	
end
	