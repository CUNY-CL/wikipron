#!/usr/bin/env python

import random
import argparse
import logging

def main(args):
    with open(args.input_path, "r") as source:
        data = [line.rstrip() for line in source]
        random.seed(args.seed)
        random.shuffle(data)
   
        train_size= int(len(data) * 0.8)
        dev_size = int(len(data) * 0.9)
        test_size =  int(len(data))
    
        train_set = data[ : train_size]
        dev_set = data[train_size: dev_size]
        test_set = data[dev_size: test_size]
    
        with open(args.train, "w") as sink:
            for line in train_set:
                print(line, file=sink)
        with open(args.dev, "w") as sink:
            for line in dev_set:
                print(line, file=sink)
        with open(args.test, "w") as sink:
            for line in test_set:
                print(line, file=sink)
                
    logging.basicConfig(level=logging.INFO)            
    logging.info(f'Train set size: {len(train_set)}')
    logging.info(f'Val set size: {len(dev_set)}')
    logging.info(f'Test set size: {len(test_set)}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('seed',type=int, help = "Seed number for shuffling data" )
    parser.add_argument('input_path', help = "Input data path" )
    parser.add_argument('train', help = "Output train set" )
    parser.add_argument('dev', help = "Output dev set")
    parser.add_argument('test', help = "Output test set")
    main(parser.parse_args())
