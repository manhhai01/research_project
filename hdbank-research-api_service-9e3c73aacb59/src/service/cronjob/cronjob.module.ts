import { Module } from '@nestjs/common';
import { CronJobService } from './cronjob.service';
import { ModelModule } from 'domain/model/model.module';
import { ScheduleModule } from '@nestjs/schedule';
@Module({
    imports: [ModelModule, ScheduleModule.forRoot()],
    providers: [CronJobService],
})
export class CronJobModule {}
