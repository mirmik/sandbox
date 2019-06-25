#ifndef DISPLAY_WIGET_H
#define DISPLAY_WIGET_H

#include <QWidget>

class DisplayWidget : public QWidget 
{
	Q_OBJECT

public:
	DisplayWidget(QWidget * parent = nullptr) : QWidget(parent) 
	{

	}
};

#endif