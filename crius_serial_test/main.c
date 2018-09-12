#include <hal/board.h>
#include <drivers/tty/tty.h>
#include <drivers/virtual/null.h>

int main() {
	board_init();

	register_null_device();

//	gpio_settings(GPIOB, 1<<7, GPIO_MODE_OUTPUT);
///	gpio_set_level(GPIOB, 1<<7, 1);

	while(1);

//	while(1) genos::schedule();
}
/*
void genos::schedule() {
	genos::tasklet_manager.execute();
	genos::timer_manager.execute();
	genos::schedee_manager.execute();
}*/