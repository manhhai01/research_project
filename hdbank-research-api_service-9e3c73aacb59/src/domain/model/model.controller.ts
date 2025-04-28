import { Body, Controller, Post } from '@nestjs/common';
import { ModelService } from './model.service';
import { BaseResponse } from 'utils/generics/base.response';
import { ModelPostTrainRequest } from './request/model-post-train.request';
import { ModelPostTrainResponse } from './response/model-post-train.response';

@Controller('/models')
export class ModelController {
    constructor(private readonly modelService: ModelService) {}

    @Post('/train')
    async train(@Body() body: ModelPostTrainRequest): Promise<BaseResponse<ModelPostTrainResponse>> {

        return BaseResponse.of(await this.modelService.train(body));
    }
}
