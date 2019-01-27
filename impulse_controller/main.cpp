#include <hal/board.h>
#include <hal/irq.h>
#include <systime/systime.h>
//#include <sched/sched.h>

#include <drivers/serial/uartring.h>

#include <addons/ramps/ramps.h>

#include <drivers/timer/avr_timer.h>

#include <math.h>

uartring serial0;
char rxbuf[16];
char txbuf[128];

int i = 0;

void handler(void*) 
{
	i++;
	//if (i == 10) {
		board::sysled.toggle();
		i = 0;
	//}
}

int main() 
{
	board_init();
	board::usart0.setup(115200);
	board::usart0.enable();
	serial0.init(&board::usart0, rxbuf, 16, txbuf, 128);

	PINOUT[11].mode(GPIO_MODE_OUTPUT);

	periph::timer1.set_overflow_irq_handler(handler, &periph::timer1);

	periph::timer1.irq_ovf_enable(true);

	periph::timer1.set_wgm(0b0111);

	//periph::timer1.set_compare_a(255);
	periph::timer1.set_compare_a(0x3ff / 2);
	periph::timer1.set_output_a_mode(0b10);

	periph::timer1.enable(256);

	periph::timer1.debug_print_regs();


	//periph::timer1.irq_overflow_enable(true);

	//pinMode(24, 1);
	//digitalWrite(24, 1);
//	schedee_manager_init();
	irqs_enable();


	while(1) 
	{
		auto m = millis() % 1000;
		float a = (float)m / 1000 * M_PI * 2;
		periph::timer1.set_compare_a(0x3ff / 2 + sin(a)*0x100);
		//delay(100);
	}


	/*board::usart0.setup(115200);
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
	}*/
}