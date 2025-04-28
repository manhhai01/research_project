import { Logger } from '@nestjs/common';
import {
    ASSET_S3_BUCKET,
    ASSET_S3_CLIENT_PUBLIC_URL,
    ASSET_S3_URL_EXPIRATION,
    AWS_ACCESS_KEY,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
} from 'app.config';
import { AWSError, S3 } from 'aws-sdk';
import { PromiseResult } from 'aws-sdk/lib/request';
import { GetSignedUrlResponse } from './response/get-signed-url.response';
import { v4 as uuid } from 'uuid';

export enum ContentType {
    PDF = 'application/pdf',
    RAR = 'application/vnd.rar',
    ZIP = 'application/zip',
    JPEG = 'image/jpeg',
    PNG = 'image/png',
    JPG = 'image/jpg',
    BMP = 'image/bmp',
    GIF = 'image/gif',
    CSV = 'text/csv',
    EXCEL = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    WORD = 'application/msword',
}

export const enum SignedUrlType {
    getObject = 'getObject',
    putObject = 'putObject',
}

export const enum DomainType {
    // MEMBER = 'member',
    // ADMIN = 'admin',
    // COMPANY = 'company',
}

export class StorageService {
    private s3: S3;
    private bucket: string;
    private expiration: number;
    private s3ClientPublicUrl: string;
    private logger = new Logger(StorageService.name);

    constructor() {
        this.bucket = ASSET_S3_BUCKET;
        this.expiration = parseInt(ASSET_S3_URL_EXPIRATION);
        this.s3 = new S3({
            credentials: {
                accessKeyId: AWS_ACCESS_KEY,
                secretAccessKey: AWS_SECRET_ACCESS_KEY,
            },
            region: AWS_REGION,
            s3ForcePathStyle: true,
            signatureVersion: 'v4',
        });
        this.s3ClientPublicUrl = ASSET_S3_CLIENT_PUBLIC_URL;
    }
    getSizeByKey = async (key: string) => {
        return await this.s3
            .headObject({ Key: key, Bucket: this.bucket })
            .promise()
            .then((metaData) => metaData);
    };

    getMetadataByKey = async (key: string): Promise<PromiseResult<S3.HeadObjectOutput, AWSError>> => {
        return await this.s3
            .headObject({ Key: key, Bucket: this.bucket })
            .promise()
            .then((metadata) => metadata);
    };

    async generateSignedUrl(contentType: ContentType, fileName: string, domain: DomainType): Promise<GetSignedUrlResponse> {
        const key = `${domain}/${uuid()}-${fileName}`;
        const url = await this.s3.getSignedUrlPromise(SignedUrlType.putObject, {
            Bucket: this.bucket,
            Key: key,
            Expires: this.expiration,
            ContentType: contentType,
        });
        return new GetSignedUrlResponse(url, key);
    }

    async getSignedUrl(key: string): Promise<string> {
        return await this.s3.getSignedUrlPromise(SignedUrlType.getObject, {
            Bucket: this.bucket,
            Key: key,
            Expires: this.expiration,
        });
    }

    async generatePermanentlyClientPublicUrl(contentType: ContentType, fileName: string): Promise<GetSignedUrlResponse> {
        const key = `client/${uuid()}-${fileName}`;
        const url = await this.s3.getSignedUrlPromise(SignedUrlType.putObject, {
            Bucket: this.bucket,
            Key: key,
            ContentType: contentType,
        });
        return new GetSignedUrlResponse(url, key);
    }

    async getPermanentlyClientPublicUrl(key: string): Promise<string> {
        return `${this.s3ClientPublicUrl}/${this.bucket}/${key}`;
    }

    extractFileNameViaClientPublicKey = (key: string): string => {
        return key.split('/')[1];
    };

    async deleteFile(key: string): Promise<void> {
        try {
            await this.s3
                .deleteObject({
                    Bucket: ASSET_S3_BUCKET,
                    Key: key,
                })
                .promise();
        } catch (e) {
            console.log('S3 error');
        }
    }

    async getListKey(): Promise<string[]> {
        return (
            await this.s3
                .listObjectsV2({
                    Bucket: ASSET_S3_BUCKET,
                })
                .promise()
        ).Contents.map((item) => item.Key);
    }
}
