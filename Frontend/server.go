package main

import (
    "net/http"
    "log"
)

func main() {
    fs := http.FileServer(http.Dir("."))
    http.Handle("/", fs)

    log.Println("Serving on http://localhost:3000")
    err := http.ListenAndServe(":3000", nil)
    if err != nil {
        log.Fatal(err)
    }
}
