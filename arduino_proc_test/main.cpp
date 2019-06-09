#include <genos/hal/board.h>
#include <genos/hal/irqs.h>
#include <genos/time/systime.h>

#include <arch/i2c_automate.h>
#include <gxx/print.h>

#include <genos/schedule.h>
#include <genos/sched/tasklet.h>
#include <genos/sched/timer.h>
#include <genos/sched/schedee.h>

#include <genos/sched/process.h>

arch::i2c_automate i2c;

void error_handler() {
	dprln("error_handler");
}

char buf[64];

char stack[256];

void operation_finish_handler() {
	gxx::print_dump((const char*)buf, 2, 8);
}

void mainproc(void* arg);

int main() {
	board_init();
	//debug_blink();

	/*const char* str = "HelloWorld";
	i2c.error_handler = error_handler;
	i2c.operation_finish_handler = operation_finish_handler;
	i2c.init_master();
	i2c.start_write(0x60, str);*/

	genos::create_process(mainproc, nullptr, stack);

	genos::hal::irqs::enable();

	while(1) {
		genos::schedule();
	}
}

void mainproc(void* arg) {

	gxx::println("Mirmik was here");

	while(1);

}

void genos::schedule() {
	genos::tasklet_manager.exec();
	genos::timer_manager.exec();
	genos::schedee_manager.exec();
}