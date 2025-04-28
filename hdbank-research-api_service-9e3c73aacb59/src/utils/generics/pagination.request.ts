import { Expose, Transform } from 'class-transformer';
import { IsOptional } from 'class-validator';
export class PaginationRequest {
    @Expose()
    @IsOptional()
    @Transform(({ value }) => value && parseInt(value))
    pageSize: number;

    @Expose()
    @IsOptional()
    @Transform(({ value }) => value && parseInt(value))
    pageNumber: number;
}
