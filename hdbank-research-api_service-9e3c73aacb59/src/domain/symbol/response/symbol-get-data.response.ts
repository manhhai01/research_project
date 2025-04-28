export class SymbolGetDataResponse {
    historyData: {
        time: string;
        value: number;
    }[];
    forecastData: {
        time: string;
        value: number;
    }[];
}
