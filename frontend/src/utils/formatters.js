/**
 * SATS Sentinel v4.1 - Telemetry Formatting Utilities
 * Centralized data normalization and localization helper layers.
 */

/**
 * Formats a raw numeric asset price into a localized, comma-separated string.
 * @param {number} price - The raw float value from the oracle feed.
 * @returns {string} Fully localized display value.
 */
export const formatMarketPrice = (price) => {
  return (price || 0).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
};
