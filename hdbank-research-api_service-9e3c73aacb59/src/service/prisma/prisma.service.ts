import { INestApplication, Injectable, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
    async onModuleInit() {
        await this.$connect();
    }

    async gracefulShutdown(application: INestApplication) {
        this.$on('beforeExit' as never, async () => {
            await application.close();
        });
    }
}
