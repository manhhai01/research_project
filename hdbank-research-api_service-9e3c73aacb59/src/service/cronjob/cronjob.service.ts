import { Injectable } from '@nestjs/common';
import { ModelService } from 'domain/model/model.service';
import { Cron, CronExpression } from '@nestjs/schedule';
@Injectable()
export class CronJobService {
    constructor(private readonly modelService: ModelService) {}

    @Cron(CronExpression.EVERY_DAY_AT_9AM)
    async trainModel(): Promise<void> {
        await this.modelService.train({ isTradingView: true });
    }
}
