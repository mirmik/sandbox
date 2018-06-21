#include <genos/hal/board.h>
#include <genos/hal/irqs.h>
#include <genos/systime.h>

#include <gxx/debug/dprint.h>

#include <g1/tower.h>
//#include <g1/gates/uartgate.h>


void incoming_handler(g1::packet* pack);

int main() {
	board_init();
	g1::incoming_handler = incoming_handler;

	//gxx::println("mirmik");

	genos::hal::irqs::enable();

	g1::send(nullptr, 0, "HelloWorld", 10, 1, (g1::QoS)0, 20);
	g1::spin();
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