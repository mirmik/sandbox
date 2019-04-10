#include <hal/board.h>
#include <hal/irq.h>
#include <systime/systime.h>
//#include <sched/sched.h>

#include <drivers/serial/uartring.h>

#include <addons/ramps/ramps.h>

#include <math.h>
#include <nos/print.h>

#include <ralgo/planning/traj.h>
#include <ralgo/servo/servo.h>

genos::uartring serial0;
char rxbuf[16];
char txbuf[128];

ramps::ramps_driver rampsdrv(&periph::timer1);

int main() 
{
	ralgo::servo<> xservo;

	board_init();
	board::usart0.setup(115200);
	board::usart0.enable();
	serial0.init(&board::usart0, rxbuf, 16, txbuf, 128);

	rampsdrv.init(4000, 8);

	ramps::x_driver.enabled=true;
	//ramps::y_driver.enabled=true;
	//ramps::z_driver.enabled=true;
	
	xservo.writer = &ramps::x_driver;

	irqs_enable();

	delay(1000);

	xservo.move_mode_speed = 2;
	xservo.move_mode_acctime = 1000;

	xservo.relative_move(30000);

	while(1) 
	{
		time_t curtime = millis();
		xservo.serve(curtime);
	}
}

void emergency_stop() 
{
	irqs_disable();
	abort();
}