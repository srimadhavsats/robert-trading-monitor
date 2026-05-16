/**
 * SATS Sentinel v4.1 - Application Configuration Core
 * Centralizes infrastructure endpoints for environment parity.
 */

export const CONFIG = {
  // Local development backend service ports
  BACKEND_API_URL: "http://127.0.0.1:8000",
  BACKEND_WS_URL: "ws://127.0.0.1:8000",

  // Default system runtime variables
  HEARTBEAT_RECONNECT_MS: 3000,
  MAX_CHART_TICKS: 40,
};
