#include <genos/hal/board.h>
#include <genos/hal/irqs.h>
#include <genos/systime.h>

#include <gxx/debug/dprint.h>

#include <g1/tower.h>
//#include <g1/gates/uartgate.h>

#include <genos/sched/schedee.h>
#include <genos/sched/tasklet.h>
#include <genos/sched/timer.h>

#include <genos/schedule.h>

void incoming_handler(g1::packet* pack);

void led_toggle() {
	dprln("ledtoggle");
	board::led.tgl();
};


int main() {
	board_init();

	g1::incoming_handler = incoming_handler;

	genos::timer ledtim(led_toggle, 1000);
	ledtim.autorepeat(true).plan();

	genos::hal::irqs::enable();

	//g1::send(nullptr, 0, "HelloWorld", 10);
	//g1::spin();

	//while(1) 
	//dprln(systime::now());
	while(1) genos::schedule();

}

void incoming_handler(g1::packet* pack) {
	debug_write(pack->dataptr(), pack->datasize());
	board::led.clr();
	g1::release(pack);
}

namespace g1 {
	uint16_t millis() {
		return systime::millis();
	}
}

void genos::schedule() {
	genos::tasklet_manager.execute();
	genos::timer_manager.execute();
	genos::schedee_manager.execute();
}