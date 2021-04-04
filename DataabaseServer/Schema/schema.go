package schema

import (
	"fmt"
	"reflect"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

// DB schemas
type Actor struct {
	Name string
}

func Decode(record neo4j.Record, target interface{}) error {
	//check that the passed in target is a struct
	t := reflect.ValueOf(target).Elem()
	if t.Kind() != reflect.Struct {
		return fmt.Errorf("Can not decode into non struct target: got %v\n", t.Kind())
	}

	//get names of fields in the response
	for _, key := range record.Keys {
		val, ok := record.Get(key)
		if !ok {
			//should we actually just abort here? this is very
			//unexpected
			fmt.Printf("cant find %v on result\n", key)
			continue
		}

		structField := t.FieldByName(key)
		if !structField.IsValid() {
			fmt.Printf("cant find %v on struct\n", key)
		}

		if !structField.CanSet() {
			fmt.Printf("Cant set field %v\n", structField.Kind())
			continue
		}

		switch structField.Kind() {
		case reflect.Int:
			structField.SetInt(int64(val.(int)))
		case reflect.String:
			structField.SetString(val.(string))
		default:
			fmt.Printf("Unsupprted type %v\n", structField.Kind())
		}
	}

	return nil
}
