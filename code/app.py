import os
import sys
import random

import readdat
from io import BytesIO
from PIL import Image, ImageDraw
from NCBIinfo_extract import Get_inform_NCBI
from Visualization_and_Save import result_df_to_veiw_pdf

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QMessageBox,  QScrollArea, QTextBrowser




class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        
        self.file_path_label = QLabel("Input File: Not selected", self)
        layout.addWidget(self.file_path_label)

        self.btn_select_file = QPushButton('Select Input File', self)
        self.btn_select_file.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select_file)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Your email (e.g., 1666526339@qq.com)")
        layout.addWidget(self.email_input)

        self.save_path_label = QLabel("Save Directory: Not selected", self)
        layout.addWidget(self.save_path_label)

        self.btn_select_save_path = QPushButton('Select Save Directory', self)
        self.btn_select_save_path.clicked.connect(self.select_save_directory)
        layout.addWidget(self.btn_select_save_path)

        #wkhtmltopdf_layout 
        layout.addWidget(QLabel('wkhtmltopdf Path:'))

        # Input for wkhtmltopdf path
        self.wkhtmltopdf_path_input = QLineEdit(self)
        self.wkhtmltopdf_path_input.setText('C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        layout.addWidget(self.wkhtmltopdf_path_input)

        # Browse button for wkhtmltopdf path
        self.wkhtmltopdf_button = QPushButton('Browse', self)
        self.wkhtmltopdf_button.clicked.connect(self.select_wkhtmltopdf_path)
        layout.addWidget(self.wkhtmltopdf_button)

        # Help button
    
        self.btn_help = QPushButton('Help', self)
        self.btn_help.clicked.connect(self.show_help)
        layout.addWidget(self.btn_help)
        
        
        self.btn_run = QPushButton('Run', self)
        self.btn_run.clicked.connect(self.run_process)
        layout.addWidget(self.btn_run)
        
        
        self.setLayout(layout)
        self.setWindowTitle('NCBI Data Processor')
        self.resize(300, 100)
        self.show()

        self.setLayout(layout)
        self.setWindowTitle('NCBI Data Processor')
        self.resize(400, 100)  # Set default window size
        self.setWindowIcon(QIcon(self.create_random_icon()))
        self.show()

        # Check wkhtmltopdf path on startup
        self.check_wkhtmltopdf_path()

    def check_wkhtmltopdf_path(self):
        path = self.wkhtmltopdf_path_input.text()
        if not os.path.exists(path):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("wkhtmltopdf not found!")
            msg.setInformativeText("Please install wkhtmltox or provide the correct path.")
            msg.setWindowTitle("Warning")
            msg.exec_()


    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_name:
            self.file_path_label.setText(f"Input File: {file_name}")

    def select_save_directory(self):
        save_directory = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        if save_directory:
            self.save_path_label.setText(f"Save Directory: {save_directory}")
    
        
    def run_process(self):
        # Read the inputs
        file_path = self.file_path_label.text().replace("Input File: ", "")
        email = self.email_input.text()
        save_directory = self.save_path_label.text().replace("Save Directory: ", "")
        save_path = os.path.join(save_directory, "result.pdf")

        # Check inputs
        email = self.email_input.text()
        wkhtmltopdf_path = self.wkhtmltopdf_path_input.text()

        if not file_path or not os.path.exists(file_path):
            self.show_warning("Please select a valid input file.")
            return

        if not email:
            self.show_warning("Please enter an email.")
            return

        if not wkhtmltopdf_path or not os.path.exists(wkhtmltopdf_path):
            self.show_warning("Please select a valid wkhtmltopdf path or install wkhtmltox.")
            return



        # Your existing process
        Sample_dat = readdat.read_data(file_path=file_path)
        Sample_dat = Get_inform_NCBI(Sample_dat=Sample_dat, email=email)
        result_df_to_veiw_pdf(Data=Sample_dat, save_path=save_path, wkhtmltopdf_path='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        
        
        # Show a message when done
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Process completed!")
        msg.setWindowTitle("Info")
        msg.exec_()

    def show_warning(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()
    
    def select_wkhtmltopdf_path(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select wkhtmltopdf", "", "All Files (*);;Executable Files (*.exe)", options=options)
        if filePath:
            self.wkhtmltopdf_path_input.setText(filePath)

    def show_help(self):
        help_text = """
        <html>
        <body>
        <p>这是 NCBI 数据处理器应用程序。</p>
    
    <p><strong>操作步骤:</strong></p>
    <ol>
        <li>点击“选择输入文件”按钮选择输入文件。支持的文件格式：xlsx、csv、xls、txt。</li>
    </ol>
    
    <p><strong>示例输入文件:</strong></p>
    <table border="1">
        <tr>
            <th>样本</th>
            <th>IR</th>
        </tr>
        <tr>
            <td>ERX123123</td>
            <td>......1231.......</td>
        </tr>
        <tr>
            <td>ERX123124</td>
            <td>1</td>
        </tr>
        <tr>
            <td>ERX123125</td>
            <td>.......1.......</td>
        </tr>
        <tr>
            <td>GSM12321</td>
            <td>.22..</td>
        </tr>
        <tr>
            <td>GSM12323</td>
            <td>...</td>
        </tr>
    </table>
    
    <ol start="2">
        <li>在电子邮件输入字段中输入您的电子邮件。</li>
        <li>点击“选择保存目录”按钮选择保存目录。</li>
        <li>单击“运行”按钮以处理数据。</li>
    </ol>

    <p>获取更多信息，请参阅用户手册。</p>
    
    <p>技术支持，请联系 support 1666526339xiongxiangyi@gmail.com</p>
    
        <p>This is the NCBI Data Processor application.</p>
        
        <p><strong>Instructions:</strong></p>
        <ol>
            <li>Select an input file by clicking the "Select Input File" button. Supported file formats: xlsx, csv, xls, txt.</li>
        </ol>
        
        <p><strong>Example input file:</strong></p>
        <table border="1">
            <tr>
                <th>Sample</th>
                <th>IR</th>
            </tr>
            <tr>
                <td>ERX123123</td>
                <td>......1231.......</td>
            </tr>
            <tr>
                <td>ERX123124</td>
                <td>1</td>
            </tr>
            <tr>
                <td>ERX123125</td>
                <td>.......1.......</td>
            </tr>
            <tr>
                <td>GSM12321</td>
                <td>.22..</td>
            </tr>
            <tr>
                <td>GSM12323</td>
                <td>...</td>
            </tr>
        </table>
        
        <ol start="2">
            <li>Enter your email in the email input field.</li>
            <li>Select a save directory by clicking the "Select Save Directory" button.</li>
            <li>Click the "Run" button to process the data.</li>
        </ol>

        <p>For more information, please refer to the user manual.</p>
        
        <p>For technical support, contact support 1666526339xiongxiangyi@gmail.com</p>
        
        <p>GitHub Repository: <a href="https://github.com/YourGitHubUsername/NCBI-metadata-SRA-AND-GSM-TO-PDF">NCBI-metadata-SRA-AND-GSM-TO-PDF</a></p>
        </body>
        </html>
        """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setTextFormat(Qt.RichText)  # 设置文本格式为Rich Text
        msg.setText(help_text)
        msg.setWindowTitle("Help")
        msg.exec_()

        

    def create_random_icon(self):
        # 创建一个随机图标
        size = (32, 32)
        icon = Image.new('RGB', size)
        draw = ImageDraw.Draw(icon)
        for _ in range(1000):
            x = random.randint(0, size[0] - 1)
            y = random.randint(0, size[1] - 1)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw.point((x, y), fill=color)
        icon_bytes = BytesIO()
        icon.save(icon_bytes, format='PNG')
        icon_bytes.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(icon_bytes.read())
        return pixmap


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


