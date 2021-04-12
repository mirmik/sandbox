#include <avr/io.h>
#include <stdlib.h>
#include <stdio.h>

volatile int k;
class A 
{
public:
	A() {k = 22;}
};

A b;

int main(void)
{
//	A a;

	volatile int i;
	DDRB = 0xFF;

	void * volatile ptr = malloc(18);

	printf("hello");

	while (1)
	{
		PORTB ^= 0xFF;
		for (i = 0; i < 1000; i++); // a fake delay
	}
}