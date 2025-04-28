import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import * as path from 'path';
import { lastValueFrom } from 'rxjs';
import { MODEL_SERVICE_URL } from 'app.config';
import { createReadStream } from 'fs';
import * as FormData from 'form-data';
import { ModelPostTrainRequest } from './request/model-post-train.request';
import { ModelPostTrainResponse } from './response/model-post-train.response';

@Injectable()
export class ModelService {
    constructor(private readonly httpService: HttpService) {}

    async train(body: ModelPostTrainRequest): Promise<ModelPostTrainResponse> {
        const formData = new FormData();
        const targetUrl = MODEL_SERVICE_URL + '/train';
        // if (!body.isTradingView) {
        //     const fileName = 'TREASURY_MARKET_VARIABLES.xlsx';
        //     // const filePath = path.resolve(BLOOMBERG_URL + fileName);
        //     // const fileStream = createReadStream(absolutePath);
        //     const filePath = path.join(__dirname, '/../../../file', fileName);
        //     const fileStream = createReadStream(filePath);
        //     formData.append('file', fileStream, {
        //         filename: fileName,
        //     });
        // }
        const printer = await lastValueFrom(
            this.httpService.post(targetUrl, formData, {
                headers: formData.getHeaders(),
            }),
        );
        
        return printer.data.data;
    }
}
