from project import app, logger


if __name__ == '__main__':
    logger.info('Starting the app')
    app.run(debug=True)
