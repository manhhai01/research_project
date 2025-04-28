export const convertFormattedMenuSybols = (data) => {
    let result = [];
    let key = 1;

    data.forEach(item => {
        result.push({
            key: key++,
            label: item.name,
            id: item.id
        });
    });

    return result;
}

export const convertFormattedMenuSymbolsAndModels = (inputData) => {
    let result = [];

    inputData.forEach((item, index) => {
        const transformedItem = {
            key: `${index + 1}`,
            label: item.name,
            id: item.id.toString(),
            children: [],
        };

        item.model?.forEach((model, modelIndex) => {
            const transformedModel = {
                key: `${transformedItem.key}${modelIndex + 1}`,
                label: model.name,
                id: model.id.toString(),
                children: [],
            };

            model.subModels?.forEach((subModel, subModelIndex) => {
                const transformedSubModel = {
                    key: `${transformedModel.key}${subModelIndex + 1}`,
                    label: subModel.name,
                    id: subModel.id.toString(),
                };

                transformedModel.children.push(transformedSubModel);
            });

            transformedItem.children.push(transformedModel);
        });

        result.push(transformedItem);
    });

    return result;
}

const findItem = (items, key) => {
    for (let item of items) {
        if (item.key === key) {
            return item;
        }

        if (item.children) {
            const found = findItem(item.children, key);
            if (found) {
                return found;
            }
        }
    }
    return null;
};

export const getSymbolSubModel = (data, key) => {

    const item = findItem(data, key);

    if (item) {
        const symbolItem = data.find((d) => d.key == item.key.charAt(0));

        return {
            symbolId: symbolItem.id,
            subModelId: item.id,
            symbolName: symbolItem.label
        };
    }

    return null;
};