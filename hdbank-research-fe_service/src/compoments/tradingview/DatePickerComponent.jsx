import React from 'react';
import { DatePicker } from 'antd';
import { convertDateFormat } from '../../utils/FormatDateSymbols';
import { useDispatch, useSelector } from 'react-redux';
import { setSelectTimeAction } from '../../redux/reducers/SelectTimeReducer';
import { setCurrentSymbolAction } from '../../redux/reducers/CurrentSymbolReducer';
const { RangePicker } = DatePicker;

const DatePickerComponent = () => {

    const { currentSymbol } = useSelector((state) => state.currentSymbolReducer)
    const { selectTime } = useSelector((state) => state.selectTimeReducer)

    const dispatch = useDispatch()

    const onChange = (date, dateString) => {

        const dataStrFormat = dateString.map((date) => {
            return date == '' ? '' : convertDateFormat(date)
        })

        if (!dataStrFormat.includes('')) {
            const action = { ...currentSymbol, startDate: dataStrFormat[0], endDate: dataStrFormat[1] }

            const updateSelectTime = selectTime.map((item) => ({
                ...item,
                isActive: false
            }))

            dispatch(setCurrentSymbolAction(action))
            dispatch(setSelectTimeAction(updateSelectTime))
        }
    }

    return (
        <RangePicker format={'DD-MM-YYYY'} onChange={onChange} />
    )
}

export default DatePickerComponent