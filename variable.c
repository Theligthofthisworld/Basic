#include "variable.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashmap.h"

/* To compile the file gcc -shared -o vg-01.dll variable.c hashmap.c -Wl,--out-implib */

// Variable structure
struct Variable* CREATE_INTEGER(long long int value , char *name){
    struct Variable *new = malloc(sizeof(struct Variable)); 
    if(!new) exit(1);
    
    new->value.i = value;
    new->type = TYPE_INT;
    new->name = malloc(strlen(name) + 1);
    strcpy(new->name, name);
    return new;
}


struct Variable* CREATE_FLOAT(double value,char *name){
    struct Variable *new = malloc(sizeof(struct Variable));
    if(!new) exit(1);

    new->value.f = value;
    new->type = TYPE_FLOAT;
    new->name = malloc(strlen(name)+1);
    strcpy(new->name, name);

    return new;
}

struct Variable* CREATE_STRING(char *value,char *name){
    struct Variable *new = malloc(sizeof(struct Variable));
    if(!new) exit(1);

    new->type = TYPE_STRING;

    new->value.s = malloc(strlen(value)+1);
    strcpy(new->value.s, value);

    new->name = malloc(strlen(name)+1);
    strcpy(new->name, name);


    return new;
}

struct Variable* CREATE_BOOL(int value , char *name){
    struct Variable *new = malloc(sizeof(struct Variable)); 
    if(!new) exit(1);
    new->value.b=value;
    new->type = TYPE_BOOL;
    new->name = malloc(strlen(name) + 1);
    strcpy(new->name, name);
    return new;
}
// END


// USEFUL
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

const void *get_variable(struct hashmap *map,struct Variable *var){
    return hashmap_get(map,&var);
}
//END

// FLOAT CALCULUS PRECISIONS

Number make(double x){
    Number temp;
    temp.raw=(int)(SCALE*x);
    return temp;
}

double to_double(Number n){
    return (double)n.raw / SCALE;
}
double add_double(Number a, Number b){
    Number r;
    r.raw = a.raw + b.raw;
    return to_double(r);
}
/*int main(void){
    //setbuf(stdout, NULL);
    //fflush(stdout);
    struct hashmap *map = Create_hashmap();
    //printf("Code : ") n'effacez pas ici sinon rien n'apparaitras dans le terminal DONT ERASE THIS LINES
    struct Variable *v = CREATE_FLOAT(45.5656,"papa");
    
    printf("%f",v->value.f);
    Var_free(v);
    hashmap_free(map);

    return 0;
}*/

int main(void){
    struct hashmap *map = Create_hashmap();

    struct Variable *v = CREATE_FLOAT(45.5656, "papa");

    hashmap_set(map, v);   

    struct Variable *var = hashmap_get(map, v);

    if (var) {
        printf("%f\n", var->value.f);
    } else {
        printf("Variable non trouvée\n");
    }

    hashmap_free(map);
    return 0;
}
