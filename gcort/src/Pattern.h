#pragma once

#include <QtCore>

class Pattern {
protected:
	struct point_record {
		QPoint point;
		float value;
		bool is_positive;

		point_record(int x, int y, float value, bool pos) : point(x,y), value(value), is_positive(pos) {}
	};

public:
	std::vector<point_record> vec;

public:
	void print() {
		for (auto& v : vec) {
			qDebug("x:%d y:%d v:%d", v.point.x() , v.point.y(), v.value);
		}
	}
};

class OpenRectanglePattern : public Pattern {
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

				float posweight = 1 / (vw * h);
				float negweight = - 1 / ((w - vw) * h);

				if (th <= h && th >= -h) {
					if (tw <= w && tw >= -w) {
						if (tw <= vw && tw >= -vw)
							vec.emplace_back(pw, ph, posweight, true);
						else	
							vec.emplace_back(pw, ph, negweight, false);
					}
				}
			}
		}		
	}
};

void draw(QPainter& painter, QPoint start, Pattern& task) {
	for (auto& v : task.vec) {
		painter.setPen(QPen(v.is_positive ? Qt::green : Qt::red));
		painter.drawPoint(start + v.point * 10);
	}
}