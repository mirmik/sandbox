avr-gcc -mmcu=atmega2560 -O0 -save-temps avr.cpp -o avr.elf
avr-objcopy -O ihex -j .text avr.elf avr.hex
