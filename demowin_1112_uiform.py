import sys
from PyQt5 import uic
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3
import data_select
import tx_duibiao
import qf_duibiao
import yh_duibiao
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
mpl.use('Qt5Agg')
mpl.rcParams['font.family'] = 'FangSong'
mpl.rcParams['font.size'] = 20
mpl.rcParams['axes.unicode_minus']=False
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Ui_demowin_1112 import Ui_Form

class win(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        # self.ui = uic.loadUi(r'.\2\ui\demowin_1112.ui')
        self.setupUi(self)
        self.init_ui()
        QSettings('myapp.ini',QSettings.Format.IniFormat)

    def init_ui(self):
        self.tx_cae_list_dict = {}
        self.tx_cae_data_dict = {}
        self.qf_cae_list_dict = {}
        self.qf_cae_data_dict = {}
        self.yh_cae_list_dict = {}
        self.yh_cae_data_dict = {}
        self.test_list_dict = {}
        self.test_data_dict = {}
        self.gv_1 = self.graphicsView
        self.gv_2 = self.graphicsView_2
        self.gv_3 = self.graphicsView_3
        self.sql_list = self.listWidget
        self.sql_view = self.tableWidget
        self.sql_bn = self.pushButton_9

        self.tab_widget = self.tabWidget
        self.test_bn = self.pushButton
        self.test_plot_bn = self.pushButton_6
        self.test_clear_bn = self.pushButton_7
        self.test_ok_bn = self.pushButton_8
        self.test_list = self.listWidget_2
        self.material_edit = self.lineEdit
        self.temperature_edit = self.lineEdit_2
        self.select_browser = self.textBrowser

        self.test_cbb = self.comboBox
        self.tx_cae_bn = self.pushButton_2
        self.tx_cae_list = self.listWidget_3
        self.tx_plot_bn = self.pushButton_3
        self.tx_clear_bn = self.pushButton_4
        self.tx_cae_bn.clicked.connect(self.tx_import_cae)
        self.tx_plot_bn.clicked.connect(self.tx_plot_fig)
        self.tx_clear_bn.clicked.connect(self.clear_tx_cae_list)

        self.test_cbb_2 = self.comboBox_2
        self.qf_cae_bn = self.pushButton_5
        self.qf_cae_list = self.listWidget_4
        self.qf_plot_bn = self.pushButton_10
        self.qf_clear_bn = self.pushButton_11
        self.qf_cae_bn.clicked.connect(self.qf_import_cae)
        self.qf_plot_bn.clicked.connect(self.qf_plot_fig)
        self.qf_clear_bn.clicked.connect(self.clear_qf_cae_list)

        self.test_cbb_3 = self.comboBox_3
        self.yh_cae_bn = self.pushButton_12
        self.yh_cae_list = self.listWidget_5
        self.yh_plot_bn = self.pushButton_13
        self.yh_clear_bn = self.pushButton_14
        self.yh_cae_bn.clicked.connect(self.yh_import_cae)
        self.yh_plot_bn.clicked.connect(self.yh_plot_fig)
        self.yh_clear_bn.clicked.connect(self.clear_yh_cae_list)

        self.tab_widget.tabBarClicked.connect(self.import_db)
        self.test_bn.clicked.connect(self.import_test)
        self.test_ok_bn.clicked.connect(self.test_to_db)
        self.test_clear_bn.clicked.connect(self.clear_test_list)
        self.test_plot_bn.clicked.connect(self.plot_test_fig)
        
        self.sql_bn.clicked.connect(self.show_sql)
        
    def no_figure(self):
        figure = plt.figure(figsize=(3, 2.5), dpi=100)
        current_axes = plt.axes()
        current_axes.get_xaxis().set_visible(False)
        current_axes.get_yaxis().set_visible(False)
        canvas = FigureCanvas(figure)
        plt.text(0.1,0.4,'No Figure',dict(size=30))
        canvas.draw()
        return canvas

    def import_test(self):
        while True:
            self.open_file_name = QFileDialog.getOpenFileName(self,'选择实验数据文件','','Mdb 文件(*.MDB)')
            self.open_test_path = self.open_file_name[0]
            if self.open_test_path == '':
                msg_box = QMessageBox.critical(self,"提示信息","未选择实验数据文件！",QMessageBox.Abort|QMessageBox.Retry,QMessageBox.Abort)
                if msg_box == QMessageBox.Abort:
                    break
                else:
                    continue
            elif self.open_test_path.split('.')[-1] == 'MDB':
                self.data_dict = data_select.import_data(self.open_test_path)
                self.data_name = list(self.data_dict.keys())
                self.test_list.clear()
                self.test_list.addItems(self.data_name)
                self.select_browser.clear()
                self.select_browser.setText("请选择并筛选实验数据")
                break

    def tx_import_cae(self):
        while True:
            self.open_file_names = QFileDialog.getOpenFileNames(self,'选择仿真数据文件','','文本文件(*.csv)')
            self.open_cae_paths = self.open_file_names[0]
            if self.open_cae_paths == []:
                msg_box = QMessageBox.critical(self,"提示信息","未选择实验数据文件！",QMessageBox.Abort|QMessageBox.Retry,QMessageBox.Abort)
                if msg_box == QMessageBox.Abort:
                    break
                else:
                    continue
            else:
                for open_cae_path in self.open_cae_paths:
                    self.tx_cae_name = open_cae_path.split('/')[-1].split('.')[0]
                    self.tx_cae_list_dict.update({self.tx_cae_name:open_cae_path})
                    self.tx_cae_list.clear()
                    self.tx_cae_list.addItems(self.tx_cae_list_dict.keys())
                break

    def import_db(self,index):
        if index == 1:
            conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
            self.table = pd.read_sql("SELECT * FROM sqlite_master WHERE type='table'",conn)
            self.test_cbb.clear()
            self.test_cbb.addItems(self.table['name'])
            canvas = self.no_figure()
            graphicscene = QtWidgets.QGraphicsScene()
            graphicscene.addWidget(canvas)
            self.gv_1.setScene(graphicscene)
            self.gv_1.show()
            self.gv_2.setScene(graphicscene)
            self.gv_2.show()
            self.gv_3.setScene(graphicscene)
            self.gv_3.show()
            plt.close('all')
        elif index == 2:
            conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
            self.table = pd.read_sql("SELECT * FROM sqlite_master WHERE type='table'",conn)
            self.test_cbb_2.clear()
            self.test_cbb_2.addItems(self.table['name'])
        elif index == 3:
            conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
            self.table = pd.read_sql("SELECT * FROM sqlite_master WHERE type='table'",conn)
            self.test_cbb_3.clear()
            self.test_cbb_3.addItems(self.table['name'])

    def show_sql(self):
        conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
        self.table = pd.read_sql("SELECT * FROM sqlite_master WHERE type='table'",conn)
        self.sql_list.clear()
        self.sql_list.addItems(self.table['name'])
        self.sql_list.itemClicked.connect(self.list_clicked)

    def list_clicked(self,item):
        conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
        self.table = pd.read_sql("SELECT * FROM "+item.text(),conn)
        self.sql_view.setRowCount(len(self.table))
        self.sql_view.setColumnCount(2)
        self.sql_view.setHorizontalHeaderLabels(['实验位移','实验力值'])
        for index,row in self.table.iterrows():
            self.sql_view.setItem(index,0,QTableWidgetItem(str(row['实验位移'])))
            self.sql_view.setItem(index,1,QTableWidgetItem(str(row['实验力值'])))

    def tx_test(self):
        self.cbb_text = self.test_cbb.currentText()
        conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
        self.sql_dataframe = pd.read_sql('SELECT * FROM "'+self.cbb_text+'"',conn)
        self.tx_test_mf = tx_duibiao.data_deal(self.sql_dataframe['实验位移'],self.sql_dataframe['实验力值'])

    def tx_cae(self):
        for i in self.tx_cae_list.selectedItems():
            self.cae_path = self.tx_cae_list_dict[i.text()]
            self.cae_mf = tx_duibiao.csv_deal(self.cae_path)
            self.tx_cae_data_dict.update({i.text():self.cae_mf})

    def clear_test_list(self):
        self.test_list.clear()
        self.test_list_dict = {}

    def clear_tx_cae_list(self):
        self.tx_cae_list.clear()
        self.tx_cae_list_dict = {}
        self.tx_cae_data_dict = {}

    def plot_test_fig(self):
        if self.test_list.selectedItems() == []:
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请在表单中选择数据表！")
            msg_box.exec_()
        else:
            plt_legend = []
            plt.figure(figsize=(10,8),dpi=60)
            for i in self.test_list.selectedItems():
                x = self.data_dict[i.text()][0]
                y = self.data_dict[i.text()][1]
                plt.plot(x,y)
                plt_legend.append(i.text())
            plt.legend(plt_legend)
            plt.show()
            self.select_browser.clear()
            self.select_browser.setText("实验数据对比图绘制成功！")

    def test_to_db(self):
        self.data_info = '材料：' + self.material_edit.text() + ' 温度：' + self.temperature_edit.text() + '℃'
        if self.material_edit.text() == '' or self.temperature_edit.text() == '':
            msg_box = QMessageBox(QMessageBox.Critical,"错误","填写实验信息不完整！")
            msg_box.exec_()
        elif self.test_list.selectedItems() == []:
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请在表单中选择数据表！")
            msg_box.exec_()
        else:
            conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
            a = 0
            for i in self.test_list.selectedItems():
                a = a+1
                x = self.data_dict[i.text()][0]
                y = self.data_dict[i.text()][1]
                dict = {
                    "实验位移":x,
                    "实验力值":y
                }
                df = pd.DataFrame(dict)
                df.to_sql(self.data_info+'_'+str(a),conn,if_exists='replace',index=False)
            conn.close()
            self.select_browser.clear()
            self.select_browser.setText("实验数据保存成功！")

    def tx_plot_fig(self):
        if self.test_cbb.count() == 0:
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请筛选并保存实验数据！")
            msg_box.exec_()
        elif self.tx_cae_list.count() == 0:
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请导入仿真数据文件！")
            msg_box.exec_()
        elif self.tx_cae_list.selectedItems() == [] :
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请选择仿真数据表！")
            msg_box.exec_()
        else:
            self.tx_test()
            self.tx_cae()
            for key,value in self.tx_cae_data_dict.items():
                x1 = self.tx_test_mf[0]
                y1 = self.tx_test_mf[1]
                x2 = value[0]
                y2 = value[1]
                cae_data_y0 = y2[x2.index(0.1)]
                x1 = x1-x1[0]+0.1
                y1 = y1-y1[0]+cae_data_y0
                plt.figure(figsize=(10,8),dpi=60)
                plt.plot(x1,y1,'ro-')
                plt.plot(x2,y2,'bs-')
                plt.xlabel('位移')
                plt.ylabel('力')
                plt.title('弹性阶段对标')
                plt.legend([self.cbb_text,key])
                plt.show()

    def qf_import_cae(self):
        while True:
            self.open_file_names = QFileDialog.getOpenFileNames(self,'选择仿真数据文件','','文本文件(*.csv)')
            self.open_cae_paths = self.open_file_names[0]
            if self.open_cae_paths == []:
                msg_box = QMessageBox.critical(self,"提示信息","未选择实验数据文件！",QMessageBox.Abort|QMessageBox.Retry,QMessageBox.Abort)
                if msg_box == QMessageBox.Abort:
                    break
                else:
                    continue
            else:
                for open_cae_path in self.open_cae_paths:
                    self.qf_cae_name = open_cae_path.split('/')[-1].split('.')[0]
                    self.qf_cae_list_dict.update({self.qf_cae_name:open_cae_path})
                    self.qf_cae_list.clear()
                    self.qf_cae_list.addItems(self.qf_cae_list_dict.keys())
                break

    def clear_qf_cae_list(self):
        self.qf_cae_list.clear()
        self.qf_cae_list_dict = {}
        self.qf_cae_data_dict = {}

    def qf_test(self,cae_mov,cae_force):
        self.cbb_text = self.test_cbb_2.currentText()
        conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
        self.sql_dataframe = pd.read_sql('SELECT * FROM "'+self.cbb_text+'"',conn)
        self.qf_test_mf = qf_duibiao.data_deal(self.sql_dataframe['实验位移'],self.sql_dataframe['实验力值'],cae_mov,cae_force)

    def qf_cae(self):
        for i in self.qf_cae_list.selectedItems():
            self.cae_path = self.qf_cae_list_dict[i.text()]
            self.qf_cae_mf = qf_duibiao.csv_deal(self.cae_path)
            self.qf_cae_data_dict.update({i.text():self.qf_cae_mf})

    def qf_plot_fig(self):
        if self.test_cbb_2.count() == 0:
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请筛选并保存实验数据！")
            msg_box.exec_()
        elif self.qf_cae_list.count() == 0:
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请导入仿真数据文件！")
            msg_box.exec_()
        elif self.qf_cae_list.selectedItems() == [] :
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请选择仿真数据表！")
            msg_box.exec_()
        else:
            self.qf_cae()
            
            for key,value in self.qf_cae_data_dict.items():
                x2 = value[0]
                y2 = value[1]
                self.qf_test(x2,y2)
                x1 = self.qf_test_mf[0]
                y1 = self.qf_test_mf[1]
                plt.figure(figsize=(10,8),dpi=60)
                plt.plot(x1,y1,'ro-')
                plt.plot(x2,y2,'bs-')
                plt.xlabel('位移')
                plt.ylabel('力')
                plt.title('屈服阶段对标')
                plt.legend([self.cbb_text,key])
                plt.show()

    def yh_import_cae(self):
        while True:
            self.open_file_names = QFileDialog.getOpenFileNames(self,'选择仿真数据文件','','文本文件(*.csv)')
            self.open_cae_paths = self.open_file_names[0]
            if self.open_cae_paths == []:
                msg_box = QMessageBox.critical(self,"提示信息","未选择实验数据文件！",QMessageBox.Abort|QMessageBox.Retry,QMessageBox.Abort)
                if msg_box == QMessageBox.Abort:
                    break
                else:
                    continue
            else:
                for open_cae_path in self.open_cae_paths:
                    self.yh_cae_name = open_cae_path.split('/')[-1].split('.')[0]
                    self.yh_cae_list_dict.update({self.yh_cae_name:open_cae_path})
                    self.yh_cae_list.clear()
                    self.yh_cae_list.addItems(self.yh_cae_list_dict.keys())
                break

    def clear_yh_cae_list(self):
        self.yh_cae_list.clear()
        self.yh_cae_list_dict = {}
        self.yh_cae_data_dict = {}

    def yh_test(self,cae_mov,cae_force):
        self.cbb_text = self.test_cbb_3.currentText()
        conn = sqlite3.connect(r'.\test_sqlite.db') #连接高低温物性测量数据库
        self.sql_dataframe = pd.read_sql('SELECT * FROM "'+self.cbb_text+'"',conn)
        self.yh_test_mf = yh_duibiao.data_deal(self.sql_dataframe['实验位移'],self.sql_dataframe['实验力值'],cae_mov,cae_force)

    def yh_cae(self):
        for i in self.yh_cae_list.selectedItems():
            self.cae_path = self.yh_cae_list_dict[i.text()]
            self.yh_cae_mf = qf_duibiao.csv_deal(self.cae_path)
            self.yh_cae_data_dict.update({i.text():self.yh_cae_mf})

    def yh_plot_fig(self):
        if self.test_cbb_3.count() == 0:
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请筛选并保存实验数据！")
            msg_box.exec_()
        elif self.yh_cae_list.count() == 0:
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请导入仿真数据文件！")
            msg_box.exec_()
        elif self.yh_cae_list.selectedItems() == [] :
            msg_box = QMessageBox(QMessageBox.Critical,"错误","请选择仿真数据表！")
            msg_box.exec_()
        else:
            self.yh_cae()
            
            for key,value in self.yh_cae_data_dict.items():
                x2 = value[0]
                y2 = value[1]
                self.yh_test(x2,y2)
                x1 = self.yh_test_mf[0]
                y1 = self.yh_test_mf[1]
                plt.figure(figsize=(10,8),dpi=60)
                plt.plot(x1,y1,'ro-')
                plt.plot(x2,y2,'bs-')
                plt.xlabel('位移')
                plt.ylabel('力')
                plt.title('硬化阶段对标')
                plt.legend([self.cbb_text,key])
                plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = win()
    w.show()
    app.exec()