import React, { useEffect, useState } from 'react';
import { Button, Menu, Switch } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import { setIsHasModelAction } from '../../redux/reducers/StatusReducer';
import { setCurrentSymbolAction } from '../../redux/reducers/CurrentSymbolReducer';
import { getMenuSymbolsActionApi } from '../../redux/reducers/MenuSymbolsReducer';
import { getSymbolSubModel } from '../../utils/CustomDataMenu';

const MenuSymbolsComponent = () => {

    const { isHasModel } = useSelector((state) => state.statusReducer)
    const { menuSymbolsNoModel, menuSymbolsAndModel } = useSelector((state) => state.menuSymbolsReducer)
    const { currentSymbol } = useSelector((state) => state.currentSymbolReducer)

    const dispatch = useDispatch()

    useEffect(() => {
        getMenuSymbolsActionFunction()
    }, [])

    const getMenuSymbolsActionFunction = () => {
        const actionAsync = getMenuSymbolsActionApi();
        dispatch(actionAsync)
    }

    const [current, setCurrent] = useState('1');
    const changeStatus = (value) => {
        dispatch(setIsHasModelAction(value))
    };
    const onClick = (e) => {
        const key = e.key

        setCurrent(key);

        const { id, label } = menuSymbolsNoModel[key - 1]
        const currentSymbolChange = { ...currentSymbol, symbolId: id, symbolName: label, subModelId: null }

        dispatch(setCurrentSymbolAction(currentSymbolChange))
    };

    const getLevelKeys = (items1) => {
        const key = {};
        const func = (items2, level = 1) => {
            items2.forEach((item) => {
                if (item.key) {
                    key[item.key] = level;
                }
                if (item.children) {
                    func(item.children, level + 1);
                }
            });
        };
        func(items1);
        return key;
    };
    const levelKeys = getLevelKeys(menuSymbolsAndModel);

    const [stateOpenKeys, setStateOpenKeys] = useState(['1', '11', '111']);
    const onOpenChange = (openKeys) => {
        const currentOpenKey = openKeys.find((key) => stateOpenKeys.indexOf(key) === -1);
        // open
        if (currentOpenKey !== undefined) {
            const repeatIndex = openKeys
                .filter((key) => key !== currentOpenKey)
                .findIndex((key) => levelKeys[key] === levelKeys[currentOpenKey]);
            setStateOpenKeys(
                openKeys
                    // remove repeat key
                    .filter((_, index) => index !== repeatIndex)
                    // remove current level all child
                    .filter((key) => levelKeys[key] <= levelKeys[currentOpenKey]),
            );
        } else {
            // close
            setStateOpenKeys(openKeys);
        }
    };

    const onSelect = (item) => {
        const key = item.key
        const { symbolId, subModelId, symbolName } = getSymbolSubModel(menuSymbolsAndModel, key)

        const dataCurrentSymbolChange = { ...currentSymbol, symbolId: Number(symbolId), subModelId: Number(subModelId), symbolName }
    
        dispatch(setCurrentSymbolAction(dataCurrentSymbolChange))
    }

    const renderMenuComponent = () => {
        if (isHasModel) {
            return (<Menu
                mode="inline"
                openKeys={stateOpenKeys}
                onOpenChange={onOpenChange}
                style={{
                    width: 256,
                }}
                items={menuSymbolsAndModel}
                onSelect={onSelect}
                inlineIndent={30}
            />)
        } else {
            return (<>
                <Menu
                    theme={"light"}
                    onClick={onClick}
                    style={{
                        width: 256,
                    }}
                    selectedKeys={[current]}
                    mode="inline"
                    items={menuSymbolsNoModel}
                />
            </>)
        }
    }

    return (
        <>
            <Switch onChange={changeStatus} />
            <Button color="default" variant="text">
                Model Service
            </Button>
            <br />
            <br />
            {renderMenuComponent()}
        </>
    )
}

export default MenuSymbolsComponent