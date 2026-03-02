PYTHON     := python3
CC         := gcc
PY_CFLAGS  := $(shell $(PYTHON)-config --includes)
CFLAGS     := -O2 -Wall -Wextra -fPIC -std=c11 \
              $(PY_CFLAGS) \
              -I src \
              -Wno-missing-field-initializers \
              -Wno-sign-compare \
              -Wno-unused-function \
              -Wno-unused-variable
LDFLAGS    := $(shell $(PYTHON)-config --ldflags) \
              $(shell $(PYTHON)-config --libs 2>/dev/null || echo '')
EXT_SUFFIX := $(shell $(PYTHON)-config --extension-suffix)

TARGET  := sno4py$(EXT_SUFFIX)
SRCS    := src/sno4py.c src/spipat.c src/spipat_stubs.c src/image.c src/image_strs.c
OBJS    := $(SRCS:.c=.o)

.PHONY: all test clean

all: $(TARGET)

%.o: %.c
	@echo "  CC  $<"
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET): $(OBJS)
	@echo "  LD  $@"
	$(CC) -shared $(OBJS) -o $(TARGET) $(LDFLAGS)
	@echo "  OK  $(TARGET)"

src/spipat.o: src/spipat.c src/spipat.h src/spipat_impl.h src/xmatch.h
src/sno4py.o: src/sno4py.c src/spipat.h
src/spipat_stubs.o: src/spipat_stubs.c src/spipat.h

test: all
	$(PYTHON) tests/test_bead_stage1.py

clean:
	rm -f $(TARGET) $(OBJS)
	rm -rf __pycache__ tests/__pycache__
