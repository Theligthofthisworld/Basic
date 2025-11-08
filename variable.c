#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "variable.h"
#include "hashmap.h"  


struct Variable CREATE_INTEGER(long long int value, char *name) {
    struct Variable new;
    new.value.i = value;
    new.type = TYPE_INT;
    new.name = malloc(strlen(name) + 1);
    strcpy(new.name, name);
    return new;
}


struct Variable CREATE_FLOAT(long double value, char *name) {
    struct Variable new;
    new.value.f = value;
    new.type = TYPE_FLOAT;
    new.name = malloc(strlen(name) + 1);
    strcpy(new.name, name);
    return new;
}


struct Variable CREATE_CHAR(char *value, char *name) {
    struct Variable new;
    new.value.s = malloc(strlen(value) + 1);
    strcpy(new.value.s, value);
    new.type = TYPE_STRING;
    new.name = malloc(strlen(name) + 1);
    strcpy(new.name, name);
    return new;
}


struct Variable CREATE_BOOL(int value, char *name) {
    struct Variable new;
    new.value.b = value;
    new.type = TYPE_BOOL;
    new.name = malloc(strlen(name) + 1);
    strcpy(new.name, name);
    return new;
}


int Var_free(void *item) {
    struct Variable *v = (struct Variable *)item;
    if (v->name) free(v->name);
    if (v->type == TYPE_STRING && v->value.s) free(v->value.s);
    return 0;  // retourne 0 pour indiquer succès
}


int Variable_compare(const void *a, const void *b, void *udata) {
    const struct Variable *va = (const struct Variable *)a;
    const struct Variable *vb = (const struct Variable *)b;
    return strcmp(vb->name, va->name);
}


uint64_t Variable_hash(const void *item, uint64_t seed0, uint64_t seed1) {
    const struct Variable *var = (const struct Variable *)item;
    return hashmap_sip(var->name, strlen(var->name), seed0, seed1);
}

struct hashmap* create_hashmap(void){
    return hashmap_new(sizeof(struct Variable), 0, 0, 0, Variable_hash, Variable_compare, NULL, NULL);
}

/*  
int main(void) {
    struct Variable i = CREATE_INTEGER(46, "mam");
    struct Variable in = CREATE_INTEGER(45, "mama");

    struct hashmap *map = hashmap_new(sizeof(struct Variable), 0, 0, 0, Variable_hash, Variable_compare, NULL, NULL);
    hashmap_set(map, &i);
    hashmap_set(map, &in);

    struct Variable *v = hashmap_get(map, &(struct Variable){ .name = "mam" });
    printf("%s  are %lld\n", v->name, v->value.i);

    hashmap_free(map);
    return 0;
}
je suis trop fier je l'ai fais eul :) */

