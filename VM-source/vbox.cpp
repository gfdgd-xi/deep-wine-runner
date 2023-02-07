#include "vbox.h"
#include "command.h"

vbox::vbox(QString name, QString managerPath) {
    this->name = name;
    this->managerPath = managerPath;
    Command command = Command();
    this->vboxVersion = Command().GetCommand("'" + managerPath + "' -v");
}
