#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int ref_count;
    int value;
    struct Node * next;
} Node;

#define HEAP_SIZE_INIT 1024
#define HEAP_SIZE_BUMP 512
int iHeapPos = 0;
int iHeapSize = 0;
Node * aHeap = NULL;
static Node empty_node = {-1, -1, (void *) -1};
Node * alloc_node() {
    if (iHeapPos >= iHeapSize) {
        if (aHeap == NULL) {
            aHeap = (Node *) malloc(HEAP_SIZE_INIT * sizeof(Node));
            memset(aHeap, -1, HEAP_SIZE_INIT * sizeof(Node));
            iHeapSize = HEAP_SIZE_INIT;
        } else {
            aHeap = (Node *) realloc(aHeap, (iHeapSize + HEAP_SIZE_BUMP) * sizeof(Node));
            memset(aHeap + iHeapSize, -1, HEAP_SIZE_BUMP * sizeof(Node));
            iHeapSize += HEAP_SIZE_BUMP;
        }
    }
    printf("   0x%08.8x = alloc_node()\n", &aHeap[iHeapPos]);
    return &aHeap[iHeapPos++];
}
Node * free_node(Node * node) {
    printf("   free_node(0x%08.8x)\n", node);
    if (node && node != (void *)-1)
        *node = empty_node;
    return NULL;
}
void release(Node * node) {
    printf("   release(0x%08.8x)\n", node);
    if (node && node != (void *)-1) {
        node->ref_count--;
        if (node->ref_count <= 0) {
            release(node->next);
            node = free_node(node);
        }
    }
}

Node * retain(Node * node) {
    if (node) node->ref_count++;
    return node;
}

Node * push(Node * stack, int value) {
    Node * new_stack = alloc_node();
    new_stack->ref_count = 1;
    new_stack->value = value;
    new_stack->next = retain(stack);
    return new_stack;
}

Node * pop(Node * stack, int * value) {
    Node * new_stack = retain(stack->next);
    *value = stack->value;
    release(stack);
    return new_stack;
}

void * free_stack(Node * stack) { release(stack); return NULL; }
void print_stack(Node * stack) {
    printf(" 0x%08.8x=[", stack);
    Node * curr = stack;
    while (curr && curr != (void *) -1) {
        printf(" %d(%d)", curr->value, curr->ref_count);
        curr = curr->next;
    }
    printf(" ]");
}

int main(void) {
    int popped;
    Node * stack1 = NULL;
    Node * stack2 = NULL;
    Node * stacks = NULL;

    stack1 = push(NULL, 66);        printf("  ");         print_stack(stack1); printf("\n");
    stack2 = push(stack1, 77);      printf("  ");         print_stack(stack2); printf("\n");
    stacks = stack2; retain(stacks);
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack1 = pop(stack1, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack1); printf("\n");
    release(stacks);                printf("  ");         print_stack(stacks); printf("\n");
    printf("\n");

    stack1 = push(NULL, 66);        printf("  ");         print_stack(stack1); printf("\n");
    stack2 = push(stack1, 77);      printf("  ");         print_stack(stack2); printf("\n");
    stack2 = push(stack2, 88);      printf("  ");         print_stack(stack2); printf("\n");
    stacks = stack2; retain(stacks);
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = push(stack2, 11);      printf("  ");         print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack1 = pop(stack1, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack1); printf("\n");
    release(stacks);                printf("  ");         print_stack(stacks); printf("\n");
    printf("\n");
    fflush(stdout);

    stack1 = free_stack(stack1); printf("  "); print_stack(stack1); printf("\n");
    stack2 = free_stack(stack2); printf("  "); print_stack(stack2); printf("\n");
    stacks = free_stack(stacks); printf("  "); print_stack(stacks); printf("\n");

    return 0;
}