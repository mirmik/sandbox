#pragma once

#include <QImage>
#include <Pattern.h>
#include <Layer.h>
#include <stdlib.h>

/*class FirstCore : public QObject {
Q_OBJECT
private:
	//BinaryMatrix& matrix;
	
	std::vector<Layer*> output_layers; 
	//std::std::vector<uint8_t> neuro[8];

public:
	/*FirstCore (const QImage& image) {
		dataarr.resize(image.width() * image.height());
		width = image.width();
		height = image.height();

		for (size_t h = 0; h < height; h++) {
			for (size_t w = 0; w < width; ++w) {
				dataarr[h * width + w] = image.pixel(w,h);
			}
		}
	}

	uint8_t get(int w, int h) {
		if (w < 0 || h < 0 || w >= width || h >= height) return 128;
		return dataarr[h * width + w];
	}

	void evaluate() {
		laywidth = width / 3;
		layheight = height / 3;
		
		for(auto& n : neuro) {
			n.resize(laywidth * layheight);
		}
	}*/
//};