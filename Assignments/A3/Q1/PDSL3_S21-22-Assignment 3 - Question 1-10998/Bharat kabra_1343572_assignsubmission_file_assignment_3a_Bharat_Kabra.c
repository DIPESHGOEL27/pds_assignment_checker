/*
Name- Bharat Kabra
Roll: 21CH10015
Dept: Chemical
Package: Codeblocks
Assignment class: 3
*/
#include<stdio.h>

int strln(char s[])
{
    int len = 0;
    while (*(s++) != '\0' )
    {
        len++;
    }
    return len;
}

int main() {
    char un[100], ps[100];
    printf("Username: ");
    scanf("%s",un);
    printf("Password: ");
    scanf("%s",ps);
    int up=0,low=0,sp=0,num=0;
    int len = strln(ps);
    int lu = strln(un);
    int flag =0;

    for (int i=0; i<len; i++){
        if (ps[i]>=65 && ps[i]<=90){
            up+= 1;
        }
    }

    for (int i=0; i<len; i++){
        if (ps[i]>=97 && ps[i]<=122){
            low+= 1;
        }
    }

    for (int i=0; i<len; i++){
        if (ps[i] == '$' || ps[i] == '*' ||ps[i] == '_' ||ps[i] == '@' ||ps[i] == '#' ||ps[i] == '/' ||ps[i] == '<' ||ps[i] == '>' ||ps[i] == '!' || ps[i] == '+' ||ps[i] == '?' ){
            sp+= 1;
        }
    }

    for (int j=0; j<len; j++)
    {
        num =0;
        for (int i=j; i<len;i++)
        {

          if (ps[i] == '0' || ps[i] == '1' ||ps[i] == '2' ||ps[i] == '3' ||ps[i] == '4' ||ps[i] == '5' ||ps[i] == '6' ||ps[i] == '7' ||ps[i] == '8' || ps[i] == '9' )
          {
             num+= 1;
          }

        }

    if (!(len<=15 && len >=8)){
        printf("Not Acceptable");
         return 0;
    }
    //counting uppercase and lowercase

    else if (up < 1){
        printf("Not Acceptable");
         return 0;
    }

    else if (low < 1){
        printf("Not Acceptable");
         return 0;
    }

    else if (sp < 2){
        printf("Not Acceptable");
         return 0;
    }

    else if (num==5){
        printf("Not Acceptable");
         return 0;
        break;
    }

    for (int i=0; i<len-lu+1; i++)
    {
        flag =0;
        for(int j=0;j<lu;j++)
        {

            if(un[j]==ps[j+i])
            {

                flag ++;
                if (flag == lu){
                  printf("Not Acceptable\n");
                  return 0;

                  break;
                }
            }


            else
            {
                break;
            }
        }


    }
    //   printf("%d\n", flag);

    //maximun 5 digits

    // printf("%d",num);

    }

    for(int i=0;i<len;i++){
      int f=0;
      for(int j=i;j<len;j++){
        if(ps[i]==ps[j]){
          f++;
        }
      if(f==5){

        break;
      }
      }
      if(f==5){
      printf("Not Acceptable\n");
      return 0;
      break;
      }
    }
    printf("Acceptable");


}
