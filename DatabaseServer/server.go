package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

type ParseFn func(*http.Request) (Query, error)

type Query interface {
	// Query returns the cypher string, the query params
	Query() (string, map[string]interface{})
}

// This needs to be aligned with the structs in the schema package
// The write and read path need to be aligned on db schema to avoid typing issues.
type StorageRequest struct {
	Actor  string
	Event  string
	Entity string
}

func (req StorageRequest) Query() (query string, params map[string]interface{}) {
	query = fmt.Sprintf("CREATE ((:actor {name: $actor})-[:%v]->(:entity {name: $entity}))", req.Event)
	params = map[string]interface{}{
		"actor":  req.Actor,
		"entity": req.Entity,
	}
	return
}

func ParseStoreRequest(req *http.Request) (Query, error) {
	var request StorageRequest
	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&request)
	return request, err
}

type GetActorRequest struct {
	Actor string
}

func (req GetActorRequest) Query() (query string, params map[string]interface{}) {
	query = "match p=(:actor {name: $actor})-[]->() return p"
	params = map[string]interface{}{"actor": req.Actor}
	return
}

func ParseGetActorRequest(req *http.Request) (Query, error) {
	var request GetActorRequest
	decoder := json.NewDecoder(req.Body)
	decoder.DisallowUnknownFields()
	err := decoder.Decode(&request)
	return request, err
}

func ExecuteQuery(q Query, driver neo4j.Driver) ([]*neo4j.Record, error) {
	if q == nil {
		return nil, fmt.Errorf("Can not execute nil query")
	}
	session := driver.NewSession(neo4j.SessionConfig{})
	defer session.Close()
	return neo4j.Collect(session.Run(q.Query()))
}

func CreateDBQueryHandler(parser ParseFn, driver neo4j.Driver) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, req *http.Request) {
		if req.Method != "POST" {
			//todo error code
			fmt.Fprintf(w, "server only supports post\n")
			return
		}

		request, err := parser(req)
		if err != nil {
			fmt.Fprintf(w, "/recieved unparasable request: %v\n", err.Error())
			return
		}

		records, err := ExecuteQuery(request, driver)
		if err != nil {
			fmt.Fprintf(w, "DB Call failed %v\n", err.Error())
			return
		}

		for _, rec := range records {
			path, ok := rec.Get("p")
			if !ok {
				fmt.Fprintf(w, "Error Getting path type\n")
				continue
			}

			fmt.Fprintf(w, "%+v", path)
		}
	}
}

//todo, programmatically create table. Need uniqueness constraints on name.
func main() {
	driver, err := neo4j.NewDriver("bolt://localhost:7687", neo4j.NoAuth())
	if err != nil {
		log.Fatalf("Failed to start db connection: %v\n", err.Error())
	}
	if driver.VerifyConnectivity() != nil {
		log.Fatalf("Could not verify connection")
	}
	defer driver.Close()

	http.HandleFunc("/store", CreateDBQueryHandler(ParseStoreRequest, driver))
	http.HandleFunc("/getActorGraph", CreateDBQueryHandler(ParseGetActorRequest, driver))

	log.Fatal(http.ListenAndServe(":8080", nil))

}
