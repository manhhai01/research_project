import { ArgumentMetadata, BadRequestException, PipeTransform } from '@nestjs/common';

export class ParseEnumPipe implements PipeTransform {
    constructor(private readonly enumType: any) {}

    transform(value: any, metadata: ArgumentMetadata) {
        const enumValues = Object.values(this.enumType);
        if (!enumValues.includes(value)) {
            throw new BadRequestException(`${value} is not a valid ${metadata.data}`);
        }
        return value; // Return the transformed enum value
    }
}
