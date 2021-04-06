package main

import (
	"fmt"
	"os"

	"github.com/maloneya/DataJournal/schema"
)

func main() {
	args := os.Args[1:]
	fmt.Printf("Exit: %v\n", schema.Generate(args[0]))
}
