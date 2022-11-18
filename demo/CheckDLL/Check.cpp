/**********************************
 * 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
 * 版本：2.5.0
 * 更新时间：2022年11月18日
 * 只能在 Wine/Windows 运行
 **********************************/
#include <iostream>
#include <Windows.h>
using namespace std;
int main(int argc, char* argv[]){
	HINSTANCE hdll;
	hdll = LoadLibrary(argv[1]);
	if(argv[1] == ""){
		cout << "Don't have full parameter" << endl;
		return 2; 
	}
	cout << "Checking " << argv[1] << " ......" << endl;
	if(hdll == NULL){
		cout << "Error, can't load this library." << endl;
		return 1;
	}
	cout << "No Problem!" << endl;
	return 0;
}
