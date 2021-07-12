---
published: true
---
[![Benjamin Bannekat](https://raw.githubusercontent.com/hamid-abbaszadeh/hamid-abbaszadeh.github.io/master/images/post13.jpg)](https://hamid-abbaszadeh.github.io/Recursion-Algorithm/)
# Recursion 
>**What is Recursion?**  
The process in which a function calls itself directly or indirectly is called recursion and the corresponding function is called as recursive function. Using recursive algorithm, certain problems can be solved quite easily.


>**How memory is allocated to different function calls in recursion?**  
When any function is called from main(), the memory is allocated to it on the **stack**. A recursive function calls itself, the memory for a called function is allocated on top of memory allocated to calling function and different copy of local variables is created for each function call. When the base case is reached, the function returns its value to the function by whom it is called and memory is de-allocated and the process continues.  
Let us take the example how recursion works by taking a simple function.


**C++ Program to print an Array using Recursion**

```cpp
// C++ Program to print
// an Array using Recursion

#include <bits/stdc++.h>
using namespace std;

// Recursive function to print the array
void print_array(int arr[], int size, int i)
{

	// base case
	if (i == size) {
		cout << endl;
		return;
	}

	// print the ith element
	cout << arr[i] << " ";
	i++;

	// recursive call
	print_array(arr, size, i);
}

// Driver code
int main()
{

	int arr[] = { 3, 5, 6, 8, 1 };
	int n = sizeof(arr) / sizeof(arr[0]);

	print_array(arr, n, 0);

	return 0;
}


```

**Sum of array elements using recursion**

```cpp
// C++ program to demonstrate functionality of unordered_map
// C++ program to find sum of array
// elements using recursion.
#include <stdio.h>

// Return sum of elements in A[0..N-1]
// using recursion.
int findSum(int A[], int N)
{
	if (N <= 0)
		return 0;
	return (findSum(A, N - 1) + A[N - 1]);
}

// Driver code
int main()
{
	int A[] = { 1, 2, 3, 4, 5 };
	int N = sizeof(A) / sizeof(A[0]);
	printf("%dn", findSum(A, N));
	return 0;
}
```
**First uppercase letter in a string (Iterative and Recursive)**

```cpp
// C++ program to find the
// first uppercase letter.
#include <bits/stdc++.h>
using namespace std;

// Function to find string which has
// first character of each word.
char first(string str, int i=0)
{
	if (str[i] == '\0')
		return 0;
	if (isupper(str[i]))
			return str[i];
	return first(str, i+1);
}

// Driver code
int main()
{
	string str = "geeksforGeeKS";
	char res = first(str);
	if (res == 0)
		cout << "No uppercase letter";
	else
		cout << res << "\n";
	return 0;
}
```
**Print a pattern without using any loop**
```cpp
// C++ program to print pattern that first reduces 5 one
// by one, then adds 5. Without any loop an extra variable.
#include <iostream>
using namespace std;

// Recursive function to print the pattern without any extra
// variable
void printPattern(int n)
{
	// Base case (When n becomes 0 or negative)
	if (n ==0 || n<0)
	{
		cout << n << " ";
		return;
	}
	
	// First print decreasing order
	cout << n << " ";
	printPattern(n-5);

	// Then print increasing order
	cout << n << " ";
}

// Driver Program
int main()
{
	int n = 16;
	printPattern(n);
	return 0;
}
```

**What is the difference between direct and indirect recursion?**  
A function fun is called direct recursive if it calls the same function fun. A function fun is called indirect recursive if it calls another function say fun_new and fun_new calls fun directly or indirectly. Difference between direct and indirect recursion has been illustrated in Table 1.

**An example of direct recursion**
```
void directRecFun()
{
    // Some code....

    directRecFun();

    // Some code...
}
```
**An example of indirect recursion**
```
void indirectRecFun1()
{
    // Some code...

    indirectRecFun2();

    // Some code...
}

void indirectRecFun2()
{
    // Some code...

    indirectRecFun1();

    // Some code...
}
```
**How memory is allocated to different function calls in recursion?**  
When any function is called from main(), the memory is allocated to it on the stack. A recursive function calls itself, the memory for a called function is allocated on top of memory allocated to calling function and different copy of local variables is created for each function call. When the base case is reached, the function returns its value to the function by whom it is called and memory is de-allocated and the process continues.  
Let us take the example how recursion works by taking a simple function.

**What are the advantages of recursive programming over iterative programming?**  
Recursion provides a **clean and simple way to write code**. Some problems are inherently recursive like tree traversals. For such problems, it is preferred to write recursive code. We can write such codes also iteratively with the help of a stack data structure.

**Inorder Tree Traversal without Recursion**



Using  [Stack] is the obvious way to traverse tree without recursion. Below is an algorithm for traversing binary tree using stack. See this for step wise step execution of the algorithm.
```
1) Create an empty stack S.
2) Initialize current node as root
3) Push the current node to S and set current = current->left until current is NULL
4) If current is NULL and stack is not empty then 
     a) Pop the top item from stack.
     b) Print the popped item, set current = popped_item->right 
     c) Go to step 3.
5) If current is NULL and stack is empty then we are done.
```

Let us consider the below tree for example

            1
          /   \
        2      3
      /  \
    4     5

Step 1 Creates an empty stack: S = NULL

Step 2 sets current as address of root: current -> 1

Step 3 Pushes the current node and set current = current->left 
       until current is NULL
     current -> 1
     push 1: Stack S -> 1
     current -> 2
     push 2: Stack S -> 2, 1
     current -> 4
     push 4: Stack S -> 4, 2, 1
     current = NULL

Step 4 pops from S
     a) Pop 4: Stack S -> 2, 1
     b) print "4"
     c) current = NULL /*right of 4 */ and go to step 3
Since current is NULL step 3 doesn't do anything. 

Step 4 pops again.
     a) Pop 2: Stack S -> 1
     b) print "2"
     c) current -> 5/*right of 2 */ and go to step 3

Step 3 pushes 5 to stack and makes current NULL
     Stack S -> 5, 1
     current = NULL

Step 4 pops from S
     a) Pop 5: Stack S -> 1
     b) print "5"
     c) current = NULL /*right of 5 */ and go to step 3
Since current is NULL step 3 doesn't do anything

Step 4 pops again.
     a) Pop 1: Stack S -> NULL
     b) print "1"
     c) current -> 3 /*right of 1 */  

Step 3 pushes 3 to stack and makes current NULL
     Stack S -> 3
     current = NULL

Step 4 pops from S
     a) Pop 3: Stack S -> NULL
     b) print "3"
     c) current = NULL /*right of 3 */  

Traversal is done now as stack S is empty and current is NULL.

```cpp
// C++ program to print inorder traversal
// using stack.
#include<bits/stdc++.h>
using namespace std;

/* A binary tree Node has data, pointer to left child
and a pointer to right child */
struct Node
{
	int data;
	struct Node* left;
	struct Node* right;
	Node (int data)
	{
		this->data = data;
		left = right = NULL;
	}
};

/* Iterative function for inorder tree
traversal */
void inOrder(struct Node *root)
{
	stack<Node *> s;
	Node *curr = root;

	while (curr != NULL || s.empty() == false)
	{
		/* Reach the left most Node of the
		curr Node */
		while (curr != NULL)
		{
			/* place pointer to a tree node on
			the stack before traversing
			the node's left subtree */
			s.push(curr);
			curr = curr->left;
		}

		/* Current must be NULL at this point */
		curr = s.top();
		s.pop();

		cout << curr->data << " ";

		/* we have visited the node and its
		left subtree. Now, it's right
		subtree's turn */
		curr = curr->right;

	} /* end of while */
}

/* Driver program to test above functions*/
int main()
{

	/* Constructed binary tree is
			1
			/ \
		2	 3
		/ \
	4	 5
	*/
	struct Node *root = new Node(1);
	root->left	 = new Node(2);
	root->right	 = new Node(3);
	root->left->left = new Node(4);
	root->left->right = new Node(5);

	inOrder(root);
	return 0;
}
```
**Output:**
```
 4 2 5 1 3
 ```
