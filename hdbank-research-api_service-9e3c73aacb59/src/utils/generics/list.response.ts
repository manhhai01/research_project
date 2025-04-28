export class ListInfo {
    total: number;
    constructor(total: number) {
        this.total = total;
    }
}

export class ListResponse<T> {
    data: T[];
    listInfo: ListInfo;
    constructor(item: T[]) {
        this.data = item;
        this.listInfo = new ListInfo(item.length);
    }
    static of<T>(list: ListResponse<T>): ListResponse<T> {
        return new ListResponse(list.data);
    }
}
