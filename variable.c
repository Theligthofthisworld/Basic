#include "variable.h"


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
struct Variable CREATE_STRING(char *value,char *name){
    struct Variable new;
    new.value.s=malloc(strlen(value)+1);
    if(!new.value.s) {
    fprintf(stderr, "Memory allocation error during variable creation\n");
    exit(1);
}
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
    return 0;
}

struct Variable CREATE_BOOL(int value,char *name){
    struct Variable new;
    new.value.b=value;
    new.type = TYPE_BOOL;
    new.name=malloc(strlen(name)+1);
    strcpy(new.name,name);
    return new;
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

