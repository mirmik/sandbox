#include <hal/board.h>
#include <hal/irq.h>
#include <systime/systime.h>
//#include <sched/sched.h>

#include <drivers/serial/uartring.h>

uartring serial0;
char rxbuf[16];
char txbuf[128];

int main() 
{
	board_init();
//	schedee_manager_init();

	board::usart0.setup(115200);
	board::usart0.enable();

	serial0.init(&board::usart0, rxbuf, 16, txbuf, 128);

	irqs_enable();

	while (1) {
		board::sysled.toggle();

		serial0.println("HelloWorld");
		//board::usart0.sendbyte('A');

		delay(1000);
	}
}