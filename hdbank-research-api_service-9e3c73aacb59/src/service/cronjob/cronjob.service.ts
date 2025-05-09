import { Injectable } from '@nestjs/common';
import { ModelService } from 'domain/model/model.service';
import { Cron, CronExpression } from '@nestjs/schedule';
@Injectable()
export class CronJobService {
    constructor(private readonly modelService: ModelService) {}

    @Cron(CronExpression.EVERY_DAY_AT_9AM)
    async trainModel(): Promise<void> {
        console.log(`[CronJobService] Cron job started at ${new Date().toISOString()}`);
        
        try {
            await this.modelService.train({ isTradingView: true });
            console.log(`[CronJobService] Model training completed at ${new Date().toISOString()}`);
        } catch (error) {
            console.error(`[CronJobService] Error during model training:`, error);
        }
    }
}
