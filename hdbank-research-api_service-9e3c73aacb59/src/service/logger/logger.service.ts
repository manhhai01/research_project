import { Injectable } from "@nestjs/common";
import { Prisma } from "@prisma/client";
import { PrismaService } from "service/prisma/prisma.service";

@Injectable()
export class LoggerErrorService {
    constructor(private readonly prismaService: PrismaService) {}

    async createLogError(data: Prisma.LogErrorCreateInput) {
        return this.prismaService.logError.create({
            data,
        })
    }
}