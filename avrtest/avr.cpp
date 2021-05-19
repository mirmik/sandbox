#include <avr/io.h>
#include <stdlib.h>
#include <stdio.h>
#include <avr/interrupt.h>


extern "C" 
void ADC_vect (void) __attribute__ ((signal, used, externally_visible));
void ADC_vect(void)
{
    // user code here
}

int main(void)
{
}