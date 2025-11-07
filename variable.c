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

struct Variable CREATE_INTEGER(long long int value , char *name){
    struct Variable new;
    new.value.i=value;
    new.type=TYPE_INT;
    new.name=malloc(strlen(name)+1);
    strcpy(new.name,name);
    return new;

}

struct Variable CREATE_FLOAT(long double value,char *name){
    struct Variable new;
    new.value.f=value;
    new.type=TYPE_FLOAT;
    new.name=malloc(strlen(name)+1);
    strcpy(new.name,name);
    return new;
}
struct Variable CREATE_CHAR(char *value,char *name){
    struct Variable new;
    new.value.s=malloc(strlen(value)+1);
    strcpy(new.value.s,value);
    new.name=malloc(strlen(name)+1);
    strcpy(new.name,name);
    return new;
}

int Var_free(void *item){
    struct Variable *v=item;
    free(v->name);
    if(v->type==TYPE_STRING){
        free(v->value.s);
    }
}

struct Variable CREATE_BOOL(int value,char *name){
    struct Variable new;
    new.value.b=value;
    new.name=malloc(strlen(name)+1);
    strcpy(new.name,name);
    return new;
}
int Variable_compare(const void *a, const void *b, void *udata) {
    const struct Variable *va = a;
    const struct Variable *vb = b;
    return strcmp(vb->name, va->name);
}

uint64_t Variable_hash(const void *item, uint64_t seed0, uint64_t seed1) {
    const struct Variable *var = item;
    return hashmap_sip(var->name, strlen(var->name), seed0, seed1);
}

int main(void){
    struct Variable i=CREATE_INTEGER(46,"mam");
    struct Variable in=CREATE_INTEGER(45,"mam");

    struct hashmap *map=hashmap_new(sizeof(struct Variable),0,0,0,Variable_hash,Variable_compare,NULL,NULL);
    hashmap_set(map,&i);
    hashmap_set(map,&in);
    char name[4]="mam";
    struct Variable *v = hashmap_get(map, &(struct Variable){ .name = "mam" });
    printf("%s  are %d",v->name,v->value.i);
    hashmap_free(map);
    return 0;


    
}
