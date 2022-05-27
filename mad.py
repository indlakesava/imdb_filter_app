import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QTableView
import PyQt5.QtCore as QtCore
import pandas as pd


class TableModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

class AppDemo(QWidget):
	def __init__(self):
		super().__init__()
		self.setStyleSheet('font-size: 25px;')
		self.setWindowTitle('All About Movies')
		self.setMinimumWidth(600)
		self.showMaximized()
		self.rating = ['select rating', '<5', '5.0-5.9', '6.0-6.9', '7.0-7.9', '8.0-8.9', '>=9.0']
		self.release_year = ['select release year', '<1950', '1950-1999', '2000-2004','2005-2009','2010-2016']
		self.genre = ['select genre', 'Action', 'Adventure', 'Fantasy', 'Sci-Fi', 'Thriller', 'Romance', 'Animation', 'Comedy', 'Family', 'Musical', 'Mystery', 'Western', 'Drama', 'History', 'Sport', 'Crime', 'Horror', 'War', 'Biography', 'Music', 'Documentary', 'Film-Noir']
		self.data = pd.DataFrame()
		self.loadData()

		layout = QVBoxLayout()
		self.setLayout(layout)

		self.comboRating = QComboBox()
		self.comboRating.addItems(self.rating)
		layout.addWidget(self.comboRating)

		self.comboYear = QComboBox()
		self.comboYear.addItems(self.release_year)
		layout.addWidget(self.comboYear)

		self.comboGenre = QComboBox()
		self.comboGenre.addItems(self.genre)
		layout.addWidget(self.comboGenre)

		self.table = QTableView()
		self.model = TableModel(self.data)
		self.table.setModel(self.model)
		layout.addWidget(self.table)

		self.comboRating.currentIndexChanged.connect(self.updateTable)
		self.comboYear.currentIndexChanged.connect(self.updateTable)
		self.comboGenre.currentIndexChanged.connect(self.updateTable)

		self.updateTable()

	def loadData(self):
		self.data = pd.read_excel('final.xlsx')

	def updateTable(self):
		selected_rating = self.comboRating.currentText()
		selected_year = self.comboYear.currentText()
		selected_genre = self.comboGenre.currentText()
		df = self.data
		default = False
		if selected_rating=='select rating' and selected_year=='select release year' and selected_genre=='select genre':
			default = True
		else:
			if selected_rating!='select rating':
				if selected_rating=='<5':
					df = df[(df['imdb_score']<5)]
				elif selected_rating=='5.0-5.9':
					df = df[(df['imdb_score']>=5.0) & (df['imdb_score']<6.0)]
				elif selected_rating=='6.0-6.9':
					df = df[(df['imdb_score']>=6.0) & (df['imdb_score']<7.0)]
				elif selected_rating=='7.0-7.9':
					df = df[(df['imdb_score']>=7.0) & (df['imdb_score']<8.0)]
				elif selected_rating=='8.0-8.9':
					df = df[(df['imdb_score']>=8.0) & (df['imdb_score']<9.0)]
				elif selected_rating=='>=9.0':
					df = df[(df['imdb_score']>=9.0)]

			if selected_year!='select release year':
				if selected_year=='<1950':
					df = df[(df['title_year']<1950)]
				elif selected_year=='1950-1999':
					df = df[(df['title_year']>=1950) & (df['title_year']<1999)]
				elif selected_year=='2000-2004':
					df = df[(df['title_year']>=2000) & (df['title_year']<2004)]
				elif selected_year=='2005-2009':
					df = df[(df['title_year']>=2005) & (df['title_year']<2009)]
				elif selected_year=='2010-2016':
					df = df[(df['title_year']>=2010)]

			if selected_genre != "select genre":
				df = df[(df['genres'].str.contains(self.comboGenre.currentText(), case=False))]

		self.model = TableModel(df)
		self.table.setModel(self.model)
		self.table.resizeColumnsToContents()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = AppDemo()
	demo.show()

	try:
		sys.exit(app.exec_())
	except SystemExit:
		print('Closing Window...')