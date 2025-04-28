import { Expose, Type } from 'class-transformer';
import { IsDateString, IsInt, IsOptional, Matches } from 'class-validator';

export class SymbolGetDataRequest {
    @Expose()
    @Matches(/^\d{4}-\d{2}-\d{2}$/, {
        message: 'Date must be in the format yyyy-mm-dd.',
    })
    @IsDateString()
    startDate: string;

    @Expose()
    @Matches(/^\d{4}-\d{2}-\d{2}$/, {
        message: 'Date must be in the format yyyy-mm-dd.',
    })
    @IsDateString()
    endDate: string;

    @Expose()
    @Type(() => Number)
    @IsInt()
    @IsOptional()
    subModelId: number;
}
