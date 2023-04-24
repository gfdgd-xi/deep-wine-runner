/*
  归属 RacoonGX 团队，开发者：gfdgd xi
 */
#include <iostream>
#include <vector>
#include <filesystem>
#include <shlobj.h>
#include <fstream>
using namespace std;

string mainlist[] = {"Visual C++ 运行库", ".net framework 运行库"};
string vcppName[] = {
	"2005 Service Pack 1 Redistributable Package MFC 安全更新", 
	"2008 (VC++ 9.0) SP1 (不再支持) X86",
	"2008 (VC++ 9.0) SP1 (不再支持) X64",
	"2010 (VC++ 10.0) SP1 (不再支持) X86",
	"2010 (VC++ 10.0) SP1 (不再支持) X64",
	"2012 (VC++ 11.0) Update 4 X86",
	"2012 (VC++ 11.0) Update 4 X64",
	"2013 (VC++ 12.0) X86",
	"2013 (VC++ 12.0) X64",
	"2015、2017、2019 和 2022 X86",
	"2015、2017、2019 和 2022 X64",
	"2015、2017、2019 和 2022 ARM64",
	"VC6 运行库"
};
string vcppUrl[] = {
	"http://download.microsoft.com/download/4/A/2/4A22001F-FA3B-4C13-BF4E-42EC249D51C4/vcredist_x86.EXE",
	"http://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x86.exe",
	"http://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x64.exe",
	"http://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe",
	"http://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe",
	"http://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x86.exe",
	"http://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x64.exe",
	"http://aka.ms/highdpimfc2013x86enu",
	"http://aka.ms/highdpimfc2013x64enu",
	"http://aka.ms/vs/17/release/vc_redist.x86.exe",
	"http://aka.ms/vs/17/release/vc_redist.x64.exe",
	"http://aka.ms/vs/17/release/vc_redist.arm64.exe",
	"http://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vscpp/VC6RedistSetup_deu.exe"
};
string netName[] = {
	"3.5 SP1 Offline Installer",
	"4.0 Offline Installer",
	"4.5 Web Installer",
	"4.5.1 Offline Installer",
	"4.5.2 Offline Installer",
	"4.6 Offline Installer",
	"4.6.1 Offline Installer",
	"4.6.2 Offline Installer",
	"4.7 Offline Installer",
	"4.7.1 Offline Installer",
	"4.7.2 Offline Installer",
	"4.8 Offline Installer",
	"4.8.1 Offline Installer",
	".NET 5.0 Desktop Runtime (v5.0.17) - Windows x86 Installer",
	".NET 5.0 Desktop Runtime (v5.0.17) - Windows x64 Installer",
	".NET 5.0 Desktop Runtime (v5.0.17) - Windows Arm64 Installer",
	".NET Core 3.0 Desktop Runtime (v3.0.3) - Windows x86 Installer",
	".NET Core 3.0 Desktop Runtime (v3.0.3) - Windows x64 Installer",
	".NET Core 3.1 Desktop Runtime (v3.1.28) - Windows x86 Installer",
	".NET Core 3.1 Desktop Runtime (v3.1.28) - Windows x64 Installer",
	".NET 6.0 Desktop Runtime (v6.0.8) - Windows x86 Installer",
	".NET 6.0 Desktop Runtime (v6.0.8) - Windows x64 Installer",
	".NET 6.0 Desktop Runtime (v6.0.8) - Windows Arm64 Installer",
	"Microsoft .NET Framework 1.1 版可转散发套件",
	"Microsoft .NET Framework 2.0 Service Pack 1 (x86)",
	"Microsoft .NET Framework 集合包",
	"Microsoft .NET Framework 3.5 便携版"
};
string netUrl[] = {
	"http://download.visualstudio.microsoft.com/download/pr/b635098a-2d1d-4142-bef6-d237545123cb/2651b87007440a15209cac29634a4e45/dotnetfx35.exe",
	"http://download.microsoft.com/download/9/5/A/95A9616B-7A37-4AF6-BC36-D6EA96C8DAAE/dotNetFx40_Full_x86_x64.exe",
	"http://download.microsoft.com/download/B/A/4/BA4A7E71-2906-4B2D-A0E1-80CF16844F5F/dotNetFx45_Full_setup.exe",
	"http://download.microsoft.com/download/1/6/7/167F0D79-9317-48AE-AEDB-17120579F8E2/NDP451-KB2858728-x86-x64-AllOS-ENU.exe",
	"http://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe",
	"http://download.microsoft.com/download/6/F/9/6F9673B1-87D1-46C4-BF04-95F24C3EB9DA/enu_netfx/NDP46-KB3045557-x86-x64-AllOS-ENU_exe/NDP46-KB3045557-x86-x64-AllOS-ENU.exe",
	"http://download.microsoft.com/download/E/4/1/E4173890-A24A-4936-9FC9-AF930FE3FA40/NDP461-KB3102436-x86-x64-AllOS-ENU.exe",
	"http://download.visualstudio.microsoft.com/download/pr/8e396c75-4d0d-41d3-aea8-848babc2736a/80b431456d8866ebe053eb8b81a168b3/ndp462-kb3151800-x86-x64-allos-enu.exe",
	"http://download.visualstudio.microsoft.com/download/pr/2dfcc711-bb60-421a-a17b-76c63f8d1907/e5c0231bd5d51fffe65f8ed7516de46a/ndp47-kb3186497-x86-x64-allos-enu.exe",
	"http://download.visualstudio.microsoft.com/download/pr/4312fa21-59b0-4451-9482-a1376f7f3ba4/9947fce13c11105b48cba170494e787f/ndp471-kb4033342-x86-x64-allos-enu.exe",
	"http://download.visualstudio.microsoft.com/download/pr/1f5af042-d0e4-4002-9c59-9ba66bcf15f6/089f837de42708daacaae7c04b7494db/ndp472-kb4054530-x86-x64-allos-enu.exe",
	"http://download.visualstudio.microsoft.com/download/pr/2d6bb6b2-226a-4baa-bdec-798822606ff1/8494001c276a4b96804cde7829c04d7f/ndp48-x86-x64-allos-enu.exe",
	"http://download.visualstudio.microsoft.com/download/pr/6f083c7e-bd40-44d4-9e3f-ffba71ec8b09/3951fd5af6098f2c7e8ff5c331a0679c/ndp481-x86-x64-allos-enu.exe",
	"http://download.visualstudio.microsoft.com/download/pr/b6fe5f2a-95f4-46f1-9824-f5994f10bc69/db5ec9b47ec877b5276f83a185fdb6a0/windowsdesktop-runtime-5.0.17-win-x86.exe",
	"http://download.visualstudio.microsoft.com/download/pr/3aa4e942-42cd-4bf5-afe7-fc23bd9c69c5/64da54c8864e473c19a7d3de15790418/windowsdesktop-runtime-5.0.17-win-x64.exe",
	"http://download.visualstudio.microsoft.com/download/pr/be25784a-4231-4c53-ba6e-869166ef523f/9602c6c0d358d31dc710fd0573fc39e0/windowsdesktop-runtime-5.0.17-win-arm64.exe",
	"http://download.visualstudio.microsoft.com/download/pr/e312618d-85c4-4cad-b660-569b5522eca9/e951e76ebe011b5d3ea1289ef68e8281/windowsdesktop-runtime-3.0.3-win-x86.exe",
	"http://download.visualstudio.microsoft.com/download/pr/c525a2bb-6e98-4e6e-849e-45241d0db71c/d21612f02b9cae52fa50eb54de905986/windowsdesktop-runtime-3.0.3-win-x64.exe",
	"http://download.visualstudio.microsoft.com/download/pr/d2ec7ca2-017d-4d06-a6da-3707daa3c3b1/1f2e108653e3d8316e1657105ef24b93/windowsdesktop-runtime-3.1.28-win-x86.exe",
	"http://download.visualstudio.microsoft.com/download/pr/5c74593e-f156-44c8-9957-f11996de72bc/d3e0e26c64a5a2d860c5c0deca975d78/windowsdesktop-runtime-3.1.28-win-x64.exe",
	"http://download.visualstudio.microsoft.com/download/pr/61747fc6-7236-4d5e-85e5-a5df5f480f3a/02203594bf1331f0875aa6491419ffa1/windowsdesktop-runtime-6.0.8-win-x86.exe",
	"http://download.visualstudio.microsoft.com/download/pr/b4a17a47-2fe8-498d-b817-30ad2e23f413/00020402af25ba40990c6cc3db5cb270/windowsdesktop-runtime-6.0.8-win-x64.exe",
	"http://download.visualstudio.microsoft.com/download/pr/17737b16-dbb0-45f8-9684-16cce46f0835/14475e8380422840249513d58c70d8da/windowsdesktop-runtime-6.0.8-win-arm64.exe",
	"http://download.microsoft.com/download/8/2/7/827bb1ef-f5e1-4464-9788-40ef682930fd/dotnetfx.exe",
	"http://download.microsoft.com/download/0/8/c/08c19fa4-4c4f-4ffb-9d6c-150906578c9e/NetFx20SP1_x86.exe",
	"http://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/net/%e5%be%ae%e8%bd%af.NET%e7%a6%bb%e7%ba%bf%e8%bf%90%e8%a1%8c%e5%ba%93%e5%90%88%e9%9b%86%202022.07.22@%e4%b8%80%e4%b8%aa%e8%b7%af%e4%ba%ba.exe",
	"http://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/net/Dotnet3.5.exe"
};

int vcppMax = 0; 
int netMax = 0;
string *mainlistM[] = {vcppName, netName};
int *mainlistMaxM[] = {&vcppMax, &netMax};
string *vcppAdviceInstallI386[] = {&vcppUrl[0], &vcppUrl[1], &vcppUrl[3], &vcppUrl[5], &vcppUrl[7], &vcppUrl[9], &vcppUrl[12]};
string *vcppAdviceInstallAmd64[] = {&vcppUrl[0], &vcppUrl[2], &vcppUrl[4], &vcppUrl[6], &vcppUrl[8], &vcppUrl[10], &vcppUrl[12]};
string *netAdviceInstallWin7[] = {&netUrl[25]};
string *mainlistUrlM[] = {vcppUrl, netUrl};
string tempPath = "C:\\Windows\\Temp";

bool GetSystemArch(){
	string windowsPath = getenv("SYSTEMROOT");
	if(filesystem::exists(windowsPath + "\\SysWOW64")){
		return true;
	}
	return false;
}

int Download(string url, string savePath, string filename){
	if(filesystem::exists(savePath + "\\" + filename)){
		cout << "文件" << savePath << "\\" << filename << "已存在，移除" << endl;
		filesystem::remove_all(savePath + "\\" + filename);
	}
	cout << "下载链接：" << url << endl;
	string command = "aria2c -x 16 -s 16 \"" + url + "\" -d \"" + savePath + "\" -o \"" + filename + "\""; 
	return system(command.c_str());
}

void InstallAdviceVcpp(){
	if(GetSystemArch()){
		int listLen = sizeof(vcppAdviceInstallAmd64) / sizeof(vcppAdviceInstallAmd64[0]);
		for(int i=0;i<=listLen;i++){
			Download(*vcppAdviceInstallAmd64[i], tempPath, to_string(i) + ".exe");
		}
		for(int i=0;i<=listLen;i++){
			string command = "\"" + tempPath + "\\" + to_string(i) + "\"";
			system(command.c_str());
		}
		return;
	}
	int listLen = sizeof(vcppAdviceInstallI386) / sizeof(vcppAdviceInstallI386[0]);
	for(int i=0;i<=listLen;i++){
		Download(*vcppAdviceInstallI386[i], tempPath, to_string(i) + ".exe");
	}
	for(int i=0;i<=listLen;i++){
		string command = "\"" + tempPath + "\\" + to_string(i) + "\"";
		system(command.c_str());
	}
}

void InstallAdviceNet(){
	int listLen = sizeof(netAdviceInstallWin7) / sizeof(netAdviceInstallWin7[0]);
	for(int i=0;i<=listLen;i++){
		Download(*netAdviceInstallWin7[i], tempPath, to_string(i) + ".exe");
	}
	for(int i=0;i<=listLen;i++){
		string command = "\"" + tempPath + "\\" + to_string(i) + "\"";
		system(command.c_str());
	}	
}

void ShowNextList(string title, int id){
	string *list = mainlistM[id];
	while(1){
		system("cls");
		cout << "项目：https://gitee.com/gfdgd-xi-org/deep-wine-runner" << endl;
		cout << "By RacoonGX Team" << endl;
		cout << "------------------------------------------------------" << endl;
		cout << "安装" << title << endl;
		int max = *mainlistMaxM[id];
		for(int i=0;i<=max - 1;i++){
			cout << i << ". " << *(list + i) << endl;
		}
		cout << max << ". 安装推荐组件" << endl;
		cout << max + 1 << ". 退出此级" << endl;
		int choose = 0;
		cin >> choose;
		if(choose == max){
			cout << "下载文件" << endl;
			if(!id){
				InstallAdviceVcpp();
			}
			else if(id == 1){
				InstallAdviceNet();
			}
			continue;
		}
		if(choose == max + 1){
			break;
		}
		if(0 <= choose && choose < max){
			cout << "下载安装程序" << endl;
			Download(*(mainlistUrlM[id] + choose), tempPath, "vcpp.exe");
			cout << "运行安装程序" << endl;
			system((tempPath + "\\vcpp.exe").c_str());
			system("pause");
			continue;
		}
		cout << "超出范围，请重新输入" << endl;
		system("pause");
	}
}

/*void GetInternetList(){
	Download("", tempPath, "list.txt");
	ifstream file(tempPath + "\\list.txt");
	if(file){
		string line;
		vector<string> netUrlList;
		while(getline(file, line)){
			netUrlList.push_back(line);
		}		
		// 加入数组
		string neturlStringlist[netUrlList.size()];
		for(int i=0;i<=(int)netUrlList.size();i++){
			neturlStringlist[i] = netUrlList[i];
		}
	}
	file.close();
	Download("", tempPath, "list.txt");
	ifstream netnamefile(tempPath + "\\list.txt");
	if(file){
		string line;
		vector<string> netUrlList;
		while(getline(netnamefile, line)){
			netUrlList.push_back(line);
		}
		file.close();
		// 加入数组
		string neturlStringlist[netUrlList.size()];
		for(int i=0;i<=(int)netUrlList.size();i++){
			neturlStringlist[i] = netUrlList[i];
		}
	}	
}*/

int main(){
	// 获取临时文件路径
	tempPath = getenv("TMP");
	tempPath += "\\wine-runner";
	cout << "程序临时目录：" << tempPath << endl;
	if(!filesystem::exists(tempPath)){
		cout << "临时目录不存在，创建。" << endl;
		filesystem::create_directories(tempPath);
	}
	// 从互联网获取数据
	//GetInternetList();
	// 设置窗口标题和主题
	system("title 安装常用组件");
	//system("color 2F");  // 设置主题颜色
	system("cls");
	// 获取数组长度（动态）
	vcppMax = sizeof(vcppName) / sizeof(vcppName[0]);
	netMax = sizeof(netName) / sizeof(netName[0]);
	// 主要逻辑
	while(1){
		cout << "项目：https://gitee.com/gfdgd-xi-org/deep-wine-runner" << endl;
		cout << "By RacoonGX Team" << endl;
		cout << "------------------------------------------------------" << endl;
		int number = 0;
		int mainlistLen = sizeof(mainlist) / sizeof(mainlist[0]);
		for(string i: mainlist){
			cout << number << ". " << i << endl;
			number++;
		}
		cout << mainlistLen << ". 设置系统 OEM 信息（需要先安装 .net framework 4.0 或以上版本）" << endl;
		cout << mainlistLen + 1 << ". 设置默认 OEM 信息（预设）" << endl;
		cout << mainlistLen + 2 << ". 退出程序" << endl;
		cout << "请输入选项编号：";
		int choose = 0;
		cin >> choose;
		if(choose == mainlistLen){
			system("Depends\\OEM.exe");
			system("cls");
			continue;
		}
		if(choose == mainlistLen + 1){
			bool runInAdmin = IsUserAnAdmin();
			if(runInAdmin){
				system("regedit /s Depends/OEM.reg");
				Download("http://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/OEM.bmp", getenv("SYSTEMROOT"), "OEM.bmp");
				cout << "完成！" << endl;
				system("pause");
				system("cls");
				continue;
			}
			cout << "使用该功能需要使用管理员权限运行该程序。" << endl;
			system("pause");
			system("cls");
			continue;
		}
		if(choose == mainlistLen + 2){
			// 退出程序逻辑
			break;
		}
		if(choose >= 0 && choose < mainlistLen){
			ShowNextList(mainlist[choose], choose);
			system("cls");
			continue;
		}
		cout << "数值超出范围，请重新输入" << endl;
		system("pause");
		system("cls");
	}
	return 0;
}
