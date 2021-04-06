package schema

import (
	"fmt"
	"reflect"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

type Schema interface {
	// Insert returns cypher string that can insert the record into the db,
	Insert() string

	// Get returns cypher string that can get the record from the db,
	Get() string
}

type GraphObj interface {
	GetType() string
}

// func (r neo4j.Relationship) GetType() string {
// 	return r.Type
// }
//
// func (n neo4j.Node) GetType() string {
// 	return n.Labels[0]
// }
//
// //does this return copies??
// //todo this map should be auto generated from the schemas.
// var typeToStruct = map[string]interface{}{
// 	"actor": Actor{},
// }
//
// func GetStructForLabel(o GraphObj) (interface{}, error) {
// 	objType := o.GetType()
// 	str, ok := typeToStruct[kind.(string)]
// 	if !ok {
// 		return nil, fmt.Errorf("Unknown type %v\n", kind)
// 	}
//
// 	return str, nil
// }

func Decode(record *neo4j.Record, target interface{}) error {
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
