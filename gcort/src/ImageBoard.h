#include <QtWidgets>

class ImageBoard : public QWidget {
	Q_OBJECT

	QImage* imag = nullptr;
	//QPushButton* button;
	QPoint mouse_last;

public:
	ImageBoard(QWidget* parent = nullptr) : QWidget(parent) {}

	void paintEvent(QPaintEvent *) override {
		QPainter painter;

		if (imag) {
			painter.begin(this);
			painter.drawImage(0, 0, *imag);
			painter.end();
		}
	}

	QImage* getImage() {
		return imag;
	}

	void setPixel(QPoint point) {
		QPainter painter(imag);
		painter.drawPoint(point);
	}

	void setLine(QPoint start, QPoint stop) {
		QPainter painter(imag);
		painter.drawLine(start, stop);
	}

	void mouseMoveEvent(QMouseEvent * event) override {
		if (event->buttons() & Qt::LeftButton) {
			setLine(mouse_last, event->pos());
			mouse_last = event->pos();
			repaint();
		}	
	}

	void mousePressEvent(QMouseEvent * event) override {
		if (event->button() & Qt::LeftButton) {
			setPixel(event->pos());
			mouse_last = event->pos();
			repaint();
		}
	}


	void resizeEvent(QResizeEvent * event) override {
		if (imag) delete imag;
		imag = new QImage(event->size(), QImage::Format_Mono);
		for (int h = 0; h < imag->height(); h++)
			for (int w = 0; w < imag->width(); w++)
				imag->setPixel(w,h,1);
	}
};


class ResultBoard : public QWidget {
	Q_OBJECT

	QImage* imag = nullptr;
	QPoint mouse_last;

public:
	ResultBoard(QWidget* parent = nullptr) : QWidget(parent) {}

	void paintEvent(QPaintEvent *) override {
		QPainter painter;

		if (imag) {
			painter.begin(this);
			painter.drawImage(0, 0, *imag);
			painter.end();
		}
	}

	QImage* getImage() {
		return imag;
	}

	void setPixel(QPoint point) {
		QPainter painter(imag);
		painter.drawPoint(point);
	}

	void setLine(QPoint start, QPoint stop) {
		QPainter painter(imag);
		painter.drawLine(start, stop);
	}

	void resizeEvent(QResizeEvent * event) override {
		if (imag) delete imag;
		imag = new QImage(event->size(), QImage::Format_RGB32);
		for (int h = 0; h < imag->height(); h++)
			for (int w = 0; w < imag->width(); w++)
				imag->setPixel(w,h,1);
	}
};