#include <QtWidgets>
#include <DisplayWidget.h>

#include <crow/hexer.h>
#include <crow/pubsub.h>
#include <crow/tower.h>

std::vector<uint8_t> crowker;

int main(int argc, char * argv []) 
{
	crow::pubsub_protocol.enable();
	crowker = compile_address(argv[1]);

	QApplication app(argc, argv);
	DisplayWidget w;

	w.show();
	app.exec();
}