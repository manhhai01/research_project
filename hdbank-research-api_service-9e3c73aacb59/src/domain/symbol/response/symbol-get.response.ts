import { ListResponse } from 'utils/generics/list.response';

class SymbolGet {
    id: number;
    name: string;
    model: {
        id: number;
        name: string;
        subModels: {
            id: number;
            name: string;
        }[];
    }[];
}
export class SymbolGetResponse extends ListResponse<SymbolGet> {}
