#include <iostream>

using namespace std;

template <class recType, int bTreeOrder> struct bTreeNode {
  int recCount;
  recType list[bTreeOrder - 1];
  bTreeNode *children[bTreeOrder];
};

template <class recType, int bTreeOrder> class bTree {
public:
  bool search(const recType &searchItem);
  // Function to determine if searchItem is in the B-tree.
  // Postcondition: Returns true if searchItem is found in the
  //  B-tree; otherwise, returns false.
  void insert(const recType &insertItem);
  // Function to insert insertItem in the B-tree.
  // Postcondition: If insertItem is not in the the B-tree, it
  //  is inserted in the B-tree.
  void inOrder();
  // Function to do an inorder traversal of the B-tree.
  bTree();
  // constructor

protected:
  bTreeNode<recType, bTreeOrder> *root;

private:
  void searchNode(bTreeNode<recType, bTreeOrder> *current, const recType &item,
                  bool &found, int &location);
  void insertBTree(bTreeNode<recType, bTreeOrder> *current,
                   const recType &insertItem, recType &median,
                   bTreeNode<recType, bTreeOrder> *&rightChild, bool &isTaller);
  void insertNode(bTreeNode<recType, bTreeOrder> *current,
                  const recType &insertItem,
                  bTreeNode<recType, bTreeOrder> *&rightChild,
                  int insertPosition);
  void splitNode(bTreeNode<recType, bTreeOrder> *current,
                 const recType &insertItem,
                 bTreeNode<recType, bTreeOrder> *rightChild, int insertPosition,
                 bTreeNode<recType, bTreeOrder> *&rightNode, recType &median);
  void recInorder(bTreeNode<recType, bTreeOrder> *current);
};

template <class recType, int bTreeOrder> bTree<recType, bTreeOrder>::bTree() {
  root = nullptr;
} // end constructor

template <class recType, int bTreeOrder>
bool bTree<recType, bTreeOrder>::search(const recType &searchItem) {
  bool found = false;
  int location;
  bTreeNode<recType, bTreeOrder> *current;
  current = root;
  while (current != nullptr && !found) {
    searchNode(current, searchItem, found, location);
    if (!found)
      current = current->children[location];
  }
  return found;
} // end search

template <class recType, int bTreeOrder>
void bTree<recType, bTreeOrder>::searchNode(
    bTreeNode<recType, bTreeOrder> *current, const recType &item, bool &found,
    int &location) {
  int low = 0;
  int high = current->recCount - 1;
  found = false;

  while (low <= high) {
    int mid = low + (high - low) / 2;

    if (current->list[mid] == item) {
      found = true;
      location = mid;
      return;
    } else if (item < current->list[mid]) {
      high = mid - 1;
    } else {
      low = mid + 1;
    }
  }

  location = low;
} // end searchNode

template <class recType, int bTreeOrder>
void bTree<recType, bTreeOrder>::insert(const recType &insertItem) {
  bool isTaller = false;
  recType median;

  bTreeNode<recType, bTreeOrder> *rightChild;

  insertBTree(root, insertItem, median, rightChild, isTaller);

  if (isTaller) // the tree is initially empty or the root
  // was split by the function insertBTree
  {
    bTreeNode<recType, bTreeOrder> *tempRoot;
    tempRoot = new bTreeNode<recType, bTreeOrder>;
    tempRoot->recCount = 1;
    tempRoot->list[0] = median;
    tempRoot->children[0] = root;
    tempRoot->children[1] = rightChild;

    root = tempRoot;
  }
} // insert

template <class recType, int bTreeOrder>
void bTree<recType, bTreeOrder>::insertBTree(
    bTreeNode<recType, bTreeOrder> *current, const recType &insertItem,
    recType &median, bTreeNode<recType, bTreeOrder> *&rightChild,
    bool &isTaller) {
  int position;
  isTaller = false;

  if (current == nullptr) {
    median = insertItem;
    rightChild = nullptr;
    isTaller = true;
  } else {
    bool found;

    searchNode(current, insertItem, found, position);

    if (found)
      cout << "Cannot insert duplicate record." << endl;
    else {
      recType newMedian;

      bTreeNode<recType, bTreeOrder> *newChild;

      insertBTree(current->children[position], insertItem, newMedian, newChild,
                  isTaller);

      if (isTaller) {
        if (current->recCount < bTreeOrder - 1) {
          isTaller = false;
          insertNode(current, newMedian, newChild, position);
        } else
          splitNode(current, newMedian, newChild, position, rightChild, median);
      }
    }
  }
} // insertBTree

template <class recType, int bTreeOrder>
void bTree<recType, bTreeOrder>::insertNode(
    bTreeNode<recType, bTreeOrder> *current, const recType &insertItem,
    bTreeNode<recType, bTreeOrder> *&rightChild, int insertPosition) {
  int index;

  for (index = current->recCount; index > insertPosition; index--) {
    current->list[index] = current->list[index - 1];
    current->children[index + 1] = current->children[index];
  }

  current->list[index] = insertItem;
  current->children[index + 1] = rightChild;
  current->recCount++;
} // end insertNode

template <class recType, int bTreeOrder>
void bTree<recType, bTreeOrder>::splitNode(
    bTreeNode<recType, bTreeOrder> *current, const recType &insertItem,
    bTreeNode<recType, bTreeOrder> *rightChild, int insertPosition,
    bTreeNode<recType, bTreeOrder> *&rightNode, recType &median) {
  rightNode = new bTreeNode<recType, bTreeOrder>;

  int mid = (bTreeOrder - 1) / 2;

  if (insertPosition <= mid) // new item goes in the first
  // half of the node
  {
    int index = 0;
    int i = mid;

    while (i < bTreeOrder - 1) {
      rightNode->list[index] = current->list[i];
      rightNode->children[index + 1] = current->children[i + 1];
      index++;
      i++;
    }

    current->recCount = mid;
    insertNode(current, insertItem, rightChild, insertPosition);
    (current->recCount)--;

    median = current->list[current->recCount];

    rightNode->recCount = index;
    rightNode->children[0] = current->children[current->recCount + 1];
  } else // new item goes in the second half of the node
  {
    int i = mid + 1;
    int index = 0;

    while (i < bTreeOrder - 1) {
      rightNode->list[index] = current->list[i];
      rightNode->children[index + 1] = current->children[i + 1];
      index++;
      i++;
    }

    current->recCount = mid;
    rightNode->recCount = index;

    median = current->list[mid];
    insertNode(rightNode, insertItem, rightChild, insertPosition - mid - 1);
    rightNode->children[0] = current->children[current->recCount + 1];
  }
} // splitNode

template <class recType, int bTreeOrder>
void bTree<recType, bTreeOrder>::inOrder() {
  recInorder(root);
} // end inOrder

template <class recType, int bTreeOrder>
void bTree<recType, bTreeOrder>::recInorder(
    bTreeNode<recType, bTreeOrder> *current) {
  if (current != nullptr) {
    recInorder(current->children[0]);
    for (int i = 0; i < current->recCount; i++) {
      cout << current->list[i] << " ";
      recInorder(current->children[i + 1]);
    }
  }
} // end recInorder
