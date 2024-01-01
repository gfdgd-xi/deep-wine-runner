#include "mainwindow.h"
#include <QGridLayout>
#include <QLabel>
#include <QComboBox>
#include <QPushButton>
#include <QMainWindow>
#include <QObject>
#include <QSizePolicy>
#include <QSpacerItem>
#include <QTextBrowser>

MainWindow::MainWindow(){
    QMainWindow *window = new QMainWindow();
    QWidget *widget = new QWidget();
    window->setCentralWidget(widget);
    QGridLayout *mainLayout = new QGridLayout();
    QSizePolicy size;
    //size->setVerticalPolicy(0);
    QWidget *leftUp = new QWidget();
    mainLayout->addWidget(leftUp, 0, 0, 1, 1);
    QGridLayout *leftUpLayout = new QGridLayout();
    leftUp->setLayout(leftUpLayout);
    QLabel *fastLabel = new QLabel(QObject::tr("快速启动"));
    fastLabel->setStyleSheet("font: 30px;");
    leftUpLayout->addWidget(fastLabel, 0, 0, 1, 2);
    leftUpLayout->addWidget(new QLabel("<hr>"), 1, 0, 1, 2);
    leftUpLayout->addWidget(new QLabel(QObject::tr("请选择容器路径：")), 2, 0, 1, 1);
    QComboBox *e1 = new QComboBox();
    e1->setEditable(1);
    leftUpLayout->addWidget(e1, 3, 0, 1, 1);
    QPushButton *button1 = new QPushButton("浏览");
    //button1.clicked.connect(liulanbutton);
    leftUpLayout->addWidget(button1, 3, 1, 1, 1);
    leftUpLayout->addWidget(new QLabel(QObject::tr("请选择要执行的程序（EXE、MSI或者命令）：")), 4, 0, 1, 1);
    QComboBox *e2 = new QComboBox();
    e2->setEditable(1);
    leftUpLayout->addWidget(e2, 5, 0, 1, 1);
    QPushButton *button2 = new QPushButton(QObject::tr("浏览"));
    //button2.clicked.connect(liulanexebutton);
    leftUpLayout->addWidget(button2, 5, 1, 1, 1);
    leftUpLayout->addWidget(new QLabel(QObject::tr("请选择WINE版本：")), 6, 0, 1, 1);
    QComboBox *o1 = new QComboBox();
    leftUpLayout->addWidget(o1, 7, 0, 1, 1);
    // 设置空间权重
    button1->setSizePolicy(size);
    button2->setSizePolicy(size);

    // UI 创建
    QWidget *leftDown = new QWidget();
    mainLayout->addWidget(leftDown, 1, 0, 1, 1);
    QVBoxLayout *leftDownLayout = new QVBoxLayout();
    leftDown->setLayout(leftDownLayout);
    QLabel *highLabel = new QLabel(QObject::tr("高级功能"));
    highLabel->setStyleSheet("font: 30px;");
    leftDownLayout->addWidget(highLabel);
    leftDownLayout->addWidget(new QLabel("<hr>"));
    leftDownLayout->addWidget(new QLabel(QObject::tr("创建快捷方式（Desktop文件）：")));
    QHBoxLayout *createDesktopLink = new QHBoxLayout();
    QLabel *label_r_2 = new QLabel(QObject::tr("名称："));
    createDesktopLink->addWidget(label_r_2);
    QComboBox *combobox1 = new QComboBox();
    combobox1->setEditable(1);
    createDesktopLink->addWidget(combobox1);
    QPushButton *button5 = new QPushButton(QObject::tr("创建到桌面"));
    //button5.clicked.connect(make_desktop_on_desktop);
    createDesktopLink->addWidget(button5);
    QPushButton *saveDesktopFileOnLauncher =  new QPushButton(QObject::tr("创建到开始菜单"));
    //saveDesktopFileOnLauncher.clicked.connect(make_desktop_on_launcher);
    createDesktopLink->addWidget(saveDesktopFileOnLauncher);
    leftDownLayout->addLayout(createDesktopLink);
    QGridLayout *programManager = new QGridLayout();
    leftDownLayout->addLayout(programManager);
    programManager->addWidget(new QLabel(QObject::tr("程序管理：")), 0, 0, 1, 1);
    QPushButton *getProgramIcon = new QPushButton(QObject::tr("提取图标"));
    //getProgramIcon.clicked.connect(lambda: RunWineProgram(f"{programPath}/BeCyIconGrabber.exe' '{e2.currentText()}" if e2.currentText()[:2].upper() == "C:" else f"{programPath}/BeCyIconGrabber.exe' 'z:/{e2.currentText()}"));
    programManager->addWidget(getProgramIcon, 1, 0, 1, 1);
    programManager->addWidget(new QLabel("     "), 1, 1, 1, 1);
    QPushButton *trasButton = new QPushButton(QObject::tr("窗口透明工具"));
    //trasButton.clicked.connect(lambda: RunWineProgram(f"{programPath}/窗体透明度设置工具.exe"));
    programManager->addWidget(trasButton, 1, 2, 1, 1);
    QPushButton *uninstallProgram = new QPushButton(QObject::tr("卸载程序"));
    //uninstallProgram.clicked.connect(lambda: RunWineProgram(f"{programPath}/geek.exe"));
    programManager->addWidget(new QLabel("     "), 1, 3, 1, 1);
    programManager->addWidget(uninstallProgram, 1, 4, 1, 1);
    QPushButton *miniAppStore = new QPushButton(QObject::tr("微型应用商店"));
    //miniAppStore.clicked.connect(lambda: threading.Thread(target=MiniAppStore).start());
    programManager->addWidget(new QLabel("     "), 1, 5, 1, 1);
    programManager->addWidget(miniAppStore, 1, 6, 1, 1);
    programManager->addWidget(new QLabel("     "), 1, 7, 1, 1);
    QPushButton *getProgramStatus = new QPushButton(QObject::tr("获取该程序运行情况"));
    //getProgramStatus.clicked.connect(ProgramRunStatusShow.ShowWindow);
    programManager->addWidget(getProgramStatus, 1, 8, 1, 1);
    QPushButton *getLoseDll = new QPushButton(QObject::tr("检测静态下程序缺少DLL"));
    //getLoseDll.clicked.connect(GetLoseDll);
    programManager->addWidget(new QLabel("     "), 1, 9, 1, 1);
    programManager->addWidget(getLoseDll, 1, 10, 1, 1);
    programManager->addItem(new QSpacerItem(20, 20, QSizePolicy::Expanding, QSizePolicy::Minimum), 1, 11, 1, 1);
    programManager->addWidget(new QLabel(QObject::tr("WINE配置：")), 2, 0, 1, 1);
    QPushButton *wineConfig = new QPushButton(QObject::tr("配置容器"));
    //wineConfig.clicked.connect(lambda: RunWineProgram("winecfg"));
    programManager->addWidget(wineConfig, 3, 0, 1, 1);
    QPushButton *fontAppStore = new QPushButton(QObject::tr("字体商店"));
    //fontAppStore.clicked.connect(FontAppStore);
    programManager->addWidget(fontAppStore, 3, 2, 1, 1);
    QPushButton *button_r_6 = new QPushButton(QObject::tr("RegShot"));
    //button_r_6.clicked.connect(lambda: RunWineProgram(f"{programPath}/RegShot/regshot.exe"));
    programManager->addWidget(button_r_6, 3, 4, 1, 1);
    QPushButton *sparkWineSetting = new QPushButton(QObject::tr("星火wine配置"));
    //sparkWineSetting.clicked.connect(lambda: threading.Thread(target=os.system, args=["bash /opt/durapps/spark-dwine-helper/spark-dwine-helper-settings/settings.sh"]).start());
    programManager->addWidget(sparkWineSetting, 3, 6, 1, 1);
    QPushButton *wineAutoConfig =  new QPushButton(QObject::tr("自动/手动配置 Wine 容器"));
    //wineAutoConfig.clicked.connect(WineBottonAutoConfig);
    programManager->addWidget(wineAutoConfig, 3, 8, 1, 1);
    QPushButton *wineBottleReboot = new QPushButton(QObject::tr("重启指定Wine容器"));
    //wineBottleReboot.clicked.connect(lambda: RunWineProgram(f"wineboot' '-k"));
    programManager->addWidget(wineBottleReboot, 3, 10, 1, 1);

    // 权重
    button5->setSizePolicy(size);
    saveDesktopFileOnLauncher->setSizePolicy(size);
    label_r_2->setSizePolicy(size);
    getProgramIcon->setSizePolicy(size);
    //trasButton.setSizePolicy(size);
    button_r_6->setSizePolicy(size);
    wineConfig->setSizePolicy(size);

    QTextBrowser *returnText = new QTextBrowser();
    returnText->setStyleSheet("background-color: black;"\
    "color: white;");
    returnText->setText(QObject::tr("在此可以看到wine安装应用时的终端输出内容\n"\
    "=============================================\n"\
    "如果解决了你的问题，请不要吝啬你的star哟！\n"\
    "地址：\n"\
    "https://gitee.com/gfdgd-xi/deep-wine-runner\n"\
    "https://github.com/gfdgd-xi/deep-wine-runner\n"\
    "https://sourceforge.net/projects/deep-wine-runner"));
    mainLayout->setRowStretch(0, 2);
    mainLayout->setRowStretch(1, 1);
    mainLayout->setColumnStretch(0, 2);
    mainLayout->setColumnStretch(1, 1);
    mainLayout->addWidget(returnText, 0, 1, 2, 1);

    // 版权
    QLabel *copy = new QLabel("程序版本：{version}，<b>提示：Wine 无法保证可以运行所有的 Windows 程序，如果想要运行更多 Windows 程序，可以考虑虚拟机和双系统</b><br/>"\
    "<b>注：部分二进制兼容层会自动注册 binfmt（如原版的 Box86/64、Qemu User Static），则意味着无需在 Wine 版本那里特别指定兼容层，直接指定 Wine 即可</b><br/>"\
    "©2020~{time.strftime('%Y')} gfdgd xi");
    mainLayout->addWidget(copy, 2, 0, 1, 1);

    // 程序运行
    QWidget *programRun = new QWidget();
    QHBoxLayout *programRunLayout = new QHBoxLayout();
    programRun->setLayout(programRunLayout);
    programRunLayout->addItem(new QSpacerItem(20, 20, QSizePolicy::Expanding, QSizePolicy::Minimum));
    QPushButton *button3 = new QPushButton(QObject::tr("运行程序"));
    //button3.clicked.connect(runexebutton);
    programRunLayout->addWidget(button3);
    QPushButton *killProgram = new QPushButton(QObject::tr("终止程序"));
    //killProgram.clicked.connect(KillProgram);
    programRunLayout->addWidget(killProgram);
    QPushButton *killBottonProgram = new QPushButton(QObject::tr("终止指定容器的程序"));
    //killBottonProgram.clicked.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/kill.sh' '{os.path.basename(e1.currentText())}'"]).start());
    programRunLayout->addWidget(killBottonProgram);
    mainLayout->addWidget(programRun, 2, 1, 1, 1);

    // 窗口设置
    window->resize(widget->frameGeometry().width() * 2, widget->frameGeometry().height());
    //window->setWindowIcon(QIcon("{programPath}/deepin-wine-runner.svg"));
    widget->setLayout(mainLayout);
    window->show();

    // 一个 Wine 都没有却用 Wine 的功能
    // 还是要处理的，至少不会闪退
    if(o1->currentText() == ""){
        o1->addItem("没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用");
    }
}

MainWindow::~MainWindow()
{
    //delete ui;
}

