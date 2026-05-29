var a = 0
var b = 10
var c = 0

cycle (a = 0; a < b; a = a + 1) {
    check (a == 5) {
        c = c + a
    } otherwise {
        c = c + 1
    }

    repeat (c < 5) {
        c = c + 1
    }
}
printx c