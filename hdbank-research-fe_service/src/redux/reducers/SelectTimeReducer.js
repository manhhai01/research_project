import { createSlice } from '@reduxjs/toolkit'

const initialState = {
    selectTime: [
        { key: "1", name: "1 Năm", isActive: true },
        { key: "2", name: "2 Năm", isActive: false },
        { key: "3", name: "3 Năm", isActive: false }
    ]
}

const SelectTimeReducer = createSlice({
    name: 'selectTimeReducer',
    initialState,
    reducers: {
        setSelectTimeAction: (state, action) => {
            state.selectTime = action.payload
        }
    }
});

export const { setSelectTimeAction } = SelectTimeReducer.actions

export default SelectTimeReducer.reducer