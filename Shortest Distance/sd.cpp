#include "weightedGraph.h"
#include <iostream>

using namespace std;

int main() {
  weightedGraphType graph(5);

  graph.createWeightedGraph();

  graph.shortestPath(1);
  graph.printShortestDistance(1);

  return 0;
}
