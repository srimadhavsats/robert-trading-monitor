import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";

/**
 * SATS Sentinel v4.1 - Application Bootstrapper
 * Initializes the React virtual DOM tree and mounts the root application shell.
 * StrictMode is maintained to enforce optimal state lifecycles and catch side-effects.
 */
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
