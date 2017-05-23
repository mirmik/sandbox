#include <hal/board.h>
#include <hal/irq.h>

#include <kernel/utility/utility.h>

#include <debug/dprint.h>
#include <drivers/gpiotbl.h>

#include <gxx/array.h>
#include <genos/banner.h>

#include <console/Terminal.h>
#include <kernel/devices/serial/Stream.h>
#include <kernel/devices/serial/PipeStream.h>
#include <kernel/sched/SchedeeTable.h>

#include <drivers/serial/avr/UsartStream.h>

#include <console/SimpleShell.h>
#include <console/Terminal.h>

#include <boardUtility.h>

#include <kernel/resources/File.h>

//#include <kernel/service/MsgTag.h>

//Genos::DebugExecutor debugExecutor;
Genos::SimpleShell shell; 

//Genos::DebugStream debugStream;
//Genos::PipeStream pipeStream((new gxx::array<char, 256>)->slice());

gxx::array<char, 256> rxbuf, txbuf;
gxx::array<char, 128> rlbuf;

Genos::AvrUsartStream io(usart0_data, rxbuf.slice(), txbuf.slice());
Genos::Terminal terminal(&io, &io, &shell, (new gxx::array<char, 64>)->slice());

int hello(int argc, char** argv) {
	dprln("HelloWorld");
	return Genos::SimpleShell::OK;
}

class TestThread : public Genos::AutomFunctorSchedee {
	uint8_t state = 0;
	
	void routine() override {
		switch (state) {
			case 0: 
				state++; 
				break;
			case 1:
				state++;
				break;
			case 2:
				break;
		}
	}
	
	void destroy() override { delete this; }
};

Genos::StdStreamStruct base_strms = { &io, &io };

int main() {
	board_init();
	global_irqs_enable();

	io.begin(115200);
	currentStdStream(&base_strms);

	try {

	} catch (int i) {
		
	}

	print_banner(io);
	print_about(io);

	io.println("HelloWorld");

	Genos::pid_t terminal_pid = Genos::automFunctorCreate<Genos::Terminal>(&io, &io, &shell, rlbuf.slice());
	Genos::Terminal& terminal = *(Genos::Terminal*)Genos::raw(terminal_pid);
	terminal.echo(true);
	terminal.name("terminal");
	terminal.run();

	Genos::utility::addKernelUtility(shell);
	Genos::utility::addBoardUtility(shell);

	while(1) {
		Genos::Glue::schedule();
	}
}