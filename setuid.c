#include "stdlib.h"
#include "stdio.h"
#include "sys/types.h"
#include "unistd.h"

#define DROP_UID 1001

int main(void) {
    /*
     * When the binary on filesystem is chmod u+s,
     * the Effective UID will be 0.
     *
     * The Real UID will remain the original UID
     * of the user running this program.
     */
    puts("Initial launch:");
    printf("euid: %i\n", geteuid());
    printf("ruid: %i\n\n", getuid());

    /**
     * Now we change the Real UID to match the Effective UID.
     */
    setuid(geteuid());

    puts("After privilege escalation through FS setuid:");
    printf("euid: %i\n", geteuid());
    printf("ruid: %i\n\n", getuid());

    /**
     * Drop our privileges by setting the Real UID only.
     */
    setuid(DROP_UID);

    puts("After privilege drop:");
    printf("euid: %i\n", geteuid());
    printf("ruid: %i\n", getuid());

    return EXIT_SUCCESS;
}
