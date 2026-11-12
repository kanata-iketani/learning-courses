// lesson09 ch01: Go にタプルはない（多値返却で代替）
package main

import "fmt"

// 商と余りを返します。戻り値の型を ( ) で並べるのが多値返却です
func divmod2(a, b int) (int, int) {
	return a / b, a % b
}

func main() {
	// 2 つの戻り値を、左から順に q と r で受け取ります
	q, r := divmod2(17, 5)
	fmt.Println(q)
	fmt.Println(r)

	// 多値は、そのまま別の関数の引数として渡すこともできます
	fmt.Println(divmod2(9, 2))
}
