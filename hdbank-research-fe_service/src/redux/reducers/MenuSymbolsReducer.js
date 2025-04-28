import { createSlice } from '@reduxjs/toolkit'
import http from '../../utils/ConfigInterceptor';
import { setIsErrorAction, setIsLoadingAction, setMessageErrorAction } from './StatusReducer';
import { convertFormattedMenuSybols, convertFormattedMenuSymbolsAndModels } from '../../utils/CustomDataMenu';
import { getCurrentDate, getPastAndFutureDates } from '../../utils/FormatDateSymbols';
import { setCurrentSymbolAction } from './CurrentSymbolReducer';

const initialState = {
    menuSymbolsAndModel: [],
    menuSymbolsNoModel: []
}

const MenuSymbolsReducer = createSlice({
    name: "menuSymbolsReducer",
    initialState,
    reducers: {
        setMenuSymbolsAndModelAction: (state, action) => {
            state.menuSymbolsAndModel = action.payload
        },

        setMenuSymbolsNoModelAction: (state, action) => {
            state.menuSymbolsNoModel = action.payload
        }
    }
});

export const { setMenuSymbolsAndModelAction, setMenuSymbolsNoModelAction } = MenuSymbolsReducer.actions

export default MenuSymbolsReducer.reducer

// async action

export const getMenuSymbolsActionApi = () => {
    return async (dispatch) => {
        try {
            const res = await http.get("/symbols")

            if (res.status == 200) {
                const symbols = res.data.data.data
                
                if (Array.isArray(symbols) && symbols.length === 0) {
                    dispatch(setIsErrorAction(true))
                    dispatch(setMessageErrorAction("Không có dữ liệu symbols"))
                } else {
                    const dataMenuSymbols = convertFormattedMenuSybols(symbols)

                    const dataMenuSymbolsAndModels = convertFormattedMenuSymbolsAndModels(symbols)

                    const currentDate = getCurrentDate()
                    const { pastDate, futureDate } = getPastAndFutureDates(currentDate, 1)

                    const { id, label } = dataMenuSymbols[0]

                    const dataCurrentSymbol = {symbolId: id, symbolName: label, subModelId: null, currentDate, startDate: pastDate, endDate: futureDate}

                    dispatch(setMenuSymbolsNoModelAction(dataMenuSymbols))
                    dispatch(setMenuSymbolsAndModelAction(dataMenuSymbolsAndModels))
                    dispatch(setCurrentSymbolAction(dataCurrentSymbol))
                }
            }
        } catch (error) {
            console.log(error)
            dispatch(setIsErrorAction(true))
            dispatch(setMessageErrorAction("Xảy ra lỗi khi kết nối đến server."))
        }
    }
}

