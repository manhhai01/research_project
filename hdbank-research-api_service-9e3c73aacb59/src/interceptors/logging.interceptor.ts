import { CallHandler, ExecutionContext, Injectable, NestInterceptor } from '@nestjs/common';
import * as chalk from 'chalk';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { WinstonLogger } from 'service/logger/winston.logger';

/**
 * Logger Interceptor.
 * Creates informative logs to all requests, showing the path and
 * the method name.
 */
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
    private readonly Logger = new WinstonLogger();
    intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
        const parentType = context.getArgs()[0].route.path;
        const fieldName = context.getArgs()[0].route.stack[0].method;
        return next.handle().pipe(
            tap(() => {
                this.Logger.debug(`${parentType} | ${fieldName}`);
            }),
        );
    }
}
