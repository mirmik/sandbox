#include <avr/io.h>


void cpu_delay(long long arg) 
{
	volatile long long i = arg;
	while(i--);
}

int main(void)
{
	DDRB = 0xFF;
	PORTB = 0xff;

	while (1)
	{
		cpu_delay(100000);
		PORTB = 0x00;

		cpu_delay(100000);
		PORTB = 0xff;
	}
}