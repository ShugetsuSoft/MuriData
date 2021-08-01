import merkletools
import bencode
import nmslib
import random
import math

newVector = lambda : [random.randint(-10000, 10000) for i in range(5)]
newSegment = lambda : [newVector() for i in range(40000)]

class VectorSegment(object):
    def __init__(self, vectors):
        self.mktree = merkletools.MerkleTools(hash_type="SHA256")
        self.vectors = vectors
        for vector in vectors:
            self.mktree.add_leaf(self.mktree.hash_function(bencode.bencode(vector).encode()).hexdigest())
        self.mktree.make_tree()
    def getSegSize(self):
        return len(self.vectors)
    def getSegId(self):
        return self.mktree.get_merkle_root()
    def getVector(self, index):
        return self.vectors[index]
    def getProof(self, index):
        return self.mktree.get_proof(index)
    def valProofIndex(self, proof, vectorIndex):
        return self.mktree.validate_proof(proof, self.mktree.get_leaf(vectorIndex), self.mktree.get_merkle_root())
    def valProof(self, proof, vector):
        return self.mktree.validate_proof(proof, self.mktree.hash_function(bencode.bencode(vector).encode()).hexdigest(), self.mktree.get_merkle_root())

class VectorSegmentList(object):
    def __init__(self):
        self.segList = {}
        self.index = None
        self.id2seg = []
    def addSeg(self, segment: VectorSegment):
        self.segList[segment.getSegId()] = segment
    def removeSeg(self, segId):
        self.segList.popitem(segId)
    def valSeg(self, segId, merkleProof, vector):
        return self.segList[segId].valProof(merkleProof, vector)
    def buildIndex(self):
        self.index = nmslib.init(method='hnsw', space='cosinesimil')
        vecid = 0
        self.id2seg = []
        for (segId, segment) in self.segList.items():
            for (index, vec) in enumerate(segment.vectors):
                self.index.addDataPoint(vecid, vec)
                self.id2seg.append((segId, index))
                vecid += 1
        self.index.createIndex()
    def queryVector(self, vector):
        res = []
        if not self.index:
            raise Exception("Index not built yet")
        ids, distances = self.index.knnQuery(vector, k=3)
        for i in ids:
            segId, segIndex = self.id2seg[i]
            segment = self.segList[segId]
            res.append((segId, segment.getProof(segIndex), segment.getVector(segIndex)))
        return res

if __name__ == "__main__":
    veclist = VectorSegmentList()
    seg1 = VectorSegment(newSegment())
    seg2 = VectorSegment(newSegment())
    veclist.addSeg(VectorSegment(newSegment()))
    
    veclist.addSeg(seg2)
    veclist.addSeg(seg1)
    
    veclist.buildIndex()

    vecIndex = 1
    vector = seg2.getVector(vecIndex)
    vector[0] += 10
    segId = seg2.getSegId()
    
    queryRes = veclist.queryVector(vector)
    print(queryRes)
    
    
    