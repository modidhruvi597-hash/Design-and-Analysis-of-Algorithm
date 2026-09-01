#include <stdio.h>
int main(){
    int age;
    printf("Enter your age:");
    scanf("%d",&age);
    if(age>=18){
        printf("ELigible to vote\n");
    } else {
        printf("Not Eligible to vote\n");
    }
    return 0;
}