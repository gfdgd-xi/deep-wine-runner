#include <iostream>
#include <filesystem>
using namespace std;
// 清屏
void CleanScreen(){
	/*if(filesystem::exists("/")){
		return;
	}*/
	system("clear");
}

int main(int argc, char* argv[]){
	// 判断参数是否齐全
	CleanScreen();
	//
	if(argc < 3) {
		cout << "参数不齐！" << endl;
		return 1;
	}
	cout << argc << endl;
	return 0;
}
