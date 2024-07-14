#include "dfmexepreview.h"

#include <dfileservices.h>

DFMExePreview::DFMExePreview(QObject *parent) : DFMFilePreview(parent)
{

}

DFMExePreview::~DFMExePreview()
{
    if (m_view) {
        m_view->deleteLater();
        m_view = NULL;
    }
    if (m_statusBar) {
        m_statusBar->deleteLater();
        m_statusBar = NULL;
    }
}

void DFMExePreview::initialize(QWidget *window, QWidget *statusBar)
{
    Q_UNUSED(window)
    Q_UNUSED(statusBar)
    if (!m_view) {
        m_view = new QLabel();
    }
    if (!m_statusBar) {
        m_statusBar = new QLabel();
    }
}

bool DFMExePreview::setFileUrl(const DUrl &url)
{
    m_url = url;
    m_view->setText("114514");
    return 1;
}

DUrl DFMExePreview::fileUrl() const
{
    return m_url;
}

QWidget *DFMExePreview::contentWidget() const
{
    return m_view;
}

QWidget *DFMExePreview::statusBarWidget() const
{
    return m_statusBar;
}

QString DFMExePreview::title() const
{
    return m_title;
}
