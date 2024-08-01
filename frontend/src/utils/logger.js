// frontend/src/utils/logger.js

const LOG_LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3,
  };
  
  const currentLogLevel = process.env.NODE_ENV === 'production' ? LOG_LEVELS.WARN : LOG_LEVELS.DEBUG;
  
  class Logger {
    static debug(...args) {
      if (currentLogLevel <= LOG_LEVELS.DEBUG) {
        console.debug('[DEBUG]', ...args);
      }
    }
  
    static info(...args) {
      if (currentLogLevel <= LOG_LEVELS.INFO) {
        console.info('[INFO]', ...args);
      }
    }
  
    static warn(...args) {
      if (currentLogLevel <= LOG_LEVELS.WARN) {
        console.warn('[WARN]', ...args);
      }
    }
  
    static error(...args) {
      if (currentLogLevel <= LOG_LEVELS.ERROR) {
        console.error('[ERROR]', ...args);
        // You could send critical errors to your backend here
        // this.sendErrorToBackend(args);
      }
    }
  
    // static async sendErrorToBackend(errorData) {
    //   try {
    //     await fetch('/api/log', {
    //       method: 'POST',
    //       headers: { 'Content-Type': 'application/json' },
    //       body: JSON.stringify({ level: 'ERROR', data: errorData }),
    //     });
    //   } catch (error) {
    //     console.error('Failed to send error to backend:', error);
    //   }
    // }
  }
  
  export default Logger;