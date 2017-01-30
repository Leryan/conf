#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PCRE_STATIC

#include <pcre.h>

pcre * c_pcre_compile(const char * const regex) {
    const char *pcreErrStr;
    int pcreErrOffset;

    pcre *c_pcreRegex = pcre_compile(
            regex,
            PCRE_CASELESS,
            &pcreErrStr, &pcreErrOffset, NULL);
    if(c_pcreRegex == NULL) {
        printf("PCRE compile error: %s: %d\n", pcreErrStr, pcreErrOffset);
        exit(EXIT_FAILURE);
    }
    return c_pcreRegex;
}

int main(void)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    int pcreExecRet;
    pcre_extra *pcreExtra;
    int subStrVec[128];


    int memTotal, memFree = 0;

    pcre *reMemTotal = c_pcre_compile("^MemTotal:[ ]+(.*) [a-zA-Z]+");
    pcre *reMemFree = c_pcre_compile("^MemFree:[ ]+(.*) [a-zA-Z]+");

    fp = fopen("/proc/meminfo", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    while ((read = getline(&line, &len, fp)) != -1) {
        pcreExecRet = pcre_exec(
                reMemTotal,
                pcreExtra,
                line,
                strlen(line),
                0, 0, subStrVec, 128);
        if(pcreExecRet >= 0) {
            printf("%s", line);
        }
        pcreExecRet = pcre_exec(
                reMemFree,
                pcreExtra,
                line,
                strlen(line),
                0, 0, subStrVec, 128);
        if(pcreExecRet >= 0) {
            printf("%s", line);
        }
    }

    fclose(fp);
    if (line)
        free(line);
    free(reMemTotal);
    free(reMemFree);

    exit(EXIT_SUCCESS);
}
