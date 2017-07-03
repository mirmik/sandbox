#include <QtWidgets>
#include <ImageBoard.h>
#include <FirstCore.h>
#include <Matrix.h>

ImageBoard* result;
ImageBoard* board;
	
void evaluate() {
	qDebug("evaluate");

	auto imag = board->getImage();

	OpenRectanglePattern task(8, 4, 8, M_PI / 4);


	QPainter painter;

	painter.begin(result->getImage());
	draw(painter, result->rect().center(), task);
	painter.end();

	result->repaint();



	//FirstCore fcore(*imag);

	//fcore.evaluate();
}

int main(int argc, char* argv[]) {
	QApplication app(argc, argv);

	QWidget* mainwindow = new QWidget;
	result = new ImageBoard;
	
	QHBoxLayout* mainlayout = new QHBoxLayout;
	QVBoxLayout* layout = new QVBoxLayout;
	QHBoxLayout* button_layout = new QHBoxLayout;
	
	QPushButton* button = new QPushButton("StartEvaluation");
	board = new ImageBoard;
	
	board->setFixedSize(600,600);
	result->setFixedSize(600,600);

	button_layout->addStretch();
	button_layout->addWidget(button);
	button_layout->addStretch();

	layout->addWidget(board);
	layout->addLayout(button_layout);

	mainlayout->addLayout(layout);
	mainlayout->addWidget(result);

	QObject::connect(button, &QPushButton::clicked, evaluate);

	mainwindow->setLayout(mainlayout);
	mainwindow->show();

	return app.exec();
}