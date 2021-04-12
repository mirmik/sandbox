#include <stdlib.h>
#include <stdio.h>

volatile int i = 0;
int main() 
{
	void * volatile ptr = malloc(10);
	(void) ptr;
	i = 42;

}

void * malloc(size_t size) { return NULL; }

void _exit(int i) 
{
	while(1) {}
}