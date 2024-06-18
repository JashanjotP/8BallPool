CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: _phylib.so

clean:
		rm -f *.o *.so phylib.py phylib_wrap.c _phylib

libphylib.so: phylib.o
		$(CC) -shared -o libphylib.so phylib.o -lm

phylib.o: phylib.c phylib.h
		$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

phylib.py: phylib.i phylib.h
		swig -python phylib.i

phylib_wrap.o:
		$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: libphylib.so phylib.py phylib_wrap.o
		$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so