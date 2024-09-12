from lib.model import retrain_model

if __name__ == "__main__":
    interval = input('Enter the target interval (the available intervals are: 1d, 60m, 1m): ')

    if interval not in ['1m', '60m', '1d']:
        raise Exception('Invalid interval')

    retrain_model(interval)
