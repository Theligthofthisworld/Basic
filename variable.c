#include "variable.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashmap.h"

struct Variable CREATE_INTEGER(long long int value , char *name){
    struct Variable new;
    new.value.i=value;
    new.type=TYPE_INT;
    new.name=malloc(strlen(name)+1);
    if(!new.name) {
        fprintf(stderr, "Memory allocation error\n");
        exit(1);
    }
    strcpy(new.name,name);
    return new;
}

int Var_free(void *item) {
    struct Variable *v = item;
    if (v->name) free(v->name);
    if (v->type == TYPE_STRING && v->value.s) free(v->value.s);
    return 0;
}

int Variable_compare(const void *a, const void *b, void *udata) {
    const struct Variable *va = a;
    const struct Variable *vb = b;
    return strcmp(va->name, vb->name);
}

uint64_t Variable_hash(const void *item, uint64_t seed0, uint64_t seed1) {
    const struct Variable *var = item;
    return hashmap_sip(var->name, strlen(var->name), seed0, seed1);
}

struct hashmap* Create_hashmap(void){
    return hashmap_new(sizeof(struct Variable), 0, 0, 0, Variable_hash, Variable_compare, NULL, Var_free);
}

int insert_hashmap(struct Variable v, struct hashmap *map){
     hashmap_set(map, &v);
     return 0;
}

/*int main(void){
    struct hashmap *map = Create_hashmap();
    struct Variable v = CREATE_INTEGER(45,"papa");
    insert_hashmap(v, map);

    // Création d'une clé temporaire
    struct Variable key = {0};
    key.name = "papa";

    struct Variable *b = hashmap_get(map, &key);
    if(b){
        printf("Trouvé: %lld\n", b->value.i);
    } else {
        printf("Pas trouvé\n");
    }

    // Libération de la hashmap
    hashmap_free(map);
}*/
