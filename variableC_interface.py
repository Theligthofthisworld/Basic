# De cette fonction on peut appeler les fonctions relatives a la gestion des fonctions

from cffi import FFI
class CInterface_V:
    def __init__(self, dll_path):
        self.ffi = FFI()
        self.lib = self.ffi.dlopen(dll_path)

        # Déclarations
        self.ffi.cdef("""
            typedef enum {
                TYPE_INT,
                TYPE_FLOAT,
                TYPE_STRING,
                TYPE_BOOL,
                TYPE_NULL
            } TypeValeur;

            struct Variable{
                TypeValeur type;
                union {
                    long long int i;
                    double f;
                    char *s;
                    int b;
                } value;
                char *name;
            } ;
        typedef struct hashmap hashmap;  // opaque

        """)

        self.ffi.cdef("""
            struct Variable* CREATE_INTEGER(long long int value, char *name);
            struct Variable* CREATE_FLOAT(long double value, char *name);
            struct Variable* CREATE_STRING(char *value, char *name);
            struct Variable* CREATE_BOOL(int value, char *name);
            int Var_free(void *item);
            hashmap* Create_hashmap(void);
            void hashmap_free(struct hashmap *map);
            const void *hashmap_set(struct hashmap *map, const void *item);
            const void *hashmap_get(const struct hashmap *map, const void *item);
            const void *get_variable(struct hashmap *map,struct Variable *var);
        """)
    def get_pointer_value(self,pointer):
        return self.ffi.cast("struct Variable *", pointer)
    def get_string_value(self,pointer):
        return self.ffi.string(pointer).decode("utf-8")


