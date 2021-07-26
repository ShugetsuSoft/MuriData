# MuriData Protocol

## Technology Stack
- BlockChain
- BFT Consensus
- Consistent hashing
- Distributed Hash Table
- Distributed Computing
- Distributed Storage
- Recursive Distributed Rendezvous
- Vector Indexing (Annoy Faiss NMSLib)
- And Some Kawaii Characters (Very important!!!)

## Glossary
- **Magu** : One vector database with index.
- **MurIndexer** : Single node in a **Magu** who perform searching tasks.
- **MuriData** : The general term of this system.
- **MuriChain** : The blockchain where muridata runs on.
- **MURI** : The token of this whole ecosystem.

## Introduction
MuriData is the name of the decentralized vector searching service. It includes a blockchain to organize nodes, give incentives and allocate tasks.

With MuriData, everyone could either publish a vector database or search on existing databases. Some specialized Indexing nodes will deal with queries and reach a consensus towards the best result.


## Design
### Layer 1 : Blockchain
The MuriData will run on the base of MuriChain.
MuriChain is designed to handle the transactions of the token **MURI**, which could be used as both a payment method of searching for data and a governance tool for the whole community.

There is no special requirement for the implementation of MuriChain. It could be a fork of either Ethereum or Polkadot or etc. However, to allocate tasks, it must be able to track a list of **Magu** and perform incentives and punishments, which also requires a higher scalability and speed.

### Layer 2 : Magus
**Magu** refers to the Japanese version of "mug". In MuriData this means a cluster of nodes who maintain a corresponding database. Because in order to search for a vector, nodes must store the vector data and related index data, which is impossible when the vector database is extremely large. To increase the scalability, support big data, and also prevent the single point of failure(SPOF), the searching task must be run on a number of nodes. With **Magus**, searching tasks could be finished efficiently and effectively.

### Operations

#### Publishing a Magu (Vector Database)
The database is created when an account send a transaction indicating the creation of one database, with the staking of some **MURI** Token and related data published at the network. The whole network would orgnize a **Magu** for this database and randomly choose some nodes to become its members, **MurIndexer**s. These nodes would form a small consensus group dealing with any tasks related to this database.

#### Becoming a MurIndexer
A node who wants to become a **MurIndexer** and provide indexing ability for the whole network will first stake some **MURI** with the promise of being online and store some data during a time interval. After staked some token, it would be on the list of candidates and allocated to a random **Magu**. It will start to store some vectors and perform tasks.

#### Searching for vectors
When a searching task is commited on the blockchain, the **Magu** would receive the task and start the searching process. Every **MurIndexer** would search for the nearst k vectors within its local data and send it to its **Magu**. Then all **MurIndexer**s will reach a consensus on the top k best result among those commitments and finally commit it on the blockchain. The task would finish and receive a result.