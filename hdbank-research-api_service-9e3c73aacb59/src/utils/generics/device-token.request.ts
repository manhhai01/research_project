import { Expose } from 'class-transformer';
import { IsOptional, IsString } from 'class-validator';

export class DeviceTokenRequest {
    @Expose()
    @IsString()
    @IsOptional()
    deviceToken: string;
}
