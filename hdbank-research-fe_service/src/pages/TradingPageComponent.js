import React, { useEffect } from 'react'
import TradingChartComponent from '../compoments/tradingview/TradingChartComponent'
import { useSelector } from 'react-redux'
import NotiErrConnComponent from '../compoments/common/NotiErrConnComponent'
import MenuSymbolsComponent from '../compoments/tradingview/MenuSymbolsComponent'
import { Flex, Spin } from 'antd'

const TradingPageComponent = () => {

  const { isLoading, isError, messageError } = useSelector((state) => state.statusReducer)

  const renderTradingViewComponent = () => {

    if (isError) {
      return (<NotiErrConnComponent desc={messageError} />)
    }

    if (isLoading) {
      return (<Flex
        style={{
          height: '50vh',
          justifyContent: 'center',
          alignItems: 'center',
        }}
        gap="middle"
        vertical
      >
        <Spin size="large" />
      </Flex>)
    }

    return (<div className="container">
      <div className="row mt-4">
        <div className="col-12 col-lg-4 col-xxl-3">
          <MenuSymbolsComponent />
        </div>
        <div className="col-12 col-lg-8 col-xxl-9">
          <TradingChartComponent />
        </div>
      </div>
    </div>)
  }

  return (
    <div>
      {renderTradingViewComponent()}
    </div>
  )
}

export default TradingPageComponent