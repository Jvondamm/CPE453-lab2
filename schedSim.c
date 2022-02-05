#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    char *str;
    str = malloc(strlen(argv[1]) * argc);
    strcat(str, "sh shedSim.sh ");
    int i;
    for(i = 1; i < argc; ++i) 
    {
        strcat(str, argv[i]);
        strcat(str, " ");
    }
    int result = system(str);
    return result;
}
