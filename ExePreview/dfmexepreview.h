#ifndef DFMEXEPREVIEW_H
#define DFMEXEPREVIEW_H

#include <QObject>
#include <dfmfilepreview.h>
#include <QLabel>

class DFMExePreview : public DFM_NAMESPACE::DFMFilePreview
{
    Q_OBJECT
public:
    explicit DFMExePreview(QObject *parent = NULL);
    ~DFMExePreview();
    virtual void initialize(QWidget *window, QWidget *statusBar) Q_DECL_OVERRIDE;
    virtual bool setFileUrl(const DUrl &url) Q_DECL_OVERRIDE;
    virtual DUrl fileUrl() const Q_DECL_OVERRIDE;
    virtual QWidget *contentWidget() const Q_DECL_OVERRIDE;
    virtual QWidget *statusBarWidget() const Q_DECL_OVERRIDE;
    virtual QString title() const Q_DECL_OVERRIDE;

protected:
    DUrl m_url;
    QLabel *m_view = NULL;
    QLabel *m_statusBar = NULL;
    QString m_title;
};

#endif // DFMEXEPREVIEW_H
