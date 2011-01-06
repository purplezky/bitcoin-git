// Copyright (c) 2010 Satoshi Nakamoto
// Distributed under the MIT/X11 software license, see the accompanying
// file license.txt or http://www.opensource.org/licenses/mit-license.php.

class CBlock;
class CBlockIndex;
class CWalletTx;

void ThreadRPCServer(void* parg);
int CommandLineRPC(int argc, char *argv[]);

void ThreadHTTPPOST(void* parg);

void monitorTx(const CWalletTx& tx);
void monitorBlock(const CBlock& block, const CBlockIndex* pblockindex);
