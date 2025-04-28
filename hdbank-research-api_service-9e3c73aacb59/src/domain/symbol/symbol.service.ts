import { HttpException, Injectable } from '@nestjs/common';
import { PrismaService } from 'service/prisma/prisma.service';
import { SymbolGetResponse } from './response/symbol-get.response';
import { ListResponse } from 'utils/generics/list.response';
import { SymbolGetDataRequest } from './request/symbol-get-data.request';
import { SymbolGetDataResponse } from './response/symbol-get-data.response';
import { format } from 'date-fns';

@Injectable()
export class SymbolService {
    constructor(private readonly prismaService: PrismaService) {}

    async getSymbols(): Promise<SymbolGetResponse> {
        const symbols = (
            await this.prismaService.symbol.findMany({
                select: {
                    id: true,
                    name: true,
                    SymbolSubModel: {
                        select: {
                            SubModel: {
                                select: {
                                    id: true,
                                    name: true,
                                    Model: {
                                        select: {
                                            id: true,
                                            name: true,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            })
        ).map((symbol) => {
            return {
                id: symbol.id,
                name: symbol.name,
                model: symbol.SymbolSubModel.reduce((acc, curr) => {
                    const currModels = acc.map((model) => model.id);
                    if (!currModels.includes(curr.SubModel.Model.id)) {
                        acc.push({
                            id: curr.SubModel.Model.id,
                            name: curr.SubModel.Model.name,
                            subModels: [
                                {
                                    id: curr.SubModel.id,
                                    name: curr.SubModel.name,
                                },
                            ],
                        });
                    } else {
                        acc[currModels.indexOf(curr.SubModel.Model.id)].subModels.push({
                            id: curr.SubModel.id,
                            name: curr.SubModel.name,
                        });
                    }
                    return acc;
                }, []),
            };
        });
        return new ListResponse(symbols);
    }

    async getSymbolData(symbolId: number, query: SymbolGetDataRequest): Promise<SymbolGetDataResponse> {
        const historyData = (
            await this.prismaService.historyData.findMany({
                where: {
                    timestamp: {
                        gte: new Date(query.startDate),
                        lte: new Date(query.endDate),
                    },
                    symbolId: symbolId,
                },
                select: {
                    timestamp: true,
                    close: true,
                },
                orderBy: {
                    timestamp: 'asc',
                },
            })
        ).map((data) => {
            return { value: data.close, time: format(data.timestamp, 'yyyy-MM-dd') };
        });
        if (query.subModelId) {
            const symbolSubModel = await this.prismaService.symbolSubModel.findUnique({
                where: {
                    symbolId_subModelId: {
                        symbolId: symbolId,
                        subModelId: query.subModelId,
                    },
                },
            });
            if (!symbolSubModel) {
                throw new HttpException('Symbol Model not found', 404);
            }

            const maxTimestamp = await this.prismaService.historyData.aggregate({
                _max: {
                    timestamp: true,
                },
            });
            if (maxTimestamp._max.timestamp <= new Date(query.endDate)) {
                const maxDateForecast = await this.prismaService.forecastData.aggregate({
                    _max: {
                        date: true,
                    },
                    where: {
                        symbolSubModelId: symbolSubModel.id,
                    },
                });
                const forecastData = (
                    await this.prismaService.forecastData.findMany({
                        where: {
                            date: new Date(maxDateForecast._max.date),
                            symbolSubModelId: symbolSubModel.id,
                        },
                        select: {
                            timestamp: true,
                            value: true,
                        },
                        orderBy: {
                            timestamp: 'asc',
                        },
                    })
                ).map((data) => {
                    return { value: data.value, time: format(data.timestamp, 'yyyy-MM-dd') };
                });
                return {
                    historyData: historyData,
                    forecastData: forecastData,
                };
            }
        }

        return {
            historyData: historyData,
            forecastData: [],
        };
    }
}
