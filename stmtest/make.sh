arm-none-eabi-gcc -mthumb -Os -save-temps main.c -o stm.elf
avr-objcopy -O ihex -j .text stm.elf stm.hex
