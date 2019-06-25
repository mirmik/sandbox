#ifndef DISPLAY_WIGET_H
#define DISPLAY_WIGET_H

#include <QWidget>
#include <QtCharts>

#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QChart>
#include <QtCharts/QValueAxis>

class DisplayWidget : public QWidget
{
	Q_OBJECT

	QChart *m_chart;
    QLineSeries *m_series ;

public:
	DisplayWidget(QWidget * parent = nullptr) : QWidget(parent),
		m_chart(new QChart),
	    m_series(new QLineSeries)
	{
		QChartView *chartView = new QChartView(m_chart);

		//QVector<double> arr(0.33, 512);
		for (int i = 0; i < 300; ++i)
			m_series->append(i,i);

		chartView->setMinimumSize(800, 600);
		m_chart->addSeries(m_series);

		QValueAxis *axisX = new QValueAxis;
		//axisX->setRange(0, 300);
		//axisX->setLabelFormat("%g");
		axisX->setTitleText("Samples");

		QValueAxis *axisY = new QValueAxis;
		//axisY->setRange(-1, 300);
		axisY->setTitleText("Audio level");

		m_chart->setAxisX(axisX, m_series);
		m_chart->setAxisY(axisY, m_series);
		m_chart->legend()->hide();

		//m_series->replace(arr);
		//m_chart->setTitle("Data from the microphone (" + deviceInfo.deviceName() + ')');

		QVBoxLayout *mainLayout = new QVBoxLayout(this);
		mainLayout->addWidget(chartView);

		setLayout(mainLayout);
	}
};

#endif