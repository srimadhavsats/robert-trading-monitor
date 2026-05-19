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

/**
 * Formats a raw price change percentage into a human-readable ticker metric.
 * Automatically appends explicit positive symbols and rounds decimal boundaries.
 * @param {number} change - The raw percentage change value (e.g., 1.45 or -2.3).
 * @returns {string} Formatted performance string (e.g., "+1.45%" or "-2.30%").
 */
export const formatPriceChange = (change) => {
  if (change === undefined || change === null) return "0.00%";
  const formatted = change.toFixed(2);
  return change > 0 ? `+${formatted}%` : `${formatted}%`;
};
