export function isArray(val): boolean {
  return Object.prototype.toString.call(val) === '[object Array]';
}
export function isObject(val): boolean {
  return Object.prototype.toString.call(val) === '[object Object]';
}
export function isString(val): boolean {
  return Object.prototype.toString.call(val) === '[object String]';
}

export const isSSR = (function () {
  return false;
  try {
    return !(typeof window !== 'undefined' && document !== undefined);
  } catch (e) {
    return true;
  }
})();
