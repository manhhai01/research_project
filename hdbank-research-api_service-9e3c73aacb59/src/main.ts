import { NestFactory } from '@nestjs/core';
import * as bodyParser from 'body-parser';
import * as compression from 'compression';
import * as cookieParser from 'cookie-parser';
import { cleanEnv, port, str } from 'envalid';
import rateLimit from 'express-rate-limit';
import helmet from 'helmet';
import { APP_SECRET, CREDENTIALS, HOST, NODE_ENV, ORIGIN, PORT } from './app.config';
import { AppModule } from './app.module';
import { LoggingInterceptor } from './interceptors/logging.interceptor';
import { ValidationPipe } from './pipes/validation.pipe';
import { WinstonLogger } from 'service/logger/winston.logger';
import { ErrorFilter } from 'filters/error.filter';

async function bootstrap() {
    const Logger = new WinstonLogger();
    try {
        validateEnv();
        const app = await NestFactory.create(AppModule, {
            cors: {
                origin: ORIGIN,
                credentials: CREDENTIALS,
            },
        });

        app.use(helmet());
        app.use(cookieParser(APP_SECRET));
        app.use(compression());
        app.use(bodyParser.json({ limit: '50mb' }));
        app.use(
            bodyParser.urlencoded({
                limit: '50mb',
                extended: true,
                parameterLimit: 50000,
            }),
        );
        app.use(
            rateLimit({
                windowMs: 1000 * 60 * 60,
                max: 1000, // 1000 requests per windowMs
                message: '🚫  Too many request created from this IP, please try again after an hour',
            }),
        );

        app.useGlobalInterceptors(new LoggingInterceptor());
        app.useGlobalPipes(new ValidationPipe());
       // app.useGlobalFilters(new ErrorFilter());

        await app.listen(PORT || 3000);

        Logger.info(
            `Server is running at http://${HOST}:${PORT}`,
        )
    } catch (error) {
        Logger.error(`❌  Error starting server, ${error}`);
        process.exit();
    }
}

function validateEnv() {
    cleanEnv(process.env, {
        DATABASE_URL: str(),
        PORT: port(),
    });
}

bootstrap().catch((e) => {
    const Logger = new WinstonLogger();
    Logger.error(`❌  Error starting server, ${e}`);
    throw e;
});
