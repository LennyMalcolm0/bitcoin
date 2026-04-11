import winston from 'winston';
import { Request, Response, NextFunction } from 'express';

/**
 * Michael Sovereign Logging System
 * Robust logging for Bitcoin Core interactions.
 */
export const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.simple()
            )
        }),
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' }),
    ],
});

/**
 * Global Error Handler Middleware
 * Catches all unhandled exceptions in the Express pipeline.
 */
export const globalErrorHandler = (err: any, req: Request, res: Response, next: NextFunction) => {
    const statusCode = err.statusCode || 500;
    const message = err.message || 'Internal Server Error';

    logger.error({
        message: message,
        stack: err.stack,
        path: req.path,
        method: req.method,
        timestamp: new Date().toISOString()
    });

    res.status(statusCode).json({
        status: 'error',
        message: message,
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    });
};

/**
 * Safely extracts a field value from an object of unknown type.
 * 
 * This function performs runtime type checking to verify that the input is an object
 * and contains the specified field before attempting to access it.
 */
export function getFieldFromUnknownObject<T>(obj: unknown, field: string) {
    try {
        if (typeof obj !== "object" || !obj) {
            return undefined;
        }
        if (field in obj) {
            return (obj as Record<string, T>)[field];
        }
        return undefined;
    } catch (error) {
        logger.warn(`Failed to extract field ${field} from object`);
        return undefined;
    }
}

/**
 * Formats a numeric value into a localized string representation with proper currency formatting.
 */
export function moneyFormat(
    value: number | string | bigint,
    standard?: string | string[],
    dec?: number,
    noDecimals?: boolean
) {
    const decimal = (noDecimals || dec === 0)
        ? 0
        : dec || 2;

    const options: Intl.NumberFormatOptions = {
        minimumFractionDigits: decimal,
        maximumFractionDigits: decimal
    };

    try {
        const locale = standard || "en-US";
        const nf = new Intl.NumberFormat(locale, options);
        
        if (value === null || value === undefined) {
            return "--";
        }

        return nf.format(Number(value));
    } catch (error) {
        logger.error(`Currency formatting error: ${error.message}`);
        const nf = new Intl.NumberFormat("en-US", options);
        return (value || value === 0) ? nf.format(Number(value)) : "--";
    }
}
