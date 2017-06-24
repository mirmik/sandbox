#include <QtCore>
#include <QtWidgets>
#include <ColorSlider.h>
#include <CentralFrame.h>



int main(int argc, char* argv[]) {
	QApplication app(argc, argv);

	qDebug("HelloWorld");
	
	QSplitter mainspl;
	
	RGBAPanel* rgba = new RGBAPanel;
	HSVAPanel* hsva = new HSVAPanel;
	CentralFrame* cfrm = new CentralFrame;

	QObject::connect(rgba, SIGNAL(valueChanged(QColor)), cfrm, SLOT(updateColor(QColor)));
	QObject::connect(hsva, SIGNAL(valueChanged(QColor)), cfrm, SLOT(updateColor(QColor)));
	QObject::connect(cfrm, SIGNAL(colorChanged(QColor)), rgba, SLOT(setColor(QColor)));
	QObject::connect(cfrm, SIGNAL(colorChanged(QColor)), hsva, SLOT(setColor(QColor)));

	cfrm->updateColor(QColor(0,0,0,255));

	QWidget* leftpanel = new QWidget;
	QVBoxLayout* lpanellayout = new QVBoxLayout;
	leftpanel -> setLayout(lpanellayout);
	lpanellayout -> addWidget(rgba);
	lpanellayout -> addStretch(1);
	
	QWidget* rightpanel = new QWidget;
	QVBoxLayout* rpanellayout = new QVBoxLayout;
	rightpanel -> setLayout(rpanellayout);
	rpanellayout -> addWidget(hsva);
	rpanellayout -> addStretch(1);

	mainspl.addWidget(leftpanel);
	mainspl.addWidget(cfrm);
	mainspl.addWidget(rightpanel);

	mainspl.resize(880,480);

	mainspl.setStretchFactor(0, 1);
	mainspl.setStretchFactor(1, 1);
	mainspl.setStretchFactor(2, 1);
	
	mainspl.show();
	return app.exec();
}