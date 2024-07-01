from numpy import array
from numpy.linalg import norm

ROBOT_VEL_NORM = 0.1 # m/s

class Node:
    def __init__(self, nodeId: str, nodePositionX: float, nodePositionY: float, allowedDeviationXY: float, released: bool = True) -> None:
        self.nodeId = nodeId
        self.nodePosition = array([nodePositionX, nodePositionY])
        self.allowedDeviationXY = allowedDeviationXY
        self.released = released

class Edge:
    def __init__(self, edgeId: str, startNode: Node, endNode: Node, released: bool = True) -> None:
        self.edgeId = edgeId
        self.startNode = startNode
        self.endNode = endNode
        self.released = released

class Robot:
    def __init__(self, posX: float, posY: float) -> None:
        self.robotPosition = array([posX, posY])
        
        self.currentNode = None
        self.nextNode = None
        self.currentEdge = None
    
        self.nodeList = []
        self.edgeList = []

        self.robotVelocity = array([0.0, 0.0])
    
    def receiveOrder(self, nodeList: list[Node], edgeList: list[Edge]) -> None:
        self.nodeList = nodeList
        self.edgeList = edgeList

        self.currentNode = self.nodeList[0]

        if (len(nodeList) > 1):
            self.nextNode = self.nodeList[1]
            self.currentEdge = self.edgeList[0]

    def step(self) -> None:
        # Calculate robot velocity to reach the next node
        if self.nextNode is not None:
            dist = self.nextNode.nodePosition - self.robotPosition
            if norm(dist) < ROBOT_VEL_NORM:
                self.robotVelocity = dist
            else:
                self.robotVelocity = ROBOT_VEL_NORM * dist/norm(dist)
        
            # Make robot move
            self.robotPosition += self.robotVelocity

            # Check if robot reached the next node
            dist = self.nextNode.nodePosition - self.robotPosition
            if norm(dist) <= self.nextNode.allowedDeviationXY:
                self.currentNode = self.nextNode
                
                # Remove old node
                self.nodeList.pop(0)
                
                # Set new next node and edge
                if (len(self.nodeList) > 1):
                    self.nextNode = self.nodeList[1]
                    self.currentEdge = self.edgeList[0]
                else:
                    self.nextNode = None
                    self.currentEdge = None