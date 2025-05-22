#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int ref_count;
    int value;
    struct Node * next;
} Node;

void FREE(void * p) { /*free(p);*/ }
void release(Node * node) {
    if (node) {
        node->ref_count--;
        if (node->ref_count <= 0) {
            release(node->next);
            FREE(node); //  printf("Freeing: 0x%08.8x\n", node);
        }
    }
}

Node * push(Node * stack, int value) {
    Node * new_stack = malloc(sizeof(Node)); // printf("Allocated: 0x%08.8x\n", new_stack);
    new_stack->ref_count = 1;
    new_stack->value = value;
    new_stack->next = stack;
    if (stack) stack->ref_count++;
    return new_stack;
}

Node * pop(Node * stack, int * value) {
    Node * new_stack = stack->next;
    if (new_stack) new_stack->ref_count++;
    *value = stack->value;
    release(stack);
    return new_stack;
}

void free_stack(Node * stack) { release(stack); }
void print_stack(Node * stack) {
    printf(" 0x%08.8x=[", stack);
    Node * curr = stack;
    while (curr) {
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
    stack1 = push(stack1, 66);      printf("  "); print_stack(stack1); printf("\n");
    stack2 = push(stack1, 77);      printf("  "); print_stack(stack2); printf("\n");
    stacks = stack2;
    stack1 = pop(stack1, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack1); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    printf("\n");

    stack1 = push(stack1, 66);      printf("  "); print_stack(stack1); printf("\n");
    stack2 = push(stack1, 77);      printf("  "); print_stack(stack2); printf("\n");
    stacks = stack2;
    stack1 = pop(stack1, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack1); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = push(stack2, 11);      printf("  ");         print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    printf("\n");
    free_stack(stack1); printf("  "); print_stack(stacks); printf("\n");
    free_stack(stack2); printf("  "); print_stack(stacks); printf("\n");
    return 0;
}
