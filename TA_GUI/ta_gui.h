#ifndef TA_GUI_H
#define TA_GUI_H

#include <QMainWindow>

namespace Ui {
class TA_GUI;
}

class TA_GUI : public QMainWindow
{
    Q_OBJECT

public:
    explicit TA_GUI(QWidget *parent = 0);
    ~TA_GUI();

private:
    Ui::TA_GUI *ui;
};

#endif // TA_GUI_H
