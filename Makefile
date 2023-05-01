# MACHTYPE only needs to be specified for `pcc` and `alpha`
# MACHTYPE=pcc
HG_DEFS=-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_GNU_SOURCE -DMACHTYPE_$(MACHTYPE)
COPTS=-O2 -Isrc/pyblat/extc/header/core -Isrc/pyblat/extc/header/aux -Isrc/pyblat/extc/header/net $(HG_DEFS)

all: bin/blat bin/faToTwoBit bin/gfClient bin/gfServer

bin:
	mkdir bin

blat: bin
	$(CC) $(COPTS) $(CFLAGS) blat.c lib/core/*.c lib/aux/*.c -o bin/blat

faToTwoBit:
	$(CC) $(COPTS) $(CFLAGS) faToTwoBit.c lib/core/*.c lib/aux/*.c -o bin/faToTwoBit

gfClient:
	$(CC) $(COPTS) $(CFLAGS) gfClient.c lib/core/*.c lib/aux/*.c lib/net/*.c -o bin/gfClient

gfServer:
	$(CC) $(COPTS) $(CFLAGS) src/pyblat/extc/gfServer.c src/pyblat/extc/source/core/*.c src/pyblat/extc/source/aux/*.c src/pyblat/extc/source/net/*.c  -o bin/gfServer

gfServer2:
	$(CC) $(COPTS) $(CFLAGS) src/pyblat/extc/gfServer2.c src/pyblat/extc/source/core/*.c src/pyblat/extc/source/aux/*.c src/pyblat/extc/source/net/*.c  -o bin/gfServer -lm -pthread

clean:
	rm -f bin/*
