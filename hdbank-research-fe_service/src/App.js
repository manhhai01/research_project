import React, { Component } from 'react'
import TradingPageComponent from './pages/TradingPageComponent'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

export default class App extends Component {
    render() {
        return (
            <BrowserRouter>
                <Routes>
                    <Route index element={<TradingPageComponent/>} ></Route>
                    <Route path='*' element={<Navigate to={'/'} />} ></Route>
                </Routes>
            </BrowserRouter>
        )
    }
}
