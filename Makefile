SHELL := /bin/bash

help:  ## Show help
	@grep -E '^[.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# MACHTYPE only needs to be specified for `pcc` and `alpha`
PYBIND11:=$(shell python -m pybind11 --includes)
LDFLAGS:=${LDFLAGS}
HG_DEFS=-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_GNU_SOURCE -DMACHTYPE_$(MACHTYPE)
COPTS=-O2 -Isrc/pxblat/extc/include/core -Isrc/pxblat/extc/include/aux -Isrc/pxblat/extc/include/net -Isrc/pxblat/extc/bindings $(PYBIND11) $(LDFLAGS) $(HG_DEFS)  -Wunused-variable

ifeq ($(shell uname), Darwin)
    COPTS += -undefined dynamic_lookup
endif

AUXSRC=$(filter-out src/pxblat/extc/src/aux/netlib.c, $(wildcard src/pxblat/extc/src/aux/*.c))
CORESRC=$(wildcard src/pxblat/extc/src/core/*.c)
NETSRC=$(wildcard src/pxblat/extc/src/net/*.c)

# compile dynamic lib
LIBLDFLAGS:=${LDFLAGS} -shared -lm -pthread -lhts -lssl -lcrypto -lz
# compile static lib
# LIBLDFLAGS:=${LDFLAGS}  -lm -pthread -lhts -lssl -lcrypto -lz
OBJS=$(AUXSRC:.c=.o) $(CORESRC:.c=.o) $(NETSRC:.c=.o)

# Target library name
LIBRARY=libblat.so
SLIBRARY=libblat.a
# Archiver
AR=ar

# Rule to compile source files into object files
%.o: %.c
	# $(CC) $(COPTS) $(CFLAGS)  -c $< -o $@
	$(CC) $(COPTS) $(CFLAGS) -fPIC  -c $< -o $@

# Rule to link object files into a shared library
$(LIBRARY): $(OBJS)
	$(CC) $(LIBLDFLAGS) -o $@ $^

$(SLIBRARY): $(OBJS)
	$(AR) $(ARFLAGS) $@ $^


all_bin: faToTwoBit gfClient gfServer

bin: ## Create bin folder
	mkdir bin

blat: bin ## Build blat
	$(CC) $(COPTS) $(CFLAGS) -DBLAT src/pxblat/extc/blat.c src/pxblat/extc/src/core/*.c src/pxblat/extc/src/aux/*.c -o bin/blat -lm -pthread -lhts -lssl -lcrypto

faToTwoBit: bin ## Build faToTwoBit
	$(CC) $(COPTS) $(CFLAGS) src/pxblat/extc/faToTwoBit.c src/pxblat/extc/src/core/*.c $(AUXSRC) src/pxblat/extc/src/net/*.c  -o bin/faToTwoBit -lm -pthread -lhts -lssl -lcrypto

twoBitToFa: bin ## Build twoBitToFa
	$(CC) $(COPTS) $(CFLAGS) -DPXBLATLIB src/pxblat/extc/twoBitToFa.c src/pxblat/extc/src/core/*.c $(AUXSRC) src/pxblat/extc/src/net/*.c  -o bin/twoBitToFa -lm -pthread -lhts -lssl -lcrypto

gfClient: bin ## Build gfClient
	$(CC) $(COPTS) $(CFLAGS)  src/pxblat/extc/gfClient.c src/pxblat/extc/src/core/*.c $(AUXSRC) src/pxblat/extc/src/net/*.c  -o bin/gfClient -lm -pthread -lhts -lssl -lcrypto

gfServer: bin ## Build gfServer
	$(CC) $(COPTS) $(CFLAGS) src/pxblat/extc/gfServer.c src/pxblat/extc/src/core/*.c $(AUXSRC) src/pxblat/extc/src/net/*.c  -o bin/gfServer -lm -pthread -lhts -lssl -lcrypto

clean: ## Clean autogenerated files
	# rm -f bin/*
	rm -rf dist
	rm -rf build
	rm -rf fixed_wheels
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . -name "*.o" -type f -delete
	find . -name "*.so" -type f -delete
	rm -f .coverage

clean-logs: ## Clean logs
	rm -rf logs/**
	rm -rf export
	rm -rf pdf_files

format: ## Run pre-commit hooks
	pre-commit run -a

commit: format ## Commit changes
	git add .
	aicommits -a --type conventional


change:
	git cliff --output CHANGELOG.md

clangd: ## Generate clangd index
	bear -- make all_bin

test: ## Run tests
	pytest -vls tests

install: binder ## install the lib
	poetry install -vvvv
	echo "Installing pxblat"

clean-stubs:
	rm -rf stubs

stubs: clean-stubs ## Generate pybind11 stubs
	echo "Generating pybind11 stubs"
	pybind11-stubgen pxblat._extc.cppbinding
	cp stubs/pxblat/_extc/cppbinding-stubs/__init__.pyi src/pxblat/extc/__init__.pyi
	rm -rf stubs

BINDER_DIR=src/pxblat/extc/bindings/binder

binder: ## Generate pybind11 bindings
	echo "Generating pybind11 bindings"
	singularity  run -B  .:/bind  docker://yangliz5/binder-pxblat \
		binder --root-module _extc \
		--prefix /bind/$(BINDER_DIR) \
		--config /bind/binder.cfg \
		--include-pybind11-stl \
		/bind/all_includes.hpp \
		-- -I/bind/src/pxblat/extc/include/core \
		-I/bind/src/pxblat/extc/include/aux \
		-I/bind/src/pxblat/extc/include/net \
		-I/bind/src/pxblat/extc/bindings \
		--std=c++17 \
		-DNDEBUG

update:
	pre-commit autoupdate
	poetry update
