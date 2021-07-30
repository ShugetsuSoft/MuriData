import merkletools
import bencode

class VectorSegment(object):
    def __init__(self, vectors, dimension = 100, count = 500):
        self.mktree = merkletools.MerkleTools(hash_type="SHA256")
        assert len(vectors) == count # One Vector Segment contains fixed number of vectors.
        self.vectors = vectors
        for vector in vectors:
            assert len(vector) == dimension
            self.mktree.add_leaf(self.mktree.hash_function(bencode.bencode(vector).encode()).hexdigest())
        self.mktree.make_tree()
    def getSegId(self):
        return self.mktree.get_merkle_root()
    def getProof(self, index):
        return self.mktree.get_proof(index)
    def valProofIndex(self, proof, vectorIndex):
        return self.mktree.validate_proof(proof, self.mktree.get_leaf(vectorIndex), self.mktree.get_merkle_root())
    def valProof(self, proof, vector):
        return self.mktree.validate_proof(proof, self.mktree.hash_function(bencode.bencode(vector).encode()).hexdigest(), self.mktree.get_merkle_root())

class VectorSegmentList(object):
    def __init__(self):
        self.segList = {}
    def addSeg(self, segment: VectorSegment):
        self.segList[segment.getSegId()] = segment
    def removeSeg(self, segId):
        self.segList.popitem(segId)
    def valSeg(self, segId, merkleProof, vector):
        return self.segList[segId].valProof(merkleProof, vector)

if __name__ == "__main__":
    veclist = VectorSegmentList()
    seg1 = VectorSegment([[1,1,0], [1,1,2]], 3, 2)
    seg2 = VectorSegment([[4,3,4,5], [12,43,432,43], [31312213,231321321,321213321,3223123]], 4, 3)
    veclist.addSeg(seg1)
    veclist.addSeg(seg2)
    
    proof = seg2.getProof(2) # [31312213,231321321,321213321,3223123]
    segId = seg2.getSegId()
    
    result = veclist.valSeg(segId, proof, [31312213,231321321,321213321,3223123])
    assert result
    