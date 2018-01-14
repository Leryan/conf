#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define CMP_BAD_TYPE -2
#define CMP_BAD_SIZE -1
#define CMP_BAD_VALUE 0
#define CMP_OK 1

typedef enum value_type {
    Int8,
    Int16,
    Int32,
    Int64,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    String,
    Char
}ValueType;

typedef struct value {
    size_t      size;
    ValueType   type;
    void        *value;
}Value;

int compare(const Value *v1, const Value *v2) {
    if (v1->type != v2->type) {
        return CMP_BAD_TYPE;
    }

    if (v1->size != v2->size) {
        return CMP_BAD_SIZE;
    }

    if (memcmp(v1->value, v2->value, v1->size) == 0) {
        return CMP_OK;
    }

    return CMP_BAD_VALUE;
}

void result(int n, int want) {
    if (n == want) {
        printf("ok:  %d\n", n);
    } else {
        printf("nok: %d\n", n);
    }
}

int main(void) {
    int i = 0;
    int j = 0;
    char c = 0;
    uint8_t ui8 = 0;
    uint64_t ui64 = 0;
    int64_t i64 = 0;
    uint64_t ui641 = 1;
    uint64_t ui640 = 0;

    Value v1 = {sizeof(i), Int32, &i};
    Value v2 = {sizeof(j), Int32, &j};
    Value v3 = {sizeof(c), Char, &c};
    Value v4 = {sizeof(ui8), UInt8, &ui8};
    Value v5 = {sizeof(ui8), Char, &ui8}; // Fake type
    Value v6 = {sizeof(ui64), UInt64, &ui64};
    Value v7 = {sizeof(i64), Int64, &i64};
    Value v8 = {sizeof(ui641), UInt64, &ui641};
    Value v9 = {sizeof(ui640), UInt64, &ui640};

    result(compare(&v1, &v2), CMP_OK);
    result(compare(&v3, &v4), CMP_BAD_TYPE);
    result(compare(&v3, &v5), CMP_OK);
    result(compare(&v5, &v6), CMP_BAD_TYPE);
    result(compare(&v6, &v7), CMP_BAD_TYPE);
    result(compare(&v8, &v9), CMP_BAD_VALUE);
}
