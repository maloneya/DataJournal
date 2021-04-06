package schema

import (
	"testing"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

type TestStruct struct {
	Foo string
	Bar int
}

func TestDecode(t *testing.T) {
	record := neo4j.Record{
		Values: []interface{}{
			"foo",
			1,
		},
		Keys: []string{
			"Foo",
			"Bar",
		},
	}

	var x TestStruct
	err := Decode(&record, &x)
	if err != nil {
		t.Errorf("Decode err: %v\n", err)
	}

	if x.Foo != "foo" {
		t.Errorf("field foo expected foo got %v\n", x.Foo)
	}

	if x.Bar != 1 {
		t.Errorf("field Bar expected 1 got %v\n", x.Bar)
	}
}
