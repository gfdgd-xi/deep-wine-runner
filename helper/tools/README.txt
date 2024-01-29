#autostart

#autostart在系统启动时自启动，根据配置“autostart”文件策略预启动容器，不需要用户手动启动

1.默认不会预启动任何容器

2.如果需要启动所有已运行过的容器，请将文件"autostart" 改名 "autostart.all" 示例如下：
sudo mv /opt/deepinwine/tools/autostart /opt/deepinwine/tools/autostart.all

3.如果需要启动用户自己关注的应用，那么将容器名称按行写入"autostart"，格式如下：
com.qq.weixin.work.deepin
com.qq.im.deepin
com.meituxiuxiu.deepin

4.兼容原来的kill.sh逻辑
