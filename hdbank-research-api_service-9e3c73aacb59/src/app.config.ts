import { config } from 'dotenv';
config({ path: `.env.${process.env.NODE_ENV || 'development'}` });

export const CREDENTIALS = process.env.CREDENTIALS === 'true';

export const {
    APP_SECRET,
    HOST,
    NODE_ENV,
    ORIGIN,
    PORT,
    DATABASE_URL,
    MODEL_SERVICE_URL,
    FILE_SERVICE_URL,
    BLOOMBERG_URL,
    ASSET_S3_BUCKET,
    ASSET_S3_CLIENT_PUBLIC_URL,
    ASSET_S3_URL_EXPIRATION,
    AWS_ACCESS_KEY,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
} = process.env;
