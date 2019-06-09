#include <genos/hal/board.h>
#include <genos/hal/irqs.h>
#include <genos/time/systime.h>

#include <gxx/debug/dprint.h>

#include <crow/tower.h>
#include <crow/node.h>

#include <crow/nodes/echo.h>

#include <genos/drivers/g1/uartgate.h>

#include <genos/sched/schedee.h>
#include <genos/sched/tasklet.h>
#include <genos/sched/timer.h>
#include <genos/sched/action.h>
#include <genos/schedule.h>

genos::uartgate usart0gate(&board::usart0, 128);

int idx = 0;
int idx2 = 0;
void incoming_handler(crow::packet* pack);
void led_toggle() { 
	board::led.tgl(); 
}

void tim1func() { 
	char arr[40] = "Mirmik was here \n";
	i32toa(idx++, arr + strlen(arr), 10);
	//crow::__node_send(0, 0, "\x42\x0C\xC0\xA8\x01\x87\x27\x14\x0C\xC0\xA8\x01\xF0\x27\x14", 15, arr, strlen(arr), crow::QoS(2), 100);
}

void tim2func() { 
	char arr[20];
	i32toa(idx2++, arr, 10);
	//crow::__node_send(0, 0, "\x42", 1, arr, strlen(arr), crow::QoS(2), 100);
	//crow::__node_send(0, 0, "\x42\x0C\xC0\xA8\x01\x87\x27\x14", 8, arr, strlen(arr), crow::QoS(2), 100);
}

crow::echo_node echo(true);

int main() {
	board_init();
	board::usart0.enable(false);
	crow::link_gate(&usart0gate, 0x42);
	crow::link_node(&echo, 2);

	board::usart0.setup(115200);
	usart0gate.init();
	board::usart0.enable();

	genos::timer_tasklet tim2(tim2func, 1000);
	tim2.autorepeat(true).plan();
	genos::timer_tasklet tim1(tim1func, 300);
	tim1.autorepeat(true).plan();

	genos::hal::irqs::enable();

	//crow::send("\x42", 1, "Hello\xACW\xADo\xAEr\xAFld", 14, 1, (crow::QoS)1);


	while(1) genos::schedule();

}

namespace crow {
	uint16_t millis() {
		return systime::millis();
	}
}

void genos::schedule() {
	crow::onestep();
	genos::tasklet_manager.execute();
	genos::timer_manager.execute();
	genos::schedee_manager.execute();
}