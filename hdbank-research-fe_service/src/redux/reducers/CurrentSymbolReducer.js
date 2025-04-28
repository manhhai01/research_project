import { createSlice } from '@reduxjs/toolkit'

const initialState = {
    currentSymbol: {}
}

const CurrentSymbolReducer = createSlice({
    name: "currentSymbolReducer",
    initialState,
    reducers: {
        setCurrentSymbolAction: (state, action) => {
            state.currentSymbol = action.payload
        },
    }
});

export const { setCurrentSymbolAction } = CurrentSymbolReducer.actions

export default CurrentSymbolReducer.reducer