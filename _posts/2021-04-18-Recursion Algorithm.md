---
published: true
---
![Benjamin Bannekat](https://raw.githubusercontent.com/hamid-abbaszadeh/hamid-abbaszadeh.github.io/master/images/blog.png)
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome file</title>
  <link rel="stylesheet" href="https://stackedit.io/style.css" />
</head>

<body class="stackedit">
  <div class="stackedit__html"><h1 id="recursion">Recursion</h1>
<blockquote>
<p><strong>What is Recursion?</strong><br>
The process in which a function calls itself directly or indirectly is called recursion and the corresponding function is called as recursive function. Using recursive algorithm, certain problems can be solved quite easily.</p>
</blockquote>
<blockquote>
<p><strong>How memory is allocated to different function calls in recursion?</strong><br>
When any function is called from main(), the memory is allocated to it on the <strong>stack</strong>. A recursive function calls itself, the memory for a called function is allocated on top of memory allocated to calling function and different copy of local variables is created for each function call. When the base case is reached, the function returns its value to the function by whom it is called and memory is de-allocated and the process continues.<br>
Let us take the example how recursion works by taking a simple function.</p>
</blockquote>
<p><strong>C++ Program to print an Array using Recursion</strong></p>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">// C++ Program to print</span>
<span class="token comment">// an Array using Recursion</span>

<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;bits/stdc++.h&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token comment">// Recursive function to print the array</span>
<span class="token keyword">void</span> <span class="token function">print_array</span><span class="token punctuation">(</span><span class="token keyword">int</span> arr<span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token keyword">int</span> size<span class="token punctuation">,</span> <span class="token keyword">int</span> i<span class="token punctuation">)</span>
<span class="token punctuation">{</span>

	<span class="token comment">// base case</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>i <span class="token operator">==</span> size<span class="token punctuation">)</span> <span class="token punctuation">{</span>
		cout <span class="token operator">&lt;&lt;</span> endl<span class="token punctuation">;</span>
		<span class="token keyword">return</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>

	<span class="token comment">// print the ith element</span>
	cout <span class="token operator">&lt;&lt;</span> arr<span class="token punctuation">[</span>i<span class="token punctuation">]</span> <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>
	i<span class="token operator">++</span><span class="token punctuation">;</span>

	<span class="token comment">// recursive call</span>
	<span class="token function">print_array</span><span class="token punctuation">(</span>arr<span class="token punctuation">,</span> size<span class="token punctuation">,</span> i<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// Driver code</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>

	<span class="token keyword">int</span> arr<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">{</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token number">5</span><span class="token punctuation">,</span> <span class="token number">6</span><span class="token punctuation">,</span> <span class="token number">8</span><span class="token punctuation">,</span> <span class="token number">1</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
	<span class="token keyword">int</span> n <span class="token operator">=</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span>arr<span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span>arr<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token function">print_array</span><span class="token punctuation">(</span>arr<span class="token punctuation">,</span> n<span class="token punctuation">,</span> <span class="token number">0</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>


</code></pre>
<p><strong>Sum of array elements using recursion</strong></p>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">// C++ program to demonstrate functionality of unordered_map</span>
<span class="token comment">// C++ program to find sum of array</span>
<span class="token comment">// elements using recursion.</span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;stdio.h&gt;</span></span>

<span class="token comment">// Return sum of elements in A[0..N-1]</span>
<span class="token comment">// using recursion.</span>
<span class="token keyword">int</span> <span class="token function">findSum</span><span class="token punctuation">(</span><span class="token keyword">int</span> A<span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token keyword">int</span> N<span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>N <span class="token operator">&lt;=</span> <span class="token number">0</span><span class="token punctuation">)</span>
		<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> <span class="token punctuation">(</span><span class="token function">findSum</span><span class="token punctuation">(</span>A<span class="token punctuation">,</span> N <span class="token operator">-</span> <span class="token number">1</span><span class="token punctuation">)</span> <span class="token operator">+</span> A<span class="token punctuation">[</span>N <span class="token operator">-</span> <span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// Driver code</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">int</span> A<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">{</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">,</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token number">4</span><span class="token punctuation">,</span> <span class="token number">5</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
	<span class="token keyword">int</span> N <span class="token operator">=</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span>A<span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token keyword">sizeof</span><span class="token punctuation">(</span>A<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token function">printf</span><span class="token punctuation">(</span><span class="token string">"%dn"</span><span class="token punctuation">,</span> <span class="token function">findSum</span><span class="token punctuation">(</span>A<span class="token punctuation">,</span> N<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre>
<p><strong>First uppercase letter in a string (Iterative and Recursive)</strong></p>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">// C++ program to find the</span>
<span class="token comment">// first uppercase letter.</span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;bits/stdc++.h&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token comment">// Function to find string which has</span>
<span class="token comment">// first character of each word.</span>
<span class="token keyword">char</span> <span class="token function">first</span><span class="token punctuation">(</span>string str<span class="token punctuation">,</span> <span class="token keyword">int</span> i<span class="token operator">=</span><span class="token number">0</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>str<span class="token punctuation">[</span>i<span class="token punctuation">]</span> <span class="token operator">==</span> <span class="token string">'\0'</span><span class="token punctuation">)</span>
		<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token function">isupper</span><span class="token punctuation">(</span>str<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
			<span class="token keyword">return</span> str<span class="token punctuation">[</span>i<span class="token punctuation">]</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> <span class="token function">first</span><span class="token punctuation">(</span>str<span class="token punctuation">,</span> i<span class="token operator">+</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// Driver code</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	string str <span class="token operator">=</span> <span class="token string">"geeksforGeeKS"</span><span class="token punctuation">;</span>
	<span class="token keyword">char</span> res <span class="token operator">=</span> <span class="token function">first</span><span class="token punctuation">(</span>str<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>res <span class="token operator">==</span> <span class="token number">0</span><span class="token punctuation">)</span>
		cout <span class="token operator">&lt;&lt;</span> <span class="token string">"No uppercase letter"</span><span class="token punctuation">;</span>
	<span class="token keyword">else</span>
		cout <span class="token operator">&lt;&lt;</span> res <span class="token operator">&lt;&lt;</span> <span class="token string">"\n"</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre>
<p><strong>Print a pattern without using any loop</strong></p>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">// C++ program to print pattern that first reduces 5 one</span>
<span class="token comment">// by one, then adds 5. Without any loop an extra variable.</span>
<span class="token macro property">#<span class="token directive keyword">include</span> <span class="token string">&lt;iostream&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token comment">// Recursive function to print the pattern without any extra</span>
<span class="token comment">// variable</span>
<span class="token keyword">void</span> <span class="token function">printPattern</span><span class="token punctuation">(</span><span class="token keyword">int</span> n<span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token comment">// Base case (When n becomes 0 or negative)</span>
	<span class="token keyword">if</span> <span class="token punctuation">(</span>n <span class="token operator">==</span><span class="token number">0</span> <span class="token operator">||</span> n<span class="token operator">&lt;</span><span class="token number">0</span><span class="token punctuation">)</span>
	<span class="token punctuation">{</span>
		cout <span class="token operator">&lt;&lt;</span> n <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>
		<span class="token keyword">return</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
	
	<span class="token comment">// First print decreasing order</span>
	cout <span class="token operator">&lt;&lt;</span> n <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>
	<span class="token function">printPattern</span><span class="token punctuation">(</span>n<span class="token number">-5</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token comment">// Then print increasing order</span>
	cout <span class="token operator">&lt;&lt;</span> n <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// Driver Program</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	<span class="token keyword">int</span> n <span class="token operator">=</span> <span class="token number">16</span><span class="token punctuation">;</span>
	<span class="token function">printPattern</span><span class="token punctuation">(</span>n<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre>
<p><strong>What is the difference between direct and indirect recursion?</strong><br>
A function fun is called direct recursive if it calls the same function fun. A function fun is called indirect recursive if it calls another function say fun_new and fun_new calls fun directly or indirectly. Difference between direct and indirect recursion has been illustrated in Table 1.</p>
<p><strong>An example of direct recursion</strong></p>
<pre><code>void directRecFun()
{
    // Some code....

    directRecFun();

    // Some code...
}
</code></pre>
<p><strong>An example of indirect recursion</strong></p>
<pre><code>void indirectRecFun1()
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
</code></pre>
<p><strong>How memory is allocated to different function calls in recursion?</strong><br>
When any function is called from main(), the memory is allocated to it on the stack. A recursive function calls itself, the memory for a called function is allocated on top of memory allocated to calling function and different copy of local variables is created for each function call. When the base case is reached, the function returns its value to the function by whom it is called and memory is de-allocated and the process continues.<br>
Let us take the example how recursion works by taking a simple function.</p>
<p><strong>What are the advantages of recursive programming over iterative programming?</strong><br>
Recursion provides a <strong>clean and simple way to write code</strong>. Some problems are inherently recursive like tree traversals. For such problems, it is preferred to write recursive code. We can write such codes also iteratively with the help of a stack data structure.</p>
<p><strong>Inorder Tree Traversal without Recursion</strong></p>
<p>Using  [Stack] is the obvious way to traverse tree without recursion. Below is an algorithm for traversing binary tree using stack. See this for step wise step execution of the algorithm.</p>
<pre><code>1) Create an empty stack S.
2) Initialize current node as root
3) Push the current node to S and set current = current-&gt;left until current is NULL
4) If current is NULL and stack is not empty then 
     a) Pop the top item from stack.
     b) Print the popped item, set current = popped_item-&gt;right 
     c) Go to step 3.
5) If current is NULL and stack is empty then we are done.
</code></pre>
<p>Let us consider the below tree for example</p>
<pre><code>        1
      /   \
    2      3
  /  \
4     5
</code></pre>
<p>Step 1 Creates an empty stack: S = NULL</p>
<p>Step 2 sets current as address of root: current -&gt; 1</p>
<p>Step 3 Pushes the current node and set current = current-&gt;left<br>
until current is NULL<br>
current -&gt; 1<br>
push 1: Stack S -&gt; 1<br>
current -&gt; 2<br>
push 2: Stack S -&gt; 2, 1<br>
current -&gt; 4<br>
push 4: Stack S -&gt; 4, 2, 1<br>
current = NULL</p>
<p>Step 4 pops from S<br>
a) Pop 4: Stack S -&gt; 2, 1<br>
b) print “4”<br>
c) current = NULL /*right of 4 */ and go to step 3<br>
Since current is NULL step 3 doesn’t do anything.</p>
<p>Step 4 pops again.<br>
a) Pop 2: Stack S -&gt; 1<br>
b) print “2”<br>
c) current -&gt; 5/*right of 2 */ and go to step 3</p>
<p>Step 3 pushes 5 to stack and makes current NULL<br>
Stack S -&gt; 5, 1<br>
current = NULL</p>
<p>Step 4 pops from S<br>
a) Pop 5: Stack S -&gt; 1<br>
b) print “5”<br>
c) current = NULL /*right of 5 */ and go to step 3<br>
Since current is NULL step 3 doesn’t do anything</p>
<p>Step 4 pops again.<br>
a) Pop 1: Stack S -&gt; NULL<br>
b) print “1”<br>
c) current -&gt; 3 /*right of 1 */</p>
<p>Step 3 pushes 3 to stack and makes current NULL<br>
Stack S -&gt; 3<br>
current = NULL</p>
<p>Step 4 pops from S<br>
a) Pop 3: Stack S -&gt; NULL<br>
b) print “3”<br>
c) current = NULL /*right of 3 */</p>
<p>Traversal is done now as stack S is empty and current is NULL.</p>
<pre class=" language-cpp"><code class="prism  language-cpp"><span class="token comment">// C++ program to print inorder traversal</span>
<span class="token comment">// using stack.</span>
<span class="token macro property">#<span class="token directive keyword">include</span><span class="token string">&lt;bits/stdc++.h&gt;</span></span>
<span class="token keyword">using</span> <span class="token keyword">namespace</span> std<span class="token punctuation">;</span>

<span class="token comment">/* A binary tree Node has data, pointer to left child
and a pointer to right child */</span>
<span class="token keyword">struct</span> Node
<span class="token punctuation">{</span>
	<span class="token keyword">int</span> data<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> Node<span class="token operator">*</span> left<span class="token punctuation">;</span>
	<span class="token keyword">struct</span> Node<span class="token operator">*</span> right<span class="token punctuation">;</span>
	<span class="token function">Node</span> <span class="token punctuation">(</span><span class="token keyword">int</span> data<span class="token punctuation">)</span>
	<span class="token punctuation">{</span>
		<span class="token keyword">this</span><span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">=</span> data<span class="token punctuation">;</span>
		left <span class="token operator">=</span> right <span class="token operator">=</span> <span class="token constant">NULL</span><span class="token punctuation">;</span>
	<span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>

<span class="token comment">/* Iterative function for inorder tree
traversal */</span>
<span class="token keyword">void</span> <span class="token function">inOrder</span><span class="token punctuation">(</span><span class="token keyword">struct</span> Node <span class="token operator">*</span>root<span class="token punctuation">)</span>
<span class="token punctuation">{</span>
	stack<span class="token operator">&lt;</span>Node <span class="token operator">*</span><span class="token operator">&gt;</span> s<span class="token punctuation">;</span>
	Node <span class="token operator">*</span>curr <span class="token operator">=</span> root<span class="token punctuation">;</span>

	<span class="token keyword">while</span> <span class="token punctuation">(</span>curr <span class="token operator">!=</span> <span class="token constant">NULL</span> <span class="token operator">||</span> s<span class="token punctuation">.</span><span class="token function">empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">==</span> <span class="token boolean">false</span><span class="token punctuation">)</span>
	<span class="token punctuation">{</span>
		<span class="token comment">/* Reach the left most Node of the
		curr Node */</span>
		<span class="token keyword">while</span> <span class="token punctuation">(</span>curr <span class="token operator">!=</span> <span class="token constant">NULL</span><span class="token punctuation">)</span>
		<span class="token punctuation">{</span>
			<span class="token comment">/* place pointer to a tree node on
			the stack before traversing
			the node's left subtree */</span>
			s<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span>curr<span class="token punctuation">)</span><span class="token punctuation">;</span>
			curr <span class="token operator">=</span> curr<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token punctuation">;</span>
		<span class="token punctuation">}</span>

		<span class="token comment">/* Current must be NULL at this point */</span>
		curr <span class="token operator">=</span> s<span class="token punctuation">.</span><span class="token function">top</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
		s<span class="token punctuation">.</span><span class="token function">pop</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

		cout <span class="token operator">&lt;&lt;</span> curr<span class="token operator">-</span><span class="token operator">&gt;</span>data <span class="token operator">&lt;&lt;</span> <span class="token string">" "</span><span class="token punctuation">;</span>

		<span class="token comment">/* we have visited the node and its
		left subtree. Now, it's right
		subtree's turn */</span>
		curr <span class="token operator">=</span> curr<span class="token operator">-</span><span class="token operator">&gt;</span>right<span class="token punctuation">;</span>

	<span class="token punctuation">}</span> <span class="token comment">/* end of while */</span>
<span class="token punctuation">}</span>

<span class="token comment">/* Driver program to test above functions*/</span>
<span class="token keyword">int</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">{</span>

	<span class="token comment">/* Constructed binary tree is
			1
			/ \
		2	 3
		/ \
	4	 5
	*/</span>
	<span class="token keyword">struct</span> Node <span class="token operator">*</span>root <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left	 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>right	 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>left <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">4</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
	root<span class="token operator">-</span><span class="token operator">&gt;</span>left<span class="token operator">-</span><span class="token operator">&gt;</span>right <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token function">Node</span><span class="token punctuation">(</span><span class="token number">5</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

	<span class="token function">inOrder</span><span class="token punctuation">(</span>root<span class="token punctuation">)</span><span class="token punctuation">;</span>
	<span class="token keyword">return</span> <span class="token number">0</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre>
<p><strong>Output:</strong></p>
<pre><code> 4 2 5 1 3
</code></pre>
</div>
</body>

</html>
