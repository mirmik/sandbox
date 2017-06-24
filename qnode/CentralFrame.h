#pragma once

#include <QtWidgets>

class CentralFrame : public QWidget {
	Q_OBJECT

	QColor currentColor;
	QPointF focus;

public:

	CentralFrame() {}

protected:
	void mouseMoveEvent(QMouseEvent * event) override {
		if (event->buttons() & Qt::LeftButton) {
			focus = event -> pos();
			repaint();
		}	
	}

	void mousePressEvent(QMouseEvent * event) override {
		if (event->button() != Qt::LeftButton) return;
		focus = event -> pos();
		repaint();
	}

	void showEvent(QShowEvent *) override {
		focus = rect().center();
	}
 
	void paintEvent(QPaintEvent *) override {
		QPainter painter(this);

		QPointF center = rect().center();
		QRadialGradient grad(center, width() / 2, focus);
		grad.setColorAt(0, currentColor);
		grad.setColorAt(0.5, Qt::blue);
		grad.setColorAt(1, QColor(Qt::blue).darker(160));

		painter.setBrush(grad);
		painter.drawRect(0,0,width(),height());
	}

public slots:
	void updateColor(QColor color) {
		if (color == currentColor) return;
		currentColor = color;

		repaint(0,0,width(),height());

		emit colorChanged(currentColor);
	}

	signals:
	void colorChanged(QColor);

};