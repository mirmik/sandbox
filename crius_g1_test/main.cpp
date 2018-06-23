#include <genos/hal/board.h>
#include <genos/hal/irqs.h>
#include <genos/time/systime.h>

#include <gxx/debug/dprint.h>

#include <g1/tower.h>
#include <g1/indexes.h>
#include <g0/services/echo.h>
#include <genos/drivers/g1/uartgate.h>

#include <genos/sched/schedee.h>
#include <genos/sched/tasklet.h>
#include <genos/sched/timer.h>
#include <genos/sched/action.h>
#include <genos/schedule.h>

arch::usart usart0(usart0_data);
genos::uartgate usart0gate(&usart0, 128);

int idx = 0;
int idx2 = 0;
void incoming_handler(g1::packet* pack);
void led_toggle() { 
	board::led.tgl(); 
}

void tim1func() { 
	char arr[40] = "Mirmik was here ";
	i32toa(idx++, arr + strlen(arr), 10);
	g0::send(0, 0, "\x42\x0C\xC0\xA8\x01\x87\x27\x14\x0C\xC0\xA8\x01\xF0\x27\x14", 15, arr, strlen(arr), g1::QoS(2), 100);
}

void tim2func() { 
	char arr[20];
	i32toa(idx2++, arr, 10);
	g0::send(0, 0, "\x42", 1, arr, strlen(arr), g1::QoS(2), 100);
	g0::send(0, 0, "\x42\x0C\xC0\xA8\x01\x87\x27\x14", 8, arr, strlen(arr), g1::QoS(2), 100);
}

g0::echo_service echo(true);

int main() {
	board_init();
	usart0.enable(false);
	g1::link_gate(&usart0gate, 0x42);
	g0::link_service(&echo, 2);

	usart0.setup(115200);
	usart0gate.init();
	usart0.enable();

	g1::incoming_handler = incoming_handler;

	genos::timer_tasklet tim2(tim2func, 1000);
	tim2.autorepeat(true).plan();
	genos::timer_tasklet tim1(tim1func, 30);
	tim1.autorepeat(true).plan();

	genos::hal::irqs::enable();

	//g1::send("\x42", 1, "Hello\xACW\xADo\xAEr\xAFld", 14, 1, (g1::QoS)1);


	while(1) genos::schedule();

}

void incoming_handler(g1::packet* pack) {
	if (pack->header.type == G1_G0TYPE) {
		g0::travell(pack);
	} else {
		g1::release(pack);
	}
}

namespace g1 {
	uint16_t millis() {
		return systime::millis();
	}
}

void genos::schedule() {
	g1::onestep();
	genos::tasklet_manager.execute();
	genos::timer_manager.execute();
	genos::schedee_manager.execute();
}