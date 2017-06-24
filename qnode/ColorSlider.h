#pragma once

#include <QtWidgets>

class ColorSlider : public QWidget {
	Q_OBJECT

	QLayout* layout;
	QLabel* name;
	QSlider* slider;
	QLabel* label;

public:

	ColorSlider(QString namestr, QWidget* parent = nullptr) : QWidget(parent) {
		layout = new QHBoxLayout;
		slider = new QSlider(Qt::Horizontal);
		label = new QLabel("0");
		name = new QLabel(namestr + ':');

		slider -> setRange(0,255);
		QObject::connect(slider, SIGNAL(valueChanged(int)), label, SLOT(setNum(int)));

		label -> setFixedWidth(25);

		layout -> addWidget(name);
		layout -> addWidget(slider);
		layout -> addWidget(label);

		QObject::connect(slider, SIGNAL(valueChanged(int)), this, SIGNAL(valueChanged(int)));


		setLayout(layout);
	}

	void setValue(int val) {
		slider->setValue(val);
		emit valueChanged(val);
	}

	int value() { return slider->value(); }

signals:
	void valueChanged(int i);
};

class RGBAPanel : public QWidget {
	Q_OBJECT

	ColorSlider* rsld;
	ColorSlider* gsld;
	ColorSlider* bsld;
	ColorSlider* asld;

	QColor currentColor;

public:

	RGBAPanel(QWidget* parent = nullptr) : QWidget(parent) {
		QVBoxLayout* layout = new QVBoxLayout;
		
		rsld = new ColorSlider("R");
		gsld = new ColorSlider("G");
		bsld = new ColorSlider("B");
		asld = new ColorSlider("A");

		layout -> addWidget(rsld);
		layout -> addWidget(gsld);
		layout -> addWidget(bsld);
		layout -> addWidget(asld);

		setLayout(layout);
		setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);

		QObject::connect(rsld, SIGNAL(valueChanged(int)), this, SLOT(changePart(int)));
		QObject::connect(gsld, SIGNAL(valueChanged(int)), this, SLOT(changePart(int)));
		QObject::connect(bsld, SIGNAL(valueChanged(int)), this, SLOT(changePart(int)));
		QObject::connect(asld, SIGNAL(valueChanged(int)), this, SLOT(changePart(int)));
	}

	bool updateFlag = false;

signals:
	void valueChanged(QColor);

public slots:
	void setColor(QColor color) {
		if (currentColor == color) return;

		currentColor = color;
		updateFlag = true;

		int r, g, b, a;
		color.getRgb(&r, &g, &b, &a);

		rsld -> setValue(r);
		gsld -> setValue(g);
		bsld -> setValue(b);
		asld -> setValue(a);

		updateFlag = false;
		emit valueChanged(currentColor);
	} 

	void changePart(int i) {
		(void)i;
		if (updateFlag == true) return;
		//qDebug("changePart");

		int r = rsld->value();
		int g = gsld->value();
		int b = bsld->value();
		int a = asld->value();

		auto qc = QColor();
		qc.setRgb(r,g,b,a);
		currentColor = qc;
		emit valueChanged(qc);
	}
};

class HSVAPanel : public QWidget {
	Q_OBJECT

	ColorSlider* hsld;
	ColorSlider* ssld;
	ColorSlider* vsld;
	ColorSlider* asld;

	QColor currentColor;

public:

	HSVAPanel(QWidget* parent = nullptr) : QWidget(parent) {
		QVBoxLayout* layout = new QVBoxLayout;
		
		hsld = new ColorSlider("H");
		ssld = new ColorSlider("S");
		vsld = new ColorSlider("V");
		asld = new ColorSlider("A");

		layout -> addWidget(hsld);
		layout -> addWidget(ssld);
		layout -> addWidget(vsld);
		layout -> addWidget(asld);

		setLayout(layout);
		setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);

		QObject::connect(hsld, SIGNAL(valueChanged(int)), this, SLOT(changePart(int)));
		QObject::connect(ssld, SIGNAL(valueChanged(int)), this, SLOT(changePart(int)));
		QObject::connect(vsld, SIGNAL(valueChanged(int)), this, SLOT(changePart(int)));
		QObject::connect(asld, SIGNAL(valueChanged(int)), this, SLOT(changePart(int)));
	}

	bool updateFlag = false;

signals:
	void valueChanged(QColor);

public slots:
	void setColor(QColor color) {
		if (currentColor == color) return;

		currentColor = color;
		updateFlag = true;

		int h, s, v, a;
		color.getHsv(&h, &s, &v, &a);

		hsld -> setValue(h);
		ssld -> setValue(s);
		vsld -> setValue(v);
		asld -> setValue(a);

		updateFlag = false;
		emit valueChanged(currentColor);
	} 

	void changePart(int i) {
		(void)i;
		if (updateFlag == true) return;
		//qDebug("changePart");

		int h = hsld->value();
		int s = ssld->value();
		int v = vsld->value();
		int a = asld->value();

		auto qc = QColor();
		qc.setHsv(h,s,v,a);
		currentColor = qc;
		emit valueChanged(qc);
	}
};