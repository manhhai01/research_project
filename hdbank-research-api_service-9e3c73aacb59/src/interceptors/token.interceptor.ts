// import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
// import { Observable, map } from 'rxjs';
// import type { Response } from 'express';
// import { NODE_ENV } from 'config';
// import { SuccessResponse } from './success.response';

// @Injectable()
// export class TokenInterceptor implements NestInterceptor {
//   constructor() {}

//   intercept(context: ExecutionContext, next: CallHandler<{ token: string; uid: string }>): Observable<SuccessResponse> {
//     return next.handle().pipe(
//       map(data => {
//         const response = context.switchToHttp().getResponse<Response>();
//         const { token, uid } = data;

//         response.setHeader('Authorization', `Bearer ${token}`);
//         response.cookie('token', token, {
//           httpOnly: true,
//           signed: true,
//           sameSite: 'strict',
//           secure: NODE_ENV === 'production',
//         });

//         return new SuccessResponse({ message: 'User logged in successfully', metadata: { userId: uid } });
//       }),
//     );
//   }
// }
