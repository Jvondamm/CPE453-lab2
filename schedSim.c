#include <stdio.h>
#include <strings.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    char *str;
    if((argc>=2)&&(str=strdup(argv[1])))
    {
            printf("argv[1] = %s\n", str);
            free(str);
            return 0;
    }
    else
    {
        return 1;
    }
    /* int result = system("python3 sched_sim.py"); */
}