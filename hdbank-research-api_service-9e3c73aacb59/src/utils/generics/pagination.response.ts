export class PageInfo {
    total: number;
    constructor(total: number) {
        this.total = total;
    }
}

export class PaginationResponse<T> {
    data: T[];
    pageInfo: PageInfo;
    constructor(item: T[], pageInfo: PageInfo) {
        this.data = item;
        this.pageInfo = pageInfo;
    }
    static of<T>(pagination: PaginationResponse<T>): PaginationResponse<T> {
        return new PaginationResponse(pagination.data, pagination.pageInfo);
    }
}
