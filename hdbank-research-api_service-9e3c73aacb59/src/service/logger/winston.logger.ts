import { Injectable } from '@nestjs/common';
import * as winston from 'winston';
import * as path from 'path';
import { format } from 'date-fns';

@Injectable()
export class WinstonLogger {
    private readonly logger: winston.Logger;

    constructor() {
        const logDir = path.join(process.cwd(), 'logs');
        const today = new Date();

        this.logger = winston.createLogger({
            format: winston.format.combine(
                winston.format.timestamp({
                    format: () => format(new Date(), 'dd-MM-yyyy HH:mm:ss'), // Thay đổi định dạng thời gian ở đây
                }),
                winston.format.printf(({ timestamp, level, message }) => {
                    return `${timestamp} [${level}]: ${message}`;
                }),
            ),
            transports: [
                new winston.transports.File({
                    filename: `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}.log`,
                    dirname: logDir,
                }),
            ],
        });

        if (process.env.NODE_ENV !== 'production') {
            // APP_ENV is accessed from env file
            this.logger.add(new winston.transports.Console());
        }
    }

    error(message: string, trace?: string) {
        this.logger.error(`${message} - ${trace}`);
    }

    warn(message: string) {
        this.logger.warn(message);
    }

    debug(message: string) {
        this.logger.debug(message);
    }

    info(message: string) {
        this.logger.info(message);
    }
}
