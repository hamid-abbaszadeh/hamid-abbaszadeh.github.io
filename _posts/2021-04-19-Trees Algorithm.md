---
published: false
---

<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome file</title>
  <link rel="stylesheet" href="https://stackedit.io/style.css" />
</head>

<body class="stackedit">
  <div class="stackedit__html"><h1 id="trees-in-c">Trees in C++</h1>
<blockquote>
<p><strong>What is Binary Tree?</strong><br>
A tree whose elements have <strong>at most 2 children</strong> is called a binary tree. Since each element in a binary tree can have only 2 children, we typically name them the left and right child.</p>
</blockquote>
<p><strong>Binary Tree Representation in C/C++:</strong><br>
A tree is represented by a pointer to the topmost node in tree. If the tree is empty, then value of root is NULL.<br>
A Tree node contains following parts.</p>
<blockquote>
<ol>
<li>Data</li>
<li>Pointer to left child</li>
<li>Pointer to right child</li>
</ol>
</blockquote>
<p>In C/C++, we can represent a tree node using structures. Below is an example of a tree node with an integer data.</p>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token keyword">struct</span> node
<span class="token punctuation">{</span>
	<span class="token keyword">int</span> data<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> node<span class="token operator">*</span> left<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> node<span class="token operator">*</span> right<span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre>
<blockquote>
<p><strong>Main applications of trees include:</strong><br>
<strong>1.</strong> Manipulate hierarchical data.<br>
<strong>2.</strong> Make information <strong>easy to search</strong> (see tree traversal).<br>
<strong>3.</strong> Manipulate sorted lists of data.<br>
<strong>4.</strong> As a workflow for compositing digital images for visual effects.<br>
<strong>5.</strong> Router algorithms<br>
<strong>6.</strong> Form of a multi-stage <strong>decision-making</strong> (see business chess).</p>
</blockquote>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;bits/stdc++.h&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token keyword">struct</span> Node <span class="token punctuation">{</span>
	<span class="token keyword">int</span> data<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> Node<span class="token operator">*</span> left<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> Node<span class="token operator">*</span> right<span class="token punctuation">;</span>

	<span class="token comment">// val is the key or the value that</span>
	<span class="token comment">// has to be added to the data part</span>
	<span class="token function">Node</span><span class="token punctuation">(</span><span class="token keyword">int</span> val<span class="token punctuation">)</span>
	<span class="token punctuation">{</span>
		data <span class="token operator">=</span> val<span class="token punctuation">;</span>

		<span class="token comment">// Left and right child for node</span>
		<span class="token comment">// will be initialized to null</span>
		left <span class="token operator">=</span> <span class="token constant">NULL</span><span class="token punctuation">;</span>
		right <span class="token operator">=</span> <span class="token constant">NULL</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>

<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>

	<span class="token comment">/*create root*/</span>
	<span class="token keyword">struct</span> Node<span class="token operator">*</span> root <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token comment">/* following is the tree after above statement

			1
			/ \
		NULL NULL
	*/</span>

	root<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token comment">/* 2 and 3 become left and right children of 1
					1
				/ \
				2	 3
			/ \	 / \
			NULL NULL NULL NULL
	*/</span>

	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token comment">/* 4 becomes left child of 2
			1
			/	 \
		2	 3
		/ \	 / \
		4 NULL NULL NULL
		/ \
	NULL NULL
	*/</span>

	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

</code></pre>
<h1 id="tree-traversals-algorithm.">Tree Traversals Algorithm.</h1>
<blockquote>
<p>Unlike linear data structures (Array, Linked List, Queues, Stacks, etc) which have only one logical way to traverse them, trees can be traversed in different ways.</p>
</blockquote>
<p><img src="https://media.geeksforgeeks.org/wp-content/cdn-uploads/level_order_traversal.png" alt="Example Tree"></p>
<h2 id="depth-first-traversals-dfs-algorithm">Depth First Traversals (DFS) Algorithm</h2>
<p>(a) Inorder (Left, Root, Right) : 4 2 5 1 3</p>
<blockquote>
<p>Uses of Inorder<br>
In case of binary search trees (BST), Inorder traversal gives nodes in non-decreasing order. To get nodes of BST in non-increasing order, a variation of Inorder traversal where Inorder traversal s reversed can be used.</p>
</blockquote>
<p>(b) Preorder (Root, Left, Right) : 1 2 4 5 3</p>
<blockquote>
<p>Uses of Preorder<br>
Preorder traversal is used to create a copy of the tree. Preorder traversal is also used to get prefix expression on of an expression tree.</p>
</blockquote>
<p>© Postorder (Left, Right, Root) : 4 5 2 3 1</p>
<blockquote>
<p>Uses of Preorder<br>
Preorder traversal is used to create a copy of the tree. Preorder traversal is also used to get prefix expression on of an expression tree.</p>
</blockquote>
<pre><code>Algorithm Inorder(tree)
   1. Traverse the left subtree, i.e., call Inorder(left-subtree)
   2. Visit the root.
   3. Traverse the right subtree, i.e., call Inorder(right-subtree)
</code></pre>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">// C++ program for different tree traversals</span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;iostream&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token comment">/* A binary tree node has data, pointer to left child
and a pointer to right child */</span>


<span class="token keyword">struct</span> Node <span class="token punctuation">{</span>
	<span class="token keyword">int</span> data<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> Node <span class="token operator">*</span>left<span class="token punctuation">,</span> <span class="token operator">*</span>right<span class="token punctuation">;</span>
	<span class="token function">Node</span><span class="token punctuation">(</span><span class="token keyword">int</span> data<span class="token punctuation">)</span>
	<span class="token punctuation">{</span>
		<span class="token keyword">this</span><span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">=</span> data<span class="token punctuation">;</span>
		left <span class="token operator">=</span> right <span class="token operator">=</span> <span class="token constant">NULL</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>


<span class="token comment">/* Given a binary tree, print its nodes in inorder*/</span>
<span class="token keyword">void</span> <span class="token function">printInorder</span><span class="token punctuation">(</span><span class="token keyword">struct</span> Node<span class="token operator">*</span> node<span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>node <span class="token operator">==</span> <span class="token constant">NULL</span><span class="token punctuation">)</span>
		<span class="token keyword">return</span><span class="token punctuation">;</span>

	<span class="token comment">/* first recur on left child */</span>
	<span class="token function">printInorder</span><span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">/* then print the data of node */</span>
	cout <span class="token operator">&lt;&lt;</span> node<span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>

	<span class="token comment">/* now recur on right child */</span>
	<span class="token function">printInorder</span><span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>right<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>


<span class="token comment">/* Driver program to test above functions*/</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">struct</span> Node<span class="token operator">*</span> root <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">5</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	cout <span class="token operator">&lt;&lt;</span> <span class="token string">"\nInorder traversal of binary tree is \n"</span><span class="token punctuation">;</span>
	<span class="token function">printInorder</span><span class="token punctuation">(</span>root<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre>
<pre><code>Algorithm Preorder(tree)
   1. Visit the root.
   2. Traverse the left subtree, i.e., call Preorder(left-subtree)
   3. Traverse the right subtree, i.e., call Preorder(right-subtree)
</code></pre>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">// C++ program for different tree traversals</span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;iostream&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token comment">/* A binary tree node has data, pointer to left child
and a pointer to right child */</span>

<span class="token keyword">struct</span> Node <span class="token punctuation">{</span>
	<span class="token keyword">int</span> data<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> Node <span class="token operator">*</span>left<span class="token punctuation">,</span> <span class="token operator">*</span>right<span class="token punctuation">;</span>
	<span class="token function">Node</span><span class="token punctuation">(</span><span class="token keyword">int</span> data<span class="token punctuation">)</span>
	<span class="token punctuation">{</span>
		<span class="token keyword">this</span><span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">=</span> data<span class="token punctuation">;</span>
		left <span class="token operator">=</span> right <span class="token operator">=</span> <span class="token constant">NULL</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>


<span class="token comment">/* Given a binary tree, print its nodes in preorder*/</span>
<span class="token keyword">void</span> <span class="token function">printPreorder</span><span class="token punctuation">(</span><span class="token keyword">struct</span> Node<span class="token operator">*</span> node<span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>node <span class="token operator">==</span> <span class="token constant">NULL</span><span class="token punctuation">)</span>
		<span class="token keyword">return</span><span class="token punctuation">;</span>

	<span class="token comment">/* first print data of node */</span>
	cout <span class="token operator">&lt;&lt;</span> node<span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>

	<span class="token comment">/* then recur on left sutree */</span>
	<span class="token function">printPreorder</span><span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">/* now recur on right subtree */</span>
	<span class="token function">printPreorder</span><span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>right<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">/* Driver program to test above functions*/</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">struct</span> Node<span class="token operator">*</span> root <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">5</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	cout <span class="token operator">&lt;&lt;</span> <span class="token string">"\nPreorder traversal of binary tree is \n"</span><span class="token punctuation">;</span>
	<span class="token function">printPreorder</span><span class="token punctuation">(</span>root<span class="token punctuation">)</span><span class="token punctuation">;</span>


	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre>
<pre><code>Algorithm Postorder(tree)
   1. Traverse the left subtree, i.e., call Postorder(left-subtree)
   2. Traverse the right subtree, i.e., call Postorder(right-subtree)
   3. Visit the root.
</code></pre>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">// C++ program for different tree traversals</span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;iostream&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token comment">/* A binary tree node has data, pointer to left child
and a pointer to right child */</span>

<span class="token keyword">struct</span> Node <span class="token punctuation">{</span>
	<span class="token keyword">int</span> data<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> Node <span class="token operator">*</span>left<span class="token punctuation">,</span> <span class="token operator">*</span>right<span class="token punctuation">;</span>
	<span class="token function">Node</span><span class="token punctuation">(</span><span class="token keyword">int</span> data<span class="token punctuation">)</span>
	<span class="token punctuation">{</span>
		<span class="token keyword">this</span><span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">=</span> data<span class="token punctuation">;</span>
		left <span class="token operator">=</span> right <span class="token operator">=</span> <span class="token constant">NULL</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>

<span class="token comment">/* Given a binary tree, print its nodes according to the
"bottom-up" postorder traversal. */</span>

<span class="token keyword">void</span> <span class="token function">printPostorder</span><span class="token punctuation">(</span><span class="token keyword">struct</span> Node<span class="token operator">*</span> node<span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>node <span class="token operator">==</span> <span class="token constant">NULL</span><span class="token punctuation">)</span>
		<span class="token keyword">return</span><span class="token punctuation">;</span>

	<span class="token comment">// first recur on left subtree</span>
	<span class="token function">printPostorder</span><span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">// then recur on right subtree</span>
	<span class="token function">printPostorder</span><span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>right<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">// now deal with the node</span>
	cout <span class="token operator">&lt;&lt;</span> node<span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">/* Driver program to test above functions*/</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">struct</span> Node<span class="token operator">*</span> root <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">5</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	cout <span class="token operator">&lt;&lt;</span> <span class="token string">"\nPostorder traversal of binary tree is \n"</span><span class="token punctuation">;</span>
	<span class="token function">printPostorder</span><span class="token punctuation">(</span>root<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

</code></pre>
<h2 id="breadth-first-or-level-order-traversal-bfs-algorithm">Breadth First or Level Order Traversal (BFS) Algorithm</h2>
<p><strong>Breadth First Traversal:</strong><br>
1 2 3 4 5</p>
<p><strong>Implementation Algorithm:</strong></p>
<pre class=" language-printlevelorder"><code class="prism (tree) language-printlevelorder">1) Create an empty queue q
2) temp_node = root /*start from root*/
3) Loop while temp_node is not NULL
    a) print temp_node-&gt;data.
    b) Enqueue temp_node’s children 
      (first left then right children) to q
    c) Dequeue a node from q.
</code></pre>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">/* C++ program to print level
	order traversal using STL */</span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;bits/stdc++.h&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token comment">// A Binary Tree Node</span>
<span class="token keyword">struct</span> Node
<span class="token punctuation">{</span>
	<span class="token keyword">int</span> data<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> Node <span class="token operator">*</span>left<span class="token punctuation">,</span> <span class="token operator">*</span>right<span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>

<span class="token comment">// Iterative method to find height of Binary Tree</span>
<span class="token keyword">void</span> <span class="token function">printLevelOrder</span><span class="token punctuation">(</span>Node <span class="token operator">*</span>root<span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token comment">// Base Case</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>root <span class="token operator">==</span> <span class="token constant">NULL</span><span class="token punctuation">)</span> <span class="token keyword">return</span><span class="token punctuation">;</span>

	<span class="token comment">// Create an empty queue for level order traversal</span>
	queue<span class="token operator">&lt;</span>Node <span class="token operator">*</span><span class="token operator">&gt;</span> q<span class="token punctuation">;</span>

	<span class="token comment">// Enqueue Root and initialize height</span>
	q<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span>root<span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">while</span> <span class="token punctuation">(</span>q<span class="token punctuation">.</span><span class="token function">empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">==</span> <span class="token boolean">false</span><span class="token punctuation">)</span>
	<span class="token punctuation">{</span>
		<span class="token comment">// Print front of queue and remove it from queue</span>
		Node <span class="token operator">*</span>node <span class="token operator">=</span> q<span class="token punctuation">.</span><span class="token function">front</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
		cout <span class="token operator">&lt;&lt;</span> node<span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>
		q<span class="token punctuation">.</span><span class="token function">pop</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

		<span class="token comment">/* Enqueue left child */</span>
		<span class="token keyword">if</span> <span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">!=</span> <span class="token constant">NULL</span><span class="token punctuation">)</span>
			q<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token punctuation">)</span><span class="token punctuation">;</span>

		<span class="token comment">/*Enqueue right child */</span>
		<span class="token keyword">if</span> <span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">!=</span> <span class="token constant">NULL</span><span class="token punctuation">)</span>
			q<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span>node<span class="token operator">-</span><span class="token operator">&gt;</span>right<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// Utility function to create a new tree node</span>
Node<span class="token operator">*</span> <span class="token function">newNode</span><span class="token punctuation">(</span><span class="token keyword">int</span> data<span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	Node <span class="token operator">*</span>temp <span class="token operator">=</span> <span class="token keyword">new</span> Node<span class="token punctuation">;</span>
	temp<span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">=</span> data<span class="token punctuation">;</span>
	temp<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> temp<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token constant">NULL</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> temp<span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// Driver program to test above functions</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token comment">// Let us create binary tree shown in above diagram</span>
	Node <span class="token operator">*</span>root <span class="token operator">=</span> <span class="token function">newNode</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token function">newNode</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token function">newNode</span><span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token function">newNode</span><span class="token punctuation">(</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token function">newNode</span><span class="token punctuation">(</span><span class="token number">5</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	cout <span class="token operator">&lt;&lt;</span> <span class="token string">"Level Order traversal of binary tree is \n"</span><span class="token punctuation">;</span>
	<span class="token function">printLevelOrder</span><span class="token punctuation">(</span>root<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre>
<p><strong>Output</strong></p>
<pre><code>Level Order traversal of binary tree is 
1 2 3 4 5
</code></pre>
</div>
</body>

</html>

