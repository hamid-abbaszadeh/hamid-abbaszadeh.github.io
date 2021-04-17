---
published: false
---

# Hash Table 
>The official name is unordered associative containers and
>bucket  is another name of index 

>In  [hashing](http://www.geeksforgeeks.org/hashing-data-structure/)  there is a hash function that maps keys to some values. But these hashing function may lead to collision that is two or more keys are mapped to same value.  **Chain hashing**  avoids collision. The idea is to make each cell of hash table point to a linked list of records that have same hash function value.
>Let’s create a hash function, such that our hash table has ‘N’ number of buckets.  
To insert a node into the hash table, we need to find the hash index for the given key. And it could be calculated using the hash function.  
**Example: hashIndex = key % noOfBuckets**
>**Insert**: Move to the bucket corresponds to the above calculated hash index and insert the new node at the end of the list.
>**Delete**: To delete a node from hash table, calculate the hash index for the key, move to the bucket corresponds to the calculated hash index, search the list in the current bucket to find and remove the node with the given key (if found).


**Hash table implementation for classic C++**

```cpp
// CPP program to implement hashing with chaining
#include<bits/stdc++.h>
using namespace std;

class Hash
{
	int BUCKET; // No. of buckets

	// Pointer to an array containing buckets
	list<int> *table;
public:
	Hash(int V); // Constructor

	// inserts a key into hash table
	void insertItem(int x);

	// deletes a key from hash table
	void deleteItem(int key);

	// hash function to map values to key
	int hashFunction(int x) {
		return (x % BUCKET);
	}

	void displayHash();
};

Hash::Hash(int b)
{
	this->BUCKET = b;
	table = new list<int>[BUCKET];
}

void Hash::insertItem(int key)
{
	int index = hashFunction(key);
	table[index].push_back(key);
}

void Hash::deleteItem(int key)
{
// get the hash index of key
int index = hashFunction(key);

// find the key in (inex)th list
list <int> :: iterator i;
for (i = table[index].begin();
		i != table[index].end(); i++) {
	if (*i == key)
	break;
}

// if key is found in hash table, remove it
if (i != table[index].end())
	table[index].erase(i);
}

// function to display hash table
void Hash::displayHash() {
for (int i = 0; i < BUCKET; i++) {
	cout << i;
	for (auto x : table[i])
	cout << " --> " << x;
	cout << endl;
}
}

// Driver program
int main()
{
// array that contains keys to be mapped
int a[] = {15, 11, 27, 8, 12};
int n = sizeof(a)/sizeof(a[0]);

// insert the keys into the hash table
Hash h(7); // 7 is count of buckets in
			// hash table
for (int i = 0; i < n; i++)
	h.insertItem(a[i]);

// delete 12 from hash table
h.deleteItem(12);

// display the Hash table
h.displayHash();

return 0;
}

```

**Hash table in C++ STL  (above C++11)**

```cpp
// C++ program to demonstrate functionality of unordered_map
#include <iostream>
#include <unordered_map>
using namespace std;

int main()
{
	// Declaring umap to be of <string, int> type
	// key will be of string type and mapped value will
	// be of int type
	unordered_map<string, int> umap;

	// inserting values by using [] operator
	umap["GeeksforGeeks"] = 10;
	umap["Practice"] = 20;
	umap["Contribute"] = 30;

	// Traversing an unordered map
	for (auto x : umap)
	cout << x.first << " " << x.second << endl;

}
```
**Methods on unordered_map**  
A lot of function are available which work on unordered_map. most useful of them are – operator =, operator [], empty and size for capacity, begin and end for iterator, find and count for lookup, insert and erase for modification.  
The C++11 library also provides function to see internally used bucket count, bucket size and also used hash function and various hash policies but they are less useful in real application.  
We can iterate over all elements of unordered_map using Iterator. Initialization, indexing and iteration is shown in below sample code :
```cpp
// C++ program to demonstrate functionality of unordered_map
#include <iostream>
#include <unordered_map>
using namespace std;

int main()
{
	// Declaring umap to be of <string, double> type
	// key will be of string type and mapped value will
	// be of double type
	unordered_map<string, double> umap;

	// inserting values by using [] operator
	umap["PI"] = 3.14;
	umap["root2"] = 1.414;
	umap["root3"] = 1.732;
	umap["log10"] = 2.302;
	umap["loge"] = 1.0;

	// inserting value by insert function
	umap.insert(make_pair("e", 2.718));

	string key = "PI";

	// If key not found in map iterator to end is returned
	if (umap.find(key) == umap.end())
		cout << key << " not found\n\n";

	// If key found then iterator to that key is returned
	else
		cout << "Found " << key << "\n\n";

	key = "lambda";
	if (umap.find(key) == umap.end())
		cout << key << " not found\n";
	else
		cout << "Found " << key << endl;

	// iterating over all value of umap
	unordered_map<string, double>:: iterator itr;
	cout << "\nAll Elements : \n";
	for (itr = umap.begin(); itr != umap.end(); itr++)
	{
		// itr works as a pointer to pair<string, double>
		// type itr->first stores the key part and
		// itr->second stroes the value part
		cout << itr->first << " " << itr->second << endl;
	}
}

```
**A practical problem based on unordered_map** – given a string of words, find frequencies of individual words.

```
Input :  str = "geeks for geeks geeks quiz practice qa for";
Output : Frequencies of individual words are
   (practice, 1)
   (for, 2)
   (qa, 1)
   (quiz, 1)
   (geeks, 3)
```
```cpp
// C++ program to find freq of every word using
// unordered_map
#include <bits/stdc++.h>
using namespace std;

// Prints frequencies of individual words in str
void printFrequencies(const string &str)
{
	// declaring map of <string, int> type, each word
	// is mapped to its frequency
	unordered_map<string, int> wordFreq;

	// breaking input into word using string stream
	stringstream ss(str); // Used for breaking words
	string word; // To store individual words
	while (ss >> word)
		wordFreq[word]++;

	// now iterating over word, freq pair and printing
	// them in <, > format
	unordered_map<string, int>:: iterator p;
	for (p = wordFreq.begin(); p != wordFreq.end(); p++)
		cout << "(" << p->first << ", " << p->second << ")\n";
}

// Driver code
int main()
{
	string str = "geeks for geeks geeks quiz "
				"practice qa for";
	printFrequencies(str);
	return 0;
}
```
