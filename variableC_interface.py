# De cette fonction on peut appeler les fonctions relatives a la gestion des fonctions

from cffi import FFI
print("hello")
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

            typedef struct {
                TypeValeur type;
                union {
                    long long int i;
                    double f;
                    char *s;
                    int b;
                } value;
                char *name;
            } Variable;
        typedef struct hashmap hashmap;  // opaque

        """)

        self.ffi.cdef("""
            Variable* CREATE_INTEGER(long long int value, char *name);
            Variable* CREATE_FLOAT(long double value, char *name);
            Variable* CREATE_STRING(char *value, char *name);
            Variable* CREATE_BOOL(int value, char *name);
            int Var_free(void *item);
            hashmap* Create_hashmap(void);
            void hashmap_free(struct hashmap *map);
            const void *hashmap_set(struct hashmap *map, const void *item);
        """)
print("rehello")
c = CInterface_V('vg-01.dll')
v = c.lib.CREATE_FLOAT(45.56,b"PAPA")
print(v.value.f)

