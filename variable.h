#ifndef VARIABLE_H
#define VARIABLE_H


#include  <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashmap.h"

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
    char *name; // nom de la variable (ca va m'aider avec les hashmap)
};
// Possible variable and freedom
struct Variable CREATE_INTEGER(long long int value,char *name);
struct Variable CREATE_FLOAT(long double value, char *name);
struct Variable CREATE_STRING(char *value,char *name);
struct Variable CREATE_BOOL(int value,char *name);
int Var_free(void *item);


// hashmap utilities

int Variable_compare(const void *a,const void *b, void *udata);
uint64_t Variable_hash(const void *item, uint64_t seed0, uint64_t seed1);

#endif