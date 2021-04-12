avr-gcc -mmcu=atmega2560 -Os -save-temps avr.cpp -o avr.elf
avr-objcopy -O ihex -j .text avr.elf avr.hex
