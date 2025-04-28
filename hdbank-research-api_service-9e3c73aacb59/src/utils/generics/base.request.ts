import { IsObject } from 'class-validator';
import { Request } from 'express';

export class BaseRequest extends Request {
    @IsObject()
    user: { accountId: number };
}
