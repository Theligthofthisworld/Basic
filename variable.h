#ifndef VARIABLE_H
#define VARIABLE_H
#define SCALE 1000000000

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashmap.h"

typedef struct {
    int raw;
} Number;

typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING,
    TYPE_BOOL,
    TYPE_NULL
} TypeValeur;

struct Variable {
    TypeValeur type;
    union {
        long long int i;
        double f;
        char *s;
        int b;
    } value;
    char *name;
};


struct Variable* CREATE_INTEGER(long long int value, char *name);
struct Variable* CREATE_FLOAT(double value, char *name);
struct Variable* CREATE_STRING(char *value, char *name);
struct Variable* CREATE_BOOL(int value, char *name);
int Var_free(void *item);
int Variable_compare(const void *a,const void *b, void *udata);
uint64_t Variable_hash(const void *item, uint64_t seed0, uint64_t seed1);
struct hashmap*  Create_hashmap(void);
const void *get_variable(struct hashmap *map,struct Variable *var);
Number make(double x);
double to_double(Number n);
double add_double(Number a , Number b);
void debug_scale();


#endif
