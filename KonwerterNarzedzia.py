import sys
import os
import json
import xmltodict
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QLineEdit

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)

def convert(data, input_format, output_format):
    if input_format == 'xml':
        data_dict = xmltodict.parse(data)
    elif input_format == 'json':
        data_dict = json.loads(data)
    elif input_format in ('yml', 'yaml'):
        data_dict = yaml.safe_load(data)
    else:
        raise ValueError(f'Unsupported input format: {input_format}')

    if output_format == 'xml':
        return xmltodict.unparse(data_dict, pretty=True)
    elif output_format == 'json':
        return json.dumps(data_dict, indent=4)
    elif output_format in ('yml', 'yaml'):
        return yaml.dump(data_dict, default_flow_style=False)
    else:
        raise ValueError(f'Unsupported output format: {output_format}')

def main(input_path, output_path):
    input_format = input_path.split('.')[-1]
    output_format = output_path.split('.')[-1]

    data = read_file(input_path)
    converted_data = convert(data, input_format, output_format)
    write_file(output_path, converted_data)

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Converter')

        layout = QVBoxLayout()

        self.input_label = QLabel('Select input file:')
        layout.addWidget(self.input_label)

        self.input_button = QPushButton('Browse...')
        self.input_button.clicked.connect(self.browse_input_file)
        layout.addWidget(self.input_button)

        self.output_label = QLabel('Select output file:')
        layout.addWidget(self.output_label)

        self.output_button = QPushButton('Browse...')
        self.output_button.clicked.connect(self.browse_output_file)
        layout.addWidget(self.output_button)

        self.format_label = QLabel('Select output format:')
        layout.addWidget(self.format_label)

        self.format_combo = QComboBox()
        self.format_combo.addItems(['xml', 'json', 'yaml'])
        layout.addWidget(self.format_combo)

        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert_file)
        layout.addWidget(self.convert_button)

        self.status_label = QLabel('')
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def browse_input_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "All Files (*);;XML Files (*.xml);;JSON Files (*.json);;YAML Files (*.yml *.yaml)", options=options)
        if file:
            self.input_label.setText(f'Selected input file: {file}')
            self.input_path = file

    def browse_output_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "All Files (*);;XML Files (*.xml);;JSON Files (*.json);;YAML Files (*.yml *.yaml)", options=options)
        if file:
            self.output_label.setText(f'Selected output file: {file}')
            self.output_path = file

    def convert_file(self):
        if hasattr(self, 'input_path') and hasattr(self, 'output_path'):
            try:
                input_format = self.input_path.split('.')[-1]
                output_format = self.format_combo.currentText()
                main(self.input_path, self.output_path)
                self.status_label.setText('Conversion successful!')
            except Exception as e:
                self.status_label.setText(f'Error: {e}')
        else:
            self.status_label.setText('Please select both input and output files.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterApp()
    ex.show()
    sys.exit(app.exec_())
