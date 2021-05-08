import subprocess, sys


if __name__ == "__main__":
    BLOCK_START = int(sys.argv[1])
    BLOCK_END = int(sys.argv[2])
    SIZE = 10

    start = BLOCK_START
    if BLOCK_END <= BLOCK_START+SIZE:
        end = BLOCK_END
    else:
        end = BLOCK_START+SIZE - ((BLOCK_START+SIZE) % 10)
    count = 1
    if BLOCK_START <= BLOCK_END :
        while (True):
            # run cmd
            print("->", count, start, end)
            cmd = ['ethereumetl', 'export_blocks_and_transactions', '--start-block', str(start), '--end-block', str(end), '--blocks-output', 'baseline_blocks_{}.csv'.format(count), '--transactions-output', 'baseline_txs_{}.csv'.format(count), '--provider-uri', 'file:/Users/earthsiwapol/master-degree/ethereum/database/nodeBaseline/geth.ipc', '--batch-size', '5']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p.wait()

            # update counter
            count += 1

            if end == BLOCK_END:
                break
            # set interval
            start = end+1
            end += SIZE
            if end > BLOCK_END:
                end = BLOCK_END




