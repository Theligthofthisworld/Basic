#include  <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING,
    TYPE_BOOL,
    TYPE_NULL
} TypeValeur;

struct Variable {
    TypeValeur type;  // pour savoir quel genre de valeur c’est
    union {
        long long int i;
        long double f;
        char *s;
        int b; // pour booléen
    } value;
    char *name; // nom de la variable (utile pour stockage)
};

struct Variable CREATE_INTEGER(long long int value , char *name){
    struct Variable new;
    new.value.i=value;
    new.type=TYPE_INT;
    new.name=malloc(strlen(name)+1);
    strcpy(new.name,name);
    return new;

}

int main(void){
    struct Variable p;
    p=CREATE_INTEGER(14,"papa");
    printf(p.name);
}