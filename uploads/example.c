#include <stdio.h>

int fib(int a, int b, int n)
{
    for(int i = 0; i <= n; i++){
        printf("%d\n", a);
        a = b;
        b = a + b;
    }
}

int main(){
    fib(0, 1, 7);
    return 0;
}