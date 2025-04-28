import { ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus, Injectable } from '@nestjs/common';
import { NODE_ENV } from 'app.config';
import { Response } from 'express';
import { LoggerErrorService } from 'service/logger/logger.service';
import { WinstonLogger } from 'service/logger/winston.logger';

@Injectable()
@Catch(Error)
export class ErrorFilter implements ExceptionFilter {
    private readonly logger = new WinstonLogger();
    constructor(private readonly logErrorService: LoggerErrorService) {}
    async catch(exception: HttpException, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();
        const request = ctx.getRequest<Request>();
        const status: number = exception instanceof HttpException ? exception.getStatus() : HttpStatus.INTERNAL_SERVER_ERROR;
        const message: string = exception.message;
        const name: string = exception.name || 'HttpException';

        this.logger.error(exception.message, exception.stack);

        await this.logErrorService.createLogError({
            service_name: 'hdb_research_be_service',
            name,
            message,
            status_code: status,
            path: request.url,
            error_details: exception.stack,
        });

        response.status(status).json({
            name,
            message: message,
            statusCode: status,
            path: request.url,
            timestamp: new Date().toISOString(),
            error: (exception as any).error,
            //stack: exception.stack,
        });
    }
}
