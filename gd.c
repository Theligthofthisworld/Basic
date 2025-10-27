#include <stdio.h>

int main() {
    int a = 5;
    int *p = &a;  // p pointe vers a

    printf("a = %d\n", a);      // 5
    printf("&a = %p\n", &a);    // adresse de a
    printf("p = %p\n", p);      // même adresse que &a
    printf("*p = %d\n", *p);    // contenu de a, donc 5

    *p = 10; // on change la valeur de a à travers le pointeur
    printf("a = %d\n", a); // a vaut maintenant 10
    return 0;
}
