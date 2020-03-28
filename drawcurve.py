import argparse
import sys
import matplotlib.pyplot as plt
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file",  help = "path to log file"  )
    parser.add_argument( "option", help = "0 -> loss vs iter"  )
    parser.add_argument( "begin", help = "begin of line"  )
    args = parser.parse_args()
    f = open(args.log_file)
    
    begin = int(args.begin)
    print(begin)
    lines  = [line.rstrip("\n") for line in f.readlines()]
    # skip the first 3 lines
    lines = lines[3:]
    numbers = {'1','2','3','4','5','6','7','8','9','0'}
    iters = []
    loss = []
    loss_avg = []
    time_e = []
    for line in lines:
        if line[0] in numbers:
            args = line.split(" ")
            if len(args) >3:
                iters.append(int(args[0][:-1]))
                loss.append(float(args[1][:-1]))
                loss_avg.append(float(args[2]))
                time_e.append(float(args[6]))
    plt.figure(12,figsize=(15, 15))
    plt.subplot(311)
    plt.plot(iters[begin:],loss_avg[begin:],'r',iters[begin:],loss[begin:],'g',)
    plt.xlabel('iters')
    plt.ylabel('loss')
    plt.grid()

    plt.subplot(312)
    plt.plot(iters[begin:],time_e[begin:])
    plt.xlabel('iters')
    plt.ylabel('time')
    plt.grid()

    plt.subplot(313)
    plt.plot(iters[begin:],loss_avg[begin:],'r',iters[begin:],loss[begin:],'g',iters[begin:],time_e[begin:],'b')
    plt.xlabel('iters')
    plt.ylabel('loss')
    plt.grid()
    plt.show()
if __name__ == "__main__":
    main(sys.argv)
