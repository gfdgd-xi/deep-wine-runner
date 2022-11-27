/**********************************
 * 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
 * 版本：2.5.0
 * 更新时间：2022年11月27日
 * 只能在 Wine/Windows 运行
 **********************************/
#include <iostream> 
#include <string>
#include <fstream>
#include <Windows.h>
#pragma comment(lib, "version.lib");
using namespace std;

// 踩坑——如果要用 Dev CPP 编译这个文件，需要在编译选项加 -lversion 
//返回文件版本号
//@params:filename:文件名
string GetFileVersion(LPCWSTR filename)
{ 
	string asVer = "";
	VS_FIXEDFILEINFO *pVsInfo;
	unsigned int iFileInfoSize = sizeof(VS_FIXEDFILEINFO);
	int iVerInfoSize = GetFileVersionInfoSizeW(filename, NULL); 
	if(iVerInfoSize != 0)
	{ 
		char *pBuf = NULL;

		while(!pBuf)
		{
			pBuf = new char[iVerInfoSize];
		}
		if(GetFileVersionInfoW(filename, 0, iVerInfoSize, pBuf))
		{ 
			if(VerQueryValueA(pBuf, "\\", (void **)&pVsInfo, &iFileInfoSize))
			{ 
				sprintf(pBuf, "%d.%d.%d.%d", HIWORD(pVsInfo->dwFileVersionMS), LOWORD(pVsInfo->dwFileVersionMS), HIWORD(pVsInfo->dwFileVersionLS), LOWORD(pVsInfo->dwFileVersionLS));
				asVer = pBuf; 
			} 
		} 
		delete pBuf;
	}
	return asVer;
}

// 格式转换 
LPWSTR ConvertCharToLPWSTR(const char* szString)
{
	int dwLen = strlen(szString) + 1;
	int nwLen = MultiByteToWideChar(CP_ACP, 0, szString, dwLen, NULL, 0);//算出合适的长度
	LPWSTR lpszPath = new WCHAR[dwLen];
	MultiByteToWideChar(CP_ACP, 0, szString, dwLen, lpszPath, nwLen);
	return lpszPath;
}

int main(int argc, char* argv[]){
	if (argc < 2){
		cout << "Unfull Option" << endl;
		return 1;
	}
	string version = GetFileVersion(ConvertCharToLPWSTR(argv[1]));
	cout << "Version: " << version << endl;
	if (argc == 3){
		cout << "Write To " << argv[2] << endl;
		// 为了方便读取，写入文本文档 
		ofstream write(argv[2], ios::trunc);
		write << version;
		write.close();
	}
	return 0;
}
