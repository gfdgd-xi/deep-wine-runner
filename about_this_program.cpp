#include "about_this_program.h"
#include "ui_about_this_program.h"

#include <QDateTime>

about_this_program::about_this_program(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::about_this_program)
{
    ui->setupUi(this);
    QString tips = tr("<h4>提示：</h4>\n"\
                      "1、使用终端运行该程序，可以看到 wine 以及程序本身的提示和报错；\n"\
                      "2、wine 32 位和 64 位的容器互不兼容；\n"\
                      "3、所有的 wine 和 winetricks 均需要自行安装（可以从 菜单栏=>程序 里面进行安装）；\n"\
                      "4、本程序支持带参数运行 wine 程序（之前版本也可以），只需要按以下格式即可：\n"\
                      "exe路径\' 参数 \'\n"\
                      "即可（单引号需要输入）；\n"\
                      "5、wine 容器如果没有指定，则会默认为 ~/.wine；\n"\
                      "6、如果可执行文件比较大的话，会出现点击“获取该程序运行情况”出现假死的情况，因为正在后台读取 SHA1，只需要等一下即可（读取速度依照您电脑处理速度、读写速度、可执行文件大小等有关）；\n"\
                      "7、如果非 X86 的用户的 UOS 专业版用户想要使用的话，只需要在应用商店安装一个 Wine 版本微信即可在本程序选择正确的 Wine 运行程序；");
    QString aboutProgram = tr("<p>Wine运行器是一个能让Linux用户更加方便地运行Windows应用的程序。原版的 Wine 只能使用命令操作，且安装过程较为繁琐，对小白不友好。于是该运行器为了解决该痛点，内置了对Wine图形化的支持、Wine 安装器、微型应用商店、各种Wine工具、自制的Wine程序打包器、运行库安装工具等。</p>\n"\
                              "<p>它同时还内置了基于Qemu/VirtualBox制作的、专供小白使用的Windows虚拟机安装工具，可以做到只需下载系统镜像并点击安装即可，无需考虑虚拟机的安装、创建、分区等操作，也能在非 X86 架构安装 X86 架构的 Windows 操作系统（但是效率较低，可以运行些老系统）。</p>\n"\
                              "<p>而且对于部分 Wine 应用适配者来说，提供了图形化的打包工具，以及提供了一些常用工具以及运行库的安装方式，以及能安装多种不同的 Wine 以测试效果，能极大提升适配效率。</p>\n"\
                              "<p>且对于 Deepin23 用户做了特别优化，以便能在缺少 i386 运行库的情况下运行 Wine32。同时也为非 X86 架构用户提供了 Box86/64、Qemu User 的安装方式</p>\n"\
                              "<pre>");
    QString goodRunSystem = tr("常见 Linux 发行版");
    QString updateThingsString = "";
    QString updateTime = "2023年12月24日";
    QString thankText = "";
    QString version = "";
    QString programUrl = "https://gitee.com/gfdgd-xi/deep-wine-runner\nhttps://github.com/gfdgd-xi/deep-wine-runner\nhttps://gfdgd-xi.github.io";
    QString about = "<style>\n"\
            "a:link, a:active {{\n"\
            "    text-decoration: none;\n"\
            "}}\n"\
            "</style>\n"\
            "<h1>关于</h1>\n"\
            "" + aboutProgram + "\n"\
            "\n"\
            "版本：" + version + "\n"\
            "适用平台：" + goodRunSystem + "\n"\
            "安装包构建时间：" + __DATE__ + " " + __TIME__ + "\n"\
            "Qt 版本：" + qVersion() + "\n"\
            "程序官网：" + programUrl + "\n"\
            "<b>Wine 运行器 QQ 交流群：762985460</b>\n"\
            "<b>Wine运行器 QQ 频道：https://pd.qq.com/s/edqkgeydx</b>\n"\
            "当前程序占用体积：@programSize@MB</pre>\n"\
            "<p>本程序依照 GPLV3 协议开源</p>\n"\
            "<hr>\n"\
            "<h1>鸣谢名单</h1>\n"\
            "<pre>" + thankText + "</pre>\n"\
            "<hr>\n"\
            "<h1>更新内容</h1>\n"\
            "<pre>" + updateThingsString + "\n"\
            "<b>更新时间：" + updateTime + "</b></pre>\n"\
            "<hr>\n"\
            "<h1>提示</h1>\n"\
            "<pre>" + tips + "\n"\
            "</pre>\n"\
            "<hr>\n"\
            "<h1>友谊链接</h1>\n"\
            "<pre>星火应用商店：<a href='https://spark-app.store/'>https://spark-app.store/</a>\n"\
            "Deepin 官网：<a href='https://www.deepin.org'>https://www.deepin.org</a>\n"\
            "Deepin 论坛：<a href='https://bbs.deepin.org'>https://bbs.deepin.org</a>\n"\
            "gfdgd xi：<a href='https://gfdgd-xi.github.io'>https://gfdgd-xi.github.io</a>\n"\
            "<hr>\n"\
            "<h1>©2020~" + QDateTime(QDateTime::currentDateTime()).toString("yyyy") + " By gfdgd xi</h1>";
}

about_this_program::~about_this_program()
{
    delete ui;
}

void about_this_program::on_ok_clicked()
{
    this->close();
}

