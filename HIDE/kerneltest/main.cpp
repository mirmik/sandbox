#include <hal/arch.h>
#include <debug/dprint.h>

#include <kernel/devices/serial/PipeStream.h>
#include <kernel/devices/serial/DebugStream.h>
#include <gxx/array.h>

#include <console/Terminal.h>
#include <kernel/sched/SchedeeManager.h>

#include <genos/banner.h>
#include <console/SimpleShell.h>
#include <drivers/serial/linux/Terminal.h>

#include <kernel/sched/SchedeeTable.h>

#include <kernel/event/WakeUpWaiter.h>

#include <kernel/pool/Pool.h>
#include <kernel/pool/Page.h>

#include <kernel/resources/ManagedObject.h>

#include <thread>
#include <chrono>

gxx::array<char, 128> arr;
gxx::array<char, 128> rlbuf;

Genos::SimpleShell shell;
Genos::DebugStream debugStream;

Genos::PipeStream pipeStream(arr.slice());
Genos::LinuxTerminal io;

//extern Genos::SchedeeTable schedeeTable;

class Thr2 : public Genos::AutomFunctorSchedee {
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
			//	final();
				break;

		}
	}
	
	void destroy() override {
		//dpr(m_name);dprln("::destroy");
		delete this;
	}
};

class Blinker : public Genos::AutomFunctorSchedee {
	uint8_t state = 0;
	Genos::pid_t child;

	Genos::WakeUpWaiter waiter;

public:
	Blinker() : waiter(this) {}

	void routine() override {
		switch (state) {
			case 0:
				child = Genos::automFunctorCreate<Thr2>();
				Genos::assign_name(child, "thr2");
				Genos::run(child); 

				Genos::wakeup_wait(child, waiter);

				state++; 
				break;
			case 1:
				dprln("child was stoped");
				state++;
				break;
			case 2:
				final();
				break;

		}
	}

	void destroy() override {
		//dpr(m_name);dprln("::destroy");
		delete this;
	}
};

class Hello: public Genos::AutomFunctorSchedee {
	void routine() override {
		dprln("helloWorld");
	};

	void destroy() override {
		//dpr(m_name); dprln("::destroy");
		delete this;
	}
};

extern Genos::SchedeeTable schedeeTable;
int print_schedee_table(int argc, char** argv);

pid_t blinker;

int create_blinker() {
	blinker = Genos::automFunctorCreate<Blinker>();
	Genos::assign_name(blinker, "blinker");
	Genos::run(blinker);
	return 0;
}

int create_hello() {
	pid_t pid = Genos::automFunctorCreate<Hello>();
	Genos::assign_name(pid, "hello");
	Genos::run(pid);
	return 0;
}

int kill(int argc, char** argv) {
	if (argc < 2) return Genos::SimpleShell::WrongArgsTotal;
	
	int a = atoi(argv[1]);

	if (a != 0) {
		return Genos::final(a);
	} 
	else {
		auto ret = Genos::Glue::systemSchedeeTable().find(
		[&argv](Genos::Schedee& sch){
			return !strcmp(sch.name(), argv[1]);
		});
		if (ret) {
			ret->final();
			//dprln("kill_end");
			return 0;
		}
		return Genos::SimpleShell::WrongArgsData;
	}	
}


int killall(int argc, char** argv) {
	if (argc < 2) return Genos::SimpleShell::WrongArgsTotal;

	Genos::Schedee* sch;
	Genos::Glue::systemSchedeeTable().foreach(
		[&argv](Genos::Schedee& sch)
	{
		if (!strcmp(sch.name(), argv[1])) {
			sch.final();
		}	
	});
	return 0;
}

Genos::Pool wwake_pool(sizeof(Genos::WakeUpWaiter), 10);


class A : public Genos::KernelObject<A> {
};

Genos::Pool apool(sizeof(A), 10);


void pools_init() {
	registry(wwake_pool, "wwake_pool");
	registry(apool, "apool");
}


namespace Genos { 
	namespace Glue {
		template<> A* getKernelObject<A>() {
			return (A*)apool.get();
		}

		template<> void putKernelObject<A>(A* a) {
			apool.put(a);
		}
	}
}

int main() {
	arch_init();
	pools_init();

	print_banner(io);
	print_about(io);
	
	A* a = A::engage();
	A* b = A::engage();
	
	a->release();
	b->release();

	shell.add("ps", print_schedee_table);

	shell.add("create", create_blinker);
	shell.add("create_hello", create_hello);
	shell.add("kill", kill);
	shell.add("killall", killall);

	shell.add("poolinfo", Genos::dbginfo_pool_list);


	pid_t terminal_pid = Genos::automFunctorCreate<Genos::Terminal>(&io, &io, &shell, rlbuf.slice());
	Genos::Terminal& terminal = *(Genos::Terminal*)Genos::raw(terminal_pid);
	terminal.echo(false);
	terminal.name("terminal");
	terminal.run();
	
	//wwake_pool.get();
	//wwake_pool.get();

	//wwake_pool.emplace<Genos::WakeUpWaiter>(nullptr);

	std::this_thread::sleep_for(std::chrono::milliseconds(100));

	while(1) Genos::Glue::schedule();
}

int print_schedee_table(int argc, char** argv) {
	Genos::Glue::systemSchedeeTable().foreach([](Genos::Schedee& sch){
		dpr(sch.pid); 
		dpr("\t");
		dpr(sch.state);
		dpr("\t"); 
		if(sch.name() != nullptr) dpr(sch.name());
		dpr("\t"); 
		auto parent = sch.parent;
		if (parent != nullptr) dpr(parent->name());
		dprln();
	});
}

Genos::Stream& Genos::Glue::debugStream() {
	return io;
}
