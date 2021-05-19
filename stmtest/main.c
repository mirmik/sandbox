#include <stdlib.h>
#include <stdio.h>

volatile int i = 0;
int main() 
{
	i = 42;
	while(1);
}

void * malloc(size_t size) { return NULL; }

void _exit(int i) 
{
	while(1) {}
}