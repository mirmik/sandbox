#include <hal/board.h>
#include <hal/irq.h>
#include <systime/systime.h>
//#include <sched/sched.h>

#include <drivers/serial/uartring.h>

#include <addons/ramps/ramps.h>

#include <math.h>
#include <nos/print.h>

#include <ralgo/planning/traj.h>

//genos::uartring serial0;
//char rxbuf[16];
//char txbuf[128];

//int i = 0;

ramps::ramps_driver rampsdrv(&periph::timer1);

//void handler(void*) 
//{
//	i++;
	//if (i == 10) {
//		board::sysled.toggle();
//		i = 0;
	//}
//}

int main() 
{
	board_init();
	board::usart0.setup(115200);
	board::usart0.enable();
	//serial0.init(&board::usart0, rxbuf, 16, txbuf, 128);

	rampsdrv.init(4000, 8);

	ramps::x_driver.enabled=true;
	ramps::y_driver.enabled=true;
	ramps::z_driver.enabled=true;
	
	irqs_enable();

	auto traj0 = ralgo::accdcc_by_time_trajectory<>(0, 50000, 3000, 10000, 3000); 
	auto traj1 = ralgo::accdcc_by_time_trajectory<>(0, 25000, 3000, 10000, 3000); 
	auto traj2 = ralgo::accdcc_by_time_trajectory<>(0, 12500, 3000, 10000, 3000); 

	delay(1000);

	ralgo::phase<> phs0, phs1, phs2;
	auto stime = millis();
	while(1) 
	{
		auto tm = millis() - stime;
		traj0.inloctime_placed(tm, &phs0);
		traj1.inloctime_placed(tm, &phs1);
		traj2.inloctime_placed(tm, &phs2);
		ramps::x_driver.write(phs0.d0, phs0.d1);
		ramps::y_driver.write(phs1.d0, phs1.d1);
		ramps::z_driver.write(phs2.d0, phs2.d1);

		//ramps::z_driver.print_state();
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