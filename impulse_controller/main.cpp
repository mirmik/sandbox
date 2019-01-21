#include <hal/board.h>
#include <hal/irq.h>
#include <systime/systime.h>
//#include <sched/sched.h>

#include <drivers/serial/uartring.h>
#include <drivers/gpio/arduino_pinout.h>

uartring serial0;
char rxbuf[16];
char txbuf[128];

int main() 
{
	board_init();

	//pinMode(24, 1);
	//digitalWrite(24, 1);
//	schedee_manager_init();

	board::usart0.setup(115200);
	board::usart0.enable();

	serial0.init(&board::usart0, rxbuf, 16, txbuf, 128);

	irqs_enable();
	delay(1000);

	pinMode(24, 1); //enable
	pinMode(26, 1); //step
	pinMode(28, 1); //dir
	digitalWrite(24, 0);
	digitalWrite(28, 0);

	while (1) {
		//board::sysled.toggle();
		//serial0.println("HelloWorld");
		//board::usart0.sendbyte('A');
		PINOUT[26].tgl();

		delay(1);
	}
}