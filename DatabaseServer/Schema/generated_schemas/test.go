
package schema
//AUTO GENERATED BY schema_gen.go from schemas/Test.yaml
type Test struct {
	foo string
	bar int
}

func (s Test) Insert() string {
	return "CREATE (:Test { foo: $foo,bar: $bar, })"	
}

func (s Test) Get() string {
	return "match p=(Test { foo: $foo,bar: $bar, })-[]->() return p"	
}
