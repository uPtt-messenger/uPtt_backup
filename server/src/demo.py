from util.src.log import Logger

if __name__ == '__main__':
    logger = Logger('demo logger', Logger.INFO)

    logger.show(
        Logger.INFO,
        'demo log')

    logger.show_value(
        Logger.INFO,
        'show value',
        12)
