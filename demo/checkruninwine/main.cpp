#include <windows.h>
#include <iostream>
//#include <stdlib.h>
//#include <stdio.h>
using namespace std;
int main(void)
{
    HKEY hKey;
    if(RegOpenKey(HKEY_LOCAL_MACHINE, TEXT("Software/Wine"), &hKey == ERROR_SUCCESS)){
    	cout << "Run In Wine" << endl;
    	return 0;
	}
	cout << "Don't 'Run In Wine" << endl;
    return 0;
}
