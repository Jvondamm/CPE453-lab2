PLAT=$(shell uname -i)

schedSim: schedSim.o
	cc -Wall -Werror -g schedSim.o -o schedSim

schedSim.o: schedSim.c
	cc -c -Wall -Werror -g schedSim.c -o schedSim.o
clean:
	rm -f *.o schedSim
