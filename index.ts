import winston from 'winston';
import { Request, Response, NextFunction } from 'express';
import fs from 'fs';
import path from 'path';

// Ensure logs directory exists - Atomic creation to prevent TOCTOU race conditions
const logDir = 'logs';
fs.mkdirSync(logDir, { recursive: true });

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
        new winston.transports.File({ filename: path.join(logDir, 'error.log'), level: 'error' }),
        new winston.transports.File({ filename: path.join(logDir, 'combined.log') }),
    ],
});

/**
 * Global Error Handler Middleware
 */
export const globalErrorHandler = (err: Error | any, req: Request, res: Response, next: NextFunction) => {
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
 *
 * @template T - The expected type of the field value
 * @param obj - The object to extract the field from
 * @param field - The name of the field to retrieve
 * @returns The value of the field cast to type T, or undefined if the object is not
 * an object type or doesn't contain the specified field
 */
export function getFieldFromUnknownObject<T>(obj: unknown, field: string) {
    if (typeof obj !== "object" || !obj) {
        return undefined;
    }
    if (field in obj) {
        return (obj as Record<string, T>)[field];
    }
    return undefined;
}

/**
 * Formats a numeric value into a localized string representation with proper currency formatting.
 * 
 * @param value - The value to format
 * @param standard - The locale string (e.g., "en-US")
 * @param dec - Number of decimal places
 * @param noDecimals - If true, returns no decimals
 * @returns Formatted currency string
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
        const errorMessage = error instanceof Error ? error.message : String(error);
        logger.error(`Currency formatting error: ${errorMessage}`);
        const nf = new Intl.NumberFormat("en-US", options);
        return (value || value === 0) ? nf.format(Number(value)) : "--";
    }
}
