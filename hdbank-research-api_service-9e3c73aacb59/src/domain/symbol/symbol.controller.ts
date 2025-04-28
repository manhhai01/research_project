import { Controller, Get, Param, ParseIntPipe, Query } from '@nestjs/common';
import { SymbolService } from './symbol.service';
import { BaseResponse } from 'utils/generics/base.response';
import { SymbolGetResponse } from './response/symbol-get.response';
import { SymbolGetDataRequest } from './request/symbol-get-data.request';
import { SymbolGetDataResponse } from './response/symbol-get-data.response';

@Controller('/symbols')
export class SymbolController {
    constructor(private readonly symbolService: SymbolService) {}

    @Get()
    async getSymbols(): Promise<BaseResponse<SymbolGetResponse>> {
        return BaseResponse.of(await this.symbolService.getSymbols());
    }

    @Get('/:symbolId/data')
    async getSymbolData(
        @Param('symbolId', new ParseIntPipe()) symbolId: number,
        @Query() query: SymbolGetDataRequest,
    ): Promise<BaseResponse<SymbolGetDataResponse>> {
        return BaseResponse.of(await this.symbolService.getSymbolData(symbolId, query));
    }
}
