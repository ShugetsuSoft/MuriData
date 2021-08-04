# MuriData Protocol Detailed Designs

This document includes a possible implementation of the MuriData Protocol.

## BlockChain Details

All the consensus about **Magu**s and token incentives will be handled by **MuriChain**. It should be able to track a list of **Magu**s and their corresponding Vector Segments.

### Magus List

One Magu represents One database. A new Magu with special id and name would be created in the blockchain.
Its current state could be represented as:

| Id | Name | Access Controller | Nodes | Vector Segments | Vector Dimensions | Node Quantity |
|----|------|-------------------|-------|-----------------|--------------------|------------|

***Name*** is specified by the creater.
***Access Controller*** refers to the account that can manage and add vectors to it.
***Nodes*** is the list of node in it.
***Vector Segments*** can be the list of all **vector segments** in it.

### Nodes List

Every Magu must have a list of nodes for allocating tokens and tasks.

| NodeId | NodeStatus | AccountPublicKey |
|--------|------------|------------------|

***NodeId*** is generated from the public key of a node, which is also used in DHT for peer discovery.
***NodeStatus*** indicates the status of this node, including its allowed disk spaces, computing ability and so on.
***AccountPublicKey*** is the account that controls the node. An account could be added to a node and is responsible for the behavior of this node.

### Vector Segments

| Merkel Root | Vector Data Source |
|-------------|--------------------|

A vector segment is identified by its ***Merkel Root***. It is also used to proof the existence of one vector. 
***Vector Data Source*** is the source of vector data, such as ipfs or other blockchain, usually being a hash pointer.

[Code Example](examples/vector_segment.py)

## Searching for vector

When MurIndexers in a Magu receive a query from MuriChain, they will start searching for the nearst results for this vector. They search them in the index, adding to a list of vectors, then give each of them a merkle proof and signature. After finishing this work, they will send the hash of this list to their Magu. When all node send their result hash, they will send their result. Any node who refuse to send the hash in a specified time interval or send the vector list will be punished, and removed from this Magu.
Their vector list looks like this:

| Segment Merkle Root | Merkle Proof | Vector | Signature |
|---------------------|--------------|--------|-----------|

The node id will be also sent with this list.

When MurIndexer receive all the vector lists of their partners, they will start ranking the vectors in all of the lists. All node will get a ordered list of vectors. Then the first-finished node will propose its result in the Magu, starting a BFT consensus. If this proposal gets most of the signature in this group, it will be sent to MuriChain.

## Node Details

MuriData Node is sperated into two: the blockchain node and index node.
Blockchain node deals with blockchain and index node is responsible for performing tasks. 
Index node is connected with blockchain node. They communicate by rpc calls.


