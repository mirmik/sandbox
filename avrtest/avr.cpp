#include <avr/io.h>
<<<<<<< HEAD
#include <stdlib.h>
#include <stdio.h>
#include <avr/interrupt.h>


extern "C" 
void ADC_vect (void) __attribute__ ((signal, used, externally_visible));
void ADC_vect(void)
{
    // user code here
=======


void cpu_delay(long long arg) 
{
	volatile long long i = arg;
	while(i--);
>>>>>>> ebeceb755c3706d8927381201430bc5adef8a72b
}

int main(void)
{
<<<<<<< HEAD
=======
	DDRB = 0xFF;
	PORTB = 0xff;

	while (1)
	{
		cpu_delay(100000);
		PORTB = 0x00;

		cpu_delay(100000);
		PORTB = 0xff;
	}
>>>>>>> ebeceb755c3706d8927381201430bc5adef8a72b
}