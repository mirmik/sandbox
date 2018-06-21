#include <genos/hal/board.h>
#include <genos/hal/irqs.h>
#include <genos/systime.h>

#include <gxx/debug/dprint.h>

#include <g1/tower.h>
#include <g1/gates/uartgate.h>


void incoming_handler(g1::packet* pack);

int main() {
	board_init();
	genos::hal::irqs::enable();

	g1::incoming_handler = incoming_handler;

	auto* pack = g1::create_packet(nullptr, 0, 10);
	memcpy(pack->dataptr(), "HelloWorld", 10);

	g1::transport(pack);

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