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
 *          an object type or doesn't contain the specified field
 * 
 * @example
 * const data: unknown = { name: "Alice", age: 30 };
 * const name = getFieldFromUnknownObject<string>(data, "name"); // "Alice"
 * const missing = getFieldFromUnknownObject<string>(data, "email"); // undefined
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

export function formatDateTime(isoString: string): string {
    const date = new Date(isoString);
    return date.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true
    });
}

export function formatDate(isoString: string): string {
    const date = new Date(isoString);
    return date.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "long",
        year: "numeric"
    });
}

export function formatTime(isoString: string): string {
    const date = new Date(isoString);
    return date.toLocaleTimeString("en-GB", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true
    });
}
