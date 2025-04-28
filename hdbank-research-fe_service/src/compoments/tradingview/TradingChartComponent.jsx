import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setSelectTimeAction } from '../../redux/reducers/SelectTimeReducer'
import { getCurrentDate, getPastAndFutureDates } from '../../utils/FormatDateSymbols'
import DatePickerComponent from './DatePickerComponent'
import { Button, Empty, Space } from 'antd';
import { setCurrentSymbolAction } from '../../redux/reducers/CurrentSymbolReducer'
import ChartComponent from './ChartComponent'
import { getDataSymbolActionApi } from '../../redux/reducers/DataSymbolReducer'

const TradingChartComponent = () => {

    const { selectTime } = useSelector((state) => state.selectTimeReducer)
    const { currentSymbol } = useSelector((state) => state.currentSymbolReducer)
    const { data } = useSelector((state) => state.dataSymbolReducer)

    const dispatch = useDispatch()
    
    useEffect(() => {
        if (Object.keys(currentSymbol).length != 0) {
            getDataSymbolActionFunction()
        }
    }, [currentSymbol])

    const getDataSymbolActionFunction = () => {
        const {symbolId, startDate, endDate, subModelId} = currentSymbol
        const actionAsync = getDataSymbolActionApi(symbolId, startDate, endDate, subModelId);
        dispatch(actionAsync)
    }

    const handleClickSelectedTime = (item) => {

        const updatedSelectTime = selectTime?.map((tmp) =>
            tmp.key === item.key
                ? { ...tmp, isActive: true }
                : { ...tmp, isActive: false }
        );

        const nowDate = getCurrentDate()

        const { pastDate, futureDate } = getPastAndFutureDates(nowDate, Number(item.key))

        const actionCurrentSybol = { ...currentSymbol, currentDate: nowDate, startDate: pastDate, endDate: futureDate }

        dispatch(setSelectTimeAction(updatedSelectTime));
        dispatch(setCurrentSymbolAction(actionCurrentSybol))
    }

    const renderChartComponent = (data) => {
        const { historyData, forecastData } = data;
        if (Array.isArray(historyData) && historyData.length === 0) {
            return (<Empty />)
        } else {
            return (<ChartComponent {...{ history: historyData, future: forecastData }} />)
        }
    }

    return (
        <>
            <div className='mt-3 border-custom'>
                <h5 className='text-left'>{currentSymbol.symbol}</h5>
                <div className='row'>
                    <div className='col-12 col-md-8 mt-3'>
                        <div className='d-flex justify-content-start'>
                            <Space>
                                {selectTime?.map((item, index) => (
                                    <Button key={index} type={item.isActive ? "primary" : ""} onClick={() => {
                                        handleClickSelectedTime(item)
                                    }}>{item.name}</Button>
                                ))}
                            </Space>
                        </div>
                    </div>
                    <div className='col-12 col-md-4 mt-3'>
                        <DatePickerComponent />
                    </div>
                </div>
                <div className='mt-5'>
                    {renderChartComponent(data)}
                </div>
            </div>
        </>
    )
}

export default TradingChartComponent