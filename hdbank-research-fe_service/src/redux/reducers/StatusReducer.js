import { createSlice } from '@reduxjs/toolkit'

const initialState = {
    isLoading: false,
    isError: false,
    isHasModel: false,
    messageError: ""
}

const StatusReducer = createSlice({
    name: "statusReducer",
    initialState,
    reducers: {
        setIsLoadingAction: (state, action) => {
            state.isLoading = action.payload
        },
        setIsErrorAction: (state, action) => {
            state.isError = action.payload
        },
        setMessageErrorAction: (state, action) => {
            state.messageError = action.payload
        },
        setIsHasModelAction: (state, action) => {
            state.isHasModel = action.payload
        }
    }
});

export const { setIsLoadingAction, setIsErrorAction, setMessageErrorAction, setIsHasModelAction } = StatusReducer.actions

export default StatusReducer.reducer