#include "main.h"
#include "dfmexepreview.h"

GenericPlugin::GenericPlugin(QObject *parent)
    : DFM_NAMESPACE::DFMFilePreviewPlugin(parent)
{
}

/*QObject *GenericPlugin::create(const QString &name, const QString &spec)
{

}*/
DFM_NAMESPACE::DFMFilePreview *GenericPlugin::create(const QString &key)
{
    Q_UNUSED(key);
    return new DFMExePreview;
}
