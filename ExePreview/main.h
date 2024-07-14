#define DFMFilePreviewFactoryInterface_ood "com.deepin.filemanager.DFMFilePreviewFactoryInterface_WineRunner"

#ifndef MAIN_H
#define MAIN_H

#include <QGenericPlugin>
#include <dfmfilepreviewplugin.h>

class GenericPlugin : public DFM_NAMESPACE::DFMFilePreviewPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QGenericPluginFactoryInterface_iid FILE "ExePreview.json")

public:
    explicit GenericPlugin(QObject *parent = nullptr);
    virtual DFM_NAMESPACE::DFMFilePreview *create(const QString &key);



};

#endif // MAIN_H
