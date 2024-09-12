from lib.model import predict_all

if __name__ == "__main__":
    interval = input('Enter the target interval (the available intervals are: 1d, 60m, 1m): ')

    if interval not in ['1m', '60m', '1d']:
        raise Exception('Invalid interval')

    print(predict_all(interval))
