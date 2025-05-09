import { Module } from '@nestjs/common';
import { ModelController } from './model.controller';
import { ModelService } from './model.service';
import { HttpModule } from '@nestjs/axios';

@Module({
    imports: [HttpModule],
    controllers: [ModelController],
    providers: [ModelService],
    exports: [ModelService]  // Add this line to export ModelService
})
export class ModelModule {}
