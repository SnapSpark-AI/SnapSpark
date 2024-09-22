package main

import (
    "net/http"
    "log"
    "time"
)

func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        rw := &responseWriter{w, http.StatusOK}

        log.Printf("[🟢] Received request: %s %s from %s", r.Method, r.URL.Path, r.RemoteAddr)
        log.Printf("[🟢] Request Headers: %+v", r.Header)

        next.ServeHTTP(rw, r)

        log.Printf("[🟢] Responded with status: %d in %v", rw.statusCode, time.Since(start))
    })
}

type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}

func main() {
    fs := http.FileServer(http.Dir("."))
    http.Handle("/", loggingMiddleware(fs))

    log.Println("[🟢] Serving on http://localhost:3000")
    err := http.ListenAndServe(":3000", nil)
    if err != nil {
        log.Fatal(err)
    }
}
