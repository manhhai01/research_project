import {configureStore} from '@reduxjs/toolkit'
import SelectTimeReducer from './reducers/SelectTimeReducer';
import MenuSymbolsReducer from './reducers/MenuSymbolsReducer';
import StatusReducer from './reducers/StatusReducer';
import DataSymbolReducer from './reducers/DataSymbolReducer';
import CurrentSymbolReducer from './reducers/CurrentSymbolReducer';

export const store = configureStore({
    reducer: {
        selectTimeReducer: SelectTimeReducer,
        menuSymbolsReducer: MenuSymbolsReducer,
        statusReducer: StatusReducer,
        dataSymbolReducer: DataSymbolReducer,
        currentSymbolReducer: CurrentSymbolReducer
    }
});

