#pragma once

#include <QtCore>

class ConvTask;

class Matrix {
	int _width;
	int _height;
	std::vector<uint8_t> dataarr;

public:
	Matrix(std::initializer_list<std::initializer_list<uint8_t>> list) {
		_height = list.size();
		_width = list.begin()->size();

		dataarr.resize(_width * _height);

		int w = 0, h =0;
		for(const auto& c : list) {
			for(const auto& r : c) {
				dataarr[h * _width + w] = r;
				w++;
			}
			w = 0;
			h++;
		}
	}

	int width() const { return _width; }
	int height() const { return _height; }

	QPoint center() const {
		return QPoint(_width / 2, _height / 2);
	}

	uint8_t operator()(int w, int h) const {
		return dataarr[h * _width + w];
	}
};

class ConvTask {
protected:
	struct point_record {
		QPoint point;
		uint8_t value;

		point_record(int x, int y, uint8_t value) : point(x,y), value(value) {}
	};

public:
	std::vector<point_record> vec;

public:
	/*ConvTask(const Matrix& matrix, float angle) {
		vec.reserve(matrix.width() * matrix.height());
		
		QPoint center = matrix.center();

		for (int h = 0; h < matrix.height(); h++)
			for (int w = 0; w < matrix.width(); w++) {
				float nx = + (w - center.x()) * qCos(angle) + (h - center.y()) * qSin(angle);
				float ny = - (w - center.x()) * qSin(angle) + (h - center.y()) * qCos(angle);
				nx += nx >= 0 ? 0.5 : -0.5;
				ny += ny >= 0 ? 0.5 : -0.5;

				qDebug("%d %d %f %f", w - center.x(), h - center.y(), nx, ny);

				vec.emplace_back(
					nx, 
					ny,
					matrix(w,h)
				);
			}
	}*/

	void print() {
		for (auto& v : vec) {
			qDebug("x:%d y:%d v:%d", v.point.x() , v.point.y(), v.value);
		}
	}
};

class OpenRectanglePattern : public ConvTask {
public:
	OpenRectanglePattern(float w, float vw, float h, float angle) {
		w = w / 2; 
		vw = vw / 2;
		h = h / 2;

		int radius = qSqrt(w*w + h*h) + 1;

		for (int ph = -radius; ph <= radius; ph++) {
			for (int pw = -radius; pw <= radius; pw++) {
				float tw = + (float)pw * qCos(angle) - (float)ph * qSin(angle);
				float th = + (float)pw * qSin(angle) + (float)ph * qCos(angle);

				qDebug("%f %f", tw, th);

				if (th <= h && th >= -h) {
					if (tw <= w && tw >= -w) {
						vec.emplace_back(pw, ph, tw <= vw && tw >= -vw ? 255 : 0);
					}
				}
			}
		}		
	}
};

void draw(QPainter& painter, QPoint start, ConvTask& task) {
	for (auto& v : task.vec) {
		if (v.value >= 128) painter.drawPoint(start + v.point * 10);
	}
}