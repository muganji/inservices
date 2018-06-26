from app import app as application

def main():
    application.run(host='0.0.0.0', debug=None)

if __name__ == '__main__':
    main()