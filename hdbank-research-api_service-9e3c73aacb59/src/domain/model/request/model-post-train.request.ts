import { Expose } from 'class-transformer';
import { IsBoolean } from 'class-validator';

export class ModelPostTrainRequest {
    @Expose()
    @IsBoolean()
    isTradingView: boolean;
}
