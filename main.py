from db.connection import init_db
from gui.app import App

if __name__ == '__main__':
    init_db()
    app = App()
    app.mainloop()