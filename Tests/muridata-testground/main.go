package main

import (
	"github.com/testground/sdk-go/run"
	"github.com/testground/sdk-go/runtime"

	"github.com/evan176/hnswgo"
)

func main() {
	run.Invoke(runf)
}

func runf(runenv *runtime.RunEnv) error {
	runenv.RecordMessage("Hello, Testground!")
	return nil
}
