import torch
import argparse
import numpy as np
import random
import torch.optim as optim
import torch.nn as nn
import flwr as fl
from models import *
from data import data_loaders
from clients import SpinsClient


def main():
    use_cuda = not args.no_cuda and torch.cuda.is_available()

    torch.cuda.set_device(args.client_id % 4)

    torch.manual_seed(args.seed)
    random.seed(args.seed)
    np.random.seed(args.seed)

    device = torch.device("cuda" if use_cuda else "cpu")
    model = SpinsConv6().to(device)
    optimizer = optim.Adam([p for p in model.parameters() if p.requires_grad])
    criterion = nn.CrossEntropyLoss()

    train_loaders, test_loader = data_loaders(args.client_id, args.data, args.is_iid, use_cuda, args.batch_size, args.test_batch_size)

    # Start client
    fl.client.start_numpy_client("[::]:8080", client=SpinsClient(model, optimizer, criterion, device, train_loaders, test_loader, args))




if __name__ == '__main__':
    # Training settings
    parser = argparse.ArgumentParser(description='SPinS-FL simulator')
    parser.add_argument('client_id', type=int, choices=list(range(10)),
                            help='ID of the client. Choose from [0,1...,9]')
    parser.add_argument('--seed', type=int, default=0,
                            help='base seed')
    parser.add_argument('--localPinRate', type=float, default=0.5,
                            help='local Pinning Rate')
    parser.add_argument('--is_iid', type=int, choices=list(range(2)),
                            help='set to 1 if you want to split dataset in iid distribution, otherwise 0')
    parser.add_argument('--globalPinRate', type=float, default=0.1,
                            help='the global Pinning rate in the global model')
    parser.add_argument('--batch-size', type=int, default=10, metavar='N',
                            help='input batch size for training (default: 8)')
    parser.add_argument('--test-batch-size', type=int, default=100, metavar='N',
                            help='input batch size for testing (default: 100)')
    parser.add_argument('--epochs', type=int, default=1, metavar='N',
                            help='number of epochs to train (default: 14)')
    parser.add_argument('--load_checkpoint', type=bool, default=False,
                            help='whether you load checkpoint')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                            help='disables CUDA training')
    parser.add_argument('--save-model', action='store_true', default=False,
                            help='For Saving the current Model')
    parser.add_argument('--data', type=str, default='../data', help='Location to store data')

    global args
    args = parser.parse_args()

    main()
