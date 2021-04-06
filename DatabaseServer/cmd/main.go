package main

import (
	"log"
	"net/http"

	"github.com/maloneya/DataJournal/server"
	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

func main() {
	driver, err := neo4j.NewDriver("bolt://localhost:7687", neo4j.NoAuth())
	if err != nil {
		log.Fatalf("Failed to start db connection: %v\n", err.Error())
	}
	if driver.VerifyConnectivity() != nil {
		log.Fatalf("Could not verify connection")
	}
	defer driver.Close()

	http.HandleFunc("/store", server.CreateDBQueryHandler(server.ParseStoreRequest, driver))
	http.HandleFunc("/getActorGraph", server.CreateDBQueryHandler(server.ParseGetActorRequest, driver))

	log.Fatal(http.ListenAndServe(":8080", nil))

}
