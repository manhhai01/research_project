export class GetSignedUrlResponse {
    url: string;
    key: string;

    constructor(url: string, key: string) {
        this.url = url;
        this.key = key;
    }
}
