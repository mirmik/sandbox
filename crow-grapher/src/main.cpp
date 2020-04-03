#include <QtWidgets>
#include <DisplayWidget.h>

#include <crow/hexer.h>
#include <crow/pubsub.h>
#include <crow/tower.h>
#include <crow/gates/udpgate.h>

#include <nos/print.h>
#include <nos/fprint.h>

std::vector<uint8_t> crowker;
crow::subscriber data_theme;

void data_theme_handler(crow::packet * pack) 
{
	crow::release(pack);
}

int main(int argc, char * argv []) 
{
	if (argc < 3) 
	{
		nos::println("Usage: {} crow_address theme", argv[0]);
	}

	//crow::diagnostic_enable();
	crow::create_udpgate(12, 0);

	crowker = compile_address(argv[1]);
	std::string theme = argv[2];

	crow::pubsub_protocol.enable();
	crow::pubsub_protocol.start_resubscribe_thread(1000);
	
	data_theme.subscribe(crowker, theme.c_str(), 0, 200, data_theme_handler);

	crow::start_thread();

	QApplication app(argc, argv);
	DisplayWidget w;

	w.show();
	app.exec();
}