#include <QSqlDatabase>
#include <QSqlError>
#include <qDebug>



bool create_connection() {

    QSqlDatabase db = QSqlDatabase::addDatabase("QPSQL");


    db.setDatabaseName("taxi_db");

    db.setUserName("myuser");
    db.setHostName("mydatabase");
    db.setPassword("mypassword");

    if (!db.open()) {

        qDebug() << "Не удалось открыть базу данных!" << db.lastError();

        return false;

    }



 
    return true;
}