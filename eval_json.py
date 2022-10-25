import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--model_root', default='data')
    parser.add_argument('--json_root', default='eval')
    parser.add_argument('--model_root', default='data')
    parser.add_argument('--save', default='img')

    args = parser.parse_args()

    
    