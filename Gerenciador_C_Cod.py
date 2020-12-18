from PyQt5 import uic
import PyQt5.QtWidgets as QtWidgets
import mysql.connector
 
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="gerenciador_combustivel"
)

def abrir_cadastro_usuario():
    tela_login.close()
    tela_cadastrar_usuario.show()

def cadastro_usuario():
    nomecadastro = tela_cadastrar_usuario.lineEdit.text()
    senhacad = tela_cadastrar_usuario.lineEdit_3.text()
    senhacadconf = tela_cadastrar_usuario.lineEdit_4.text()
    try:
        if(senhacad == senhacadconf):
            if(len(senhacad) >= 6) and (len(senhacad) <= 30):
                cursor = banco.cursor()
                comando_SQL = "INSERT INTO users (username, senha) VALUES(%s, %s)"
                info = (str(nomecadastro),str(senhacad))
                cursor.execute(comando_SQL,info)
                banco.commit()
                
                tela_cadastrar_usuario.lineEdit.setText("") 
                tela_cadastrar_usuario.lineEdit_3.setText("")
                tela_cadastrar_usuario.lineEdit_4.setText("")
                            
                tela_cadastrar_usuario.close()
                tela_login.show()
            else:
                tela_cadastrar_usuario.label_2.setText("Senha deve conter de 6 a 30 caracteres")

        else:
            tela_cadastrar_usuario.label_2.setText("Erro, Senhas Incompativeis")
    except:
        tela_cadastrar_usuario.label_2.setText("Erro, Campos nulos ou nome Já registrado!")

def tela_inicial():
    name = tela_login.lineEdit.text()
    password = tela_login.lineEdit_2.text()
    try:
        cursor = banco.cursor()
        cursor.execute(f"SELECT senha from users WHERE username ='{name}'")
        catpass = cursor.fetchall()
        if(password == catpass[0][0]):
            tela_login.close()
            tela_home.show()
            tela_home.label_2.setText(f"Olá, {name}")
        else:
            tela_login.label_4.setText("Senha errada")

    except:
        tela_login.label_4.setText("Erro, Cadastre-se")

def abrir_media():
    tela_home.close()
    tela_media.show()

def fazer_calculo():
    lts_abastecidos = tela_media.lineEdit.text()
    km = tela_media.lineEdit_2.text()
    lts = float(lts_abastecidos)
    kms = float(km)
    calc = kms / lts
    tela_media.label_4.setText("Seu automovel fez {:.2f} km/l".format(calc))


app = QtWidgets.QApplication([])
tela_login = uic.loadUi("logintela.ui")
tela_cadastrar_usuario = uic.loadUi("cadastrotela.ui")
tela_home = uic.loadUi("home.ui")
tela_media = uic.loadUi("mediacombustivel.ui")

tela_login.pushButton_3.clicked.connect(tela_inicial)
tela_login.pushButton_2.clicked.connect(abrir_cadastro_usuario)
tela_cadastrar_usuario.pushButton.clicked.connect(cadastro_usuario)
tela_home.pushButton.clicked.connect(abrir_media)
tela_media.pushButton.clicked.connect(fazer_calculo)


tela_login.show()
app.exec()