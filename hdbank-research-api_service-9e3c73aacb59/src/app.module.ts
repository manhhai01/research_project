import { Module } from '@nestjs/common';
import { APP_FILTER } from '@nestjs/core';
import { ModelModule } from 'domain/model/model.module';
import { SymbolModule } from 'domain/symbol/symbol.module';
import { ErrorFilter } from 'filters/error.filter';
import { LoggerErrorService } from 'service/logger/logger.service';
import { PrismaModule } from 'service/prisma/prisma.module';
import { CronJobModule } from 'service/cronjob/cronjob.module';

@Module({
    imports: [ModelModule, SymbolModule, PrismaModule, CronJobModule],
    providers: [
        LoggerErrorService, 
        {
          provide: APP_FILTER, 
          useClass: ErrorFilter,
        },
    ],
})
export class AppModule {}
