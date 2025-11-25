// Centralized HTTP error message handling

type HttpErrorInfo = {
  code: number;
  label: string;
  message: string;
};

// Common HTTP error definitions
export const HTTP_ERRORS: Record<number, HttpErrorInfo> = {
  400: {
    code: 400,
    label: "400_BAD_REQUEST",
    message: "The request is invalid or malformed."
  },
  401: {
    code: 401,
    label: "401_UNAUTHORIZED",
    message: "Authentication is required to access this resource."
  },
  403: {
    code: 403,
    label: "403_FORBIDDEN",
    message: "You do not have permission to access this resource."
  },
  404: {
    code: 404,
    label: "404_NOT_FOUND",
    message: "The requested resource could not be found."
  },
  408: {
    code: 408,
    label: "408_REQUEST_TIMEOUT",
    message: "The server took too long to respond."
  },
  409: {
    code: 409,
    label: "409_CONFLICT",
    message: "A conflict was detected in the request."
  },
  429: {
    code: 429,
    label: "429_TOO_MANY_REQUESTS",
    message: "Too many requests were sent in a short period."
  },
  500: {
    code: 500,
    label: "500_INTERNAL_SERVER_ERROR",
    message: "An internal server error occurred."
  },
  501: {
    code: 501,
    label: "501_NOT_IMPLEMENTED",
    message: "The server does not support the requested functionality."
  },
  502: {
    code: 502,
    label: "502_BAD_GATEWAY",
    message: "An invalid response was received from an upstream server."
  },
  503: {
    code: 503,
    label: "503_SERVICE_UNAVAILABLE",
    message: "The server is temporarily unavailable."
  },
  504: {
    code: 504,
    label: "504_GATEWAY_TIMEOUT",
    message: "The upstream server timed out."
  }
};

// Auto-generated functions such as 404_NOT_FOUND(extra?)
export const ERROR_FUNCTIONS = Object.fromEntries(
  Object.values(HTTP_ERRORS).map(err => [
    err.label,
    (extra?: string) =>
      console.error(
        `[${err.label}] ${err.message}${extra ? " — " + extra : ""}`
      )
  ])
) as Record<string, (extra?: string) => void>;

// Main function for logging any HTTP error
export const logHttpError = (code: number, extra?: string) => {
  const err = HTTP_ERRORS[code];
  if (!err) {
    console.error(`[UNKNOWN_HTTP_ERROR] Code: ${code}${extra ? " — " + extra : ""}`);
    return;
  }
  console.error(
    `[${err.label}] ${err.message}${extra ? " — " + extra : ""}`
  );
};
