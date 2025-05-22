#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int ref_count;
    int value;
    struct Node * next;
} Node;

void FREE(void * p) { /* free(p); */ }
void release(Node * node) {
    if (node) {
        node->ref_count--;
        if (node->ref_count <= 0) {
            release(node->next);
            FREE(node);
        }
    }
}

Node * retain(Node * node) {
    if (node) node->ref_count++;
    return node;
}

Node * push(Node * stack, int value) {
    Node * new_stack = malloc(sizeof(Node));
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

    stack1 = push(stack1, 66);      printf("  ");         print_stack(stack1); printf("\n");
    stack2 = push(stack1, 77);      printf("  ");         print_stack(stack2); printf("\n");
    stacks = stack2;
    stack1 = pop(stack1, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack1); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    printf("\n");

    stack1 = push(NULL, 66);        printf("  ");         print_stack(stack1); printf("\n");
    retain(stack1);                 printf("  ");         print_stack(stack1); printf("\n");
    stack2 = push(stack1, 77);      printf("  ");         print_stack(stack2); printf("\n");
    stack2 = push(stack2, 88);      printf("  ");         print_stack(stack2); printf("\n");
    stacks = stack2;
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = push(stack2, 11);      printf("  ");         print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    stack2 = pop(stack2, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack2); printf("\n");
    release(stack2);                printf("  ");         print_stack(stack2); printf("\n");
    stack1 = pop(stack1, &popped);  printf("%d", popped); print_stack(stacks); print_stack(stack1); printf("\n");
    printf("\n");

    stack1 = free_stack(stack1); printf("  "); print_stack(stack1); printf("\n");
    stack2 = free_stack(stack2); printf("  "); print_stack(stack1); printf("\n");
    stacks = free_stack(stacks); printf("  "); print_stack(stack1); printf("\n");

    return 0;
}