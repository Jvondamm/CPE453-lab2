PLAT=$(shell uname -i)

schedSim: schedSim.o
	cc -Wall -Werror -g -c -o $@ $<
	cc -S $<

schedSim.o: schedSim.c
	cc -Wall -Werror -g -c -o $@ $<
	cc -S $<

clean:
	rm -f *.o schedSim