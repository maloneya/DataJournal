package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

type StorageRequest struct {
	Actor  string
	Event  string
	Entity string
}

func ParseRequest(req *http.Request) (request StorageRequest, err error) {
	decoder := json.NewDecoder(req.Body)
	err = decoder.Decode(&request)
	return
}

func Store(req StorageRequest, driver neo4j.Driver) error {
	session := driver.NewSession(neo4j.SessionConfig{})
	defer session.Close()
	_, err := session.WriteTransaction(func(tx neo4j.Transaction) (interface{}, error) {
		return tx.Run(fmt.Sprintf("CREATE ((:actor {name: $actor})-[:%v]->(:entity {name: $entity}))", req.Event), map[string]interface{}{
			"actor":  req.Actor,
			"entity": req.Entity,
		})
	})

	return err
}

func main() {
	driver, err := neo4j.NewDriver("bolt://localhost:7687", neo4j.NoAuth())
	if err != nil {
		log.Fatalf("Failed to start db connection: %v\n", err.Error())
	}
	if driver.VerifyConnectivity() != nil {
		log.Fatalf("Could not verify connection")
	}
	defer driver.Close()

	http.HandleFunc("/store", func(w http.ResponseWriter, req *http.Request) {
		if req.Method != "POST" {
			//todo error code
			fmt.Fprintf(w, "/store only supports post\n")
			return
		}

		request, err := ParseRequest(req)
		if err != nil {
			fmt.Fprintf(w, "/store recieved unparasable request: %v\n", err.Error())
			return
		}

		err = Store(request, driver)
		if err != nil {
			fmt.Fprintf(w, "Store failed %v\n", err.Error())
		}
	})

	log.Fatal(http.ListenAndServe(":8080", nil))

}
