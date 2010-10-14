// Copyright (c) 2010 Satoshi Nakamoto
// Distributed under the MIT/X11 software license, see the accompanying
// file license.txt or http://www.opensource.org/licenses/mit-license.php.

class CBlock;
class CTransaction;

void ThreadRPCServer(void* parg);
int CommandLineRPC(int argc, char *argv[]);

void ThreadHTTPPOST(void* parg);

void monitorTransaction(const CTransaction& transaction, const CBlockIndex* pblockindex);
void monitorBlock(const CBlockIndex* pblockindex);
