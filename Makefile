CC       := gcc
CFLAGS   := -Wall -Wextra -std=c11 -g -Icommon
SANFLAGS := -fsanitize=address,undefined

BIN_DIR  := bin

# Recursively find every .c file across all subdirectories (excluding common/)
SRCS     := $(filter-out common/%, $(shell find . -maxdepth 2 -name '*.c'))

# Map each source file to a binary in bin/ (e.g., 01_sorting_searching/foo.c -> bin/foo)
BINS     := $(foreach src, $(SRCS), $(BIN_DIR)/$(basename $(notdir $(src))))

.PHONY: all clean sanitize help

all: $(BINS)

# Generic rule to compile any binary from its source file
$(BIN_DIR)/%: $(SRCS) | $(BIN_DIR)
	@src=$$(find . -maxdepth 2 -name "$*.c" | head -n 1); \
	echo "[CC] $$src -> $@"; \
	$(CC) $(CFLAGS) $$src -o $@

# Build with AddressSanitizer + UndefinedBehaviorSanitizer enabled
sanitize: CFLAGS += $(SANFLAGS)
sanitize: clean all

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

clean:
	@rm -rf $(BIN_DIR)
	@echo "Cleaned $(BIN_DIR)/"

# Run any algorithm by basename: make run-insertion_sort
run-%: $(BIN_DIR)/%
	@./$<
