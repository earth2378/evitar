import subprocess, sys


if __name__ == "__main__":
    BLOCK_START = 13
    BLOCK_END = int(sys.argv[1])
    SIZE = 100

    start = BLOCK_START
    if BLOCK_END <= SIZE:
        end = BLOCK_END
    else:
        end = SIZE
    count = 1
    if BLOCK_START <= BLOCK_END :
        while (True):
            # run cmd
            print("->", count)
            cmd = ['ethereumetl', 'export_blocks_and_transactions', '--start-block', str(start), '--end-block', str(end), '--blocks-output', 'baseline_blocks_{}.csv'.format(count), '--transactions-output', 'baseline_txs_{}.csv'.format(count), '--provider-uri', 'file:/Users/earthsiwapol/master-degree/ethereum/database/nodeBaseline/geth.ipc', '--batch-size', '10']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            for line in p.stdout:
                print(line)
            p.wait()
            # print(p.returncode)

            # update counter
            count += 1

            if end == BLOCK_END:
                break
            # set interval
            start += SIZE
            end += SIZE
            if end > BLOCK_END:
                end = BLOCK_END




