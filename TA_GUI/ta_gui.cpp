#include "ta_gui.h"
#include "ui_ta_gui.h"

TA_GUI::TA_GUI(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::TA_GUI)
{
    ui->setupUi(this);
}

TA_GUI::~TA_GUI()
{
    delete ui;
}
