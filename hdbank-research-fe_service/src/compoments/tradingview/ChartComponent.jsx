import { ColorType, createChart } from 'lightweight-charts';
import React, { useEffect, useRef } from 'react'

const ChartComponent = (props) => {

  const styles = {
    backgroundColor: 'white',
    lineColor: '#2962FF',
    textColor: 'black',
    areaTopColor: '#2962FF',
    areaBottomColor: 'rgba(41, 98, 255, 0.28)',
    futureLineColor: '#dc362e',
    futureAreaTopColor: '#ffde21',
    futureAreaBottomColor: 'rgba(255, 33, 33, 0.28)',
  }

  const chartContainerRef = useRef();

    useEffect(() =>
    {
        if (props.history && props.history.length > 0)
        {

            const handleResize = () =>
            {
                chart.applyOptions({
                    width: chartContainerRef.current.clientWidth,
                    autoScale: true
                });
            };
            const chart = createChart(chartContainerRef.current, {
                layout: {
                    background: { type: ColorType.Solid, color: styles.backgroundColor },
                    textColor: "black",
                },
                width: chartContainerRef.current.clientWidth,
                height: 420,
            });

            chart.timeScale().fitContent();

            const newSeries = chart.addAreaSeries({ lineColor: styles.lineColor, topColor: styles.areaTopColor, bottomColor: styles.areaBottomColor });
            newSeries.setData(props.history);

            // #future
            const futureSeries = chart.addAreaSeries({ lineColor: styles.futureLineColor, topColor: styles.futureAreaTopColor, bottomColor: styles.futureAreaBottomColor, customValues:"timestamp" });
            futureSeries.setData(props.future);

            window.addEventListener('resize', handleResize);

            return () =>
            {
                window.removeEventListener('resize', handleResize);
                chart.remove();
            };

        }

    }, [props.history, props.future]);

    return (
        <div ref={chartContainerRef} />
    );
}

export default ChartComponent