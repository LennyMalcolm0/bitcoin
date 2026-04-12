import { logger, getFieldFromUnknownObject, moneyFormat } from '../index';

const describe = (global as any).describe;
const test = (global as any).test;
const expect = (global as any).expect;

describe('Utility Functions', () => {
    test('getFieldFromUnknownObject returns correct field', () => {
        const data = { name: 'Sovereign', value: 100 };
        expect(getFieldFromUnknownObject<string>(data, 'name')).toBe('Sovereign');
        expect(getFieldFromUnknownObject<number>(data, 'value')).toBe(100);
        expect(getFieldFromUnknownObject<string>(data, 'missing')).toBeUndefined();
    });

    test('moneyFormat formats correctly', () => {
        expect(moneyFormat(1234.56)).toBe('1,234.56');
        expect(moneyFormat(1234.56, 'de-DE')).toBe('1.234,56');
        expect(moneyFormat(1234.56, 'en-US', 3)).toBe('1,234.560');
        expect(moneyFormat(1234.56, 'en-US', 2, true)).toBe('1,235');
        expect(moneyFormat(null)).toBe('--');
    });
});

describe('Logger', () => {
    test('logger is defined', () => {
        expect(logger).toBeDefined();
    });
});
