#include <hal/board.h>
#include <hal/irq.h>
#include <systime/systime.h>
//#include <sched/sched.h>

#include <drivers/serial/uartring.h>

#include <addons/ramps/ramps.h>

#include <drivers/timer/avr_timer.h>

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

	ramps::x_driver.enable();
	ramps::y_driver.enable();
	ramps::z_driver.enable();

	while (1) {
		board::sysled.toggle();
		//serial0.println("HelloWorld");
		//board::usart0.sendbyte('A');
		ramps::x_driver.step_toggle();
		ramps::y_driver.step_toggle();
		ramps::z_driver.step_toggle();

		delay(1);
	}
}