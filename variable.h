#ifndef VARIABLE_H
#define VARIABLE_H

#include <stdint.h>  // pour uint64_t

// Définition du type enum pour les types de variable
typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING,
    TYPE_BOOL,
    TYPE_NULL
} TypeValeur;

// Structure principale pour une variable
struct Variable {
    TypeValeur type;   
    union {
        long long int i;
        long double f;
        char *s;
        int b; 
    } value;
    char *name; 
};

// Fonctions de création
struct Variable CREATE_INTEGER(long long int value, char *name);
struct Variable CREATE_FLOAT(long double value, char *name);
struct Variable CREATE_CHAR(char *value, char *name);
struct Variable CREATE_BOOL(int value, char *name);
struct hashmap* create_hashmap(void);
// Fonctions utilitaires pour hashmap
int Var_free(void *item);
int Variable_compare(const void *a, const void *b, void *udata);
uint64_t Variable_hash(const void *item, uint64_t seed0, uint64_t seed1);

#endif // VARIABLE_H
