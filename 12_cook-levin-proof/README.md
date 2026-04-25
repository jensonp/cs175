# The Cook-Levin Proof: Why SAT Captures All of NP

The Cook-Levin theorem is one of the central results in theoretical computer science because it gives the first complete problem for the class NP. It says that the Boolean satisfiability problem, usually called SAT, is not merely one difficult problem among many. SAT is expressive enough to encode every computation whose correctness can be verified in polynomial time.

The proof is often remembered as a technical encoding: take a nondeterministic Turing machine, build a computation tableau, introduce Boolean variables for its cells, and write clauses saying that the tableau is legal. That description is accurate but incomplete. It tells us what the proof does, but not why those objects are introduced or why the construction works. The real idea is deeper and cleaner: a polynomial-time accepting computation has only polynomially many local facts, and each local fact can be forced by a Boolean formula of polynomial size. SAT is complete for NP because a satisfying assignment can serve as a certificate for an entire accepting computation history.

This chapter explains the Cook-Levin proof as a coherent argument. The goal is not to memorize a list of clauses, but to understand how the proof turns the dynamic process of computation into the static object of a Boolean formula.

---

# 1. Why the theorem matters

The theorem appears at the point where we have two ideas that need to be connected. On one side, NP is a class of decision problems whose yes-instances have efficiently checkable witnesses. On the other side, SAT is a concrete decision problem about whether a Boolean formula has a satisfying truth assignment. The gap is this: why should a problem about formulas have anything to do with arbitrary efficient verification procedures?

Cook-Levin fills that gap. It shows that every polynomial-time verification problem can be translated into one satisfiability question. The proof therefore explains why SAT can act as a universal language for NP computations.

## 1.1 The object being introduced: NP-completeness

Before we prove anything about SAT, we need to be clear about the role SAT is supposed to play. A problem being in NP means that yes-instances have short certificates whose correctness can be checked efficiently. A problem being NP-hard means that every problem in NP can be efficiently transformed into it. A problem being NP-complete means both are true: it is itself in NP, and it is at least as hard as every problem in NP under polynomial-time reductions.

The Cook-Levin proof establishes the NP-completeness of SAT. The hard part is NP-hardness: given any problem in NP, we must show how to encode its verification process as a Boolean formula.

### Formal definition: polynomial-time many-one reduction

Let $A$ and $B$ be decision problems over strings. We say that $A$ is polynomial-time many-one reducible to $B$, written

$$
A \leq_p B,
$$

if there is a function $f$ computable in polynomial time such that for every input string $x$,

$$
x \in A \quad \text{if and only if} \quad f(x) \in B.
$$

The function $f$ transforms instances of $A$ into instances of $B$ while preserving yes/no answers.

### Interpretation

A reduction is not just a translation of notation. It is a correctness-preserving transformation. If $x$ is a yes-instance of $A$, then $f(x)$ must be a yes-instance of $B$. If $x$ is a no-instance of $A$, then $f(x)$ must be a no-instance of $B$. The transformation is useful only because it is efficient: it cannot solve the hard part by doing exponential work before producing the new instance.

For Cook-Levin, $B$ is SAT. The reduction must take an input $w$ to some language $L \in NP$ and produce a Boolean formula $\Phi_{M,w}$ such that

$$
\Phi_{M,w} \text{ is satisfiable} \quad \text{if and only if} \quad M \text{ accepts } w
$$

for a suitable nondeterministic polynomial-time Turing machine $M$ deciding $L$.

### Assumptions and boundary conditions

The reduction must be uniform. It is not allowed to invent a different proof idea for each input. Once the machine $M$ is fixed, the construction must mechanically build the formula from $w$ in polynomial time.

The reduction also must preserve both directions of truth. A common mistake is to show only that an accepting computation gives a satisfying assignment. That direction proves that the formula is satisfiable when the machine accepts. It does not prove that every satisfying assignment corresponds to a legal accepting computation. Cook-Levin requires both directions.

### Worked example: what a reduction claim really says

Suppose $L$ is a language in NP, and suppose $M$ is a nondeterministic machine deciding $L$ in time at most $p(n)$, where $p$ is a polynomial and $n = |w|$. For a particular input $w$, the reduction produces a formula $\Phi_{M,w}$.

The formula is not supposed to describe every possible input to $M$. It describes possible computations of this fixed machine on this fixed input $w$. The input $w$ becomes hardwired into the formula. The machine $M$ is fixed by the language $L$, and the varying object is the string $w$.

The proof then checks two claims.

First, if $w \in L$, then $M$ has at least one accepting computation path on $w$. That accepting path can be written as a finite computation history. From that history, we assign truth values to the variables of $\Phi_{M,w}$ so that every clause is satisfied.

Second, if $\Phi_{M,w}$ is satisfiable, then the satisfying assignment describes a computation history. The clauses are designed so that this history cannot be arbitrary: it must start with $M$ on input $w$, evolve according to $M$'s transition relation, and reach an accepting state. Therefore $M$ accepts $w$, so $w \in L$.

This example was chosen because it separates the three moving pieces: the language $L$, the fixed verifier or machine $M$, and the input $w$. Confusing these levels is one of the most common sources of misunderstanding.

### Misconception: SAT does not simulate the machine by running it

Cook-Levin does not say that the SAT formula runs the Turing machine step by step. A Boolean formula is static. It has no time evolution. Instead, the formula describes a completed computation history all at once. A satisfying assignment is like a filled-in table claiming, "Here is an accepting computation." The clauses then check whether that table is locally and globally consistent.

### Connection to later material

NP-completeness theory depends on this style of reasoning. Once SAT is shown NP-complete, later NP-completeness proofs usually reduce SAT, or a close variant such as 3-SAT, to new problems. Cook-Levin is the foundational source of that reduction chain. It explains why Boolean formulas are a universal encoding medium for efficient verification.

### Retain / Do not confuse

Retain: Cook-Levin proves that SAT is in NP and NP-hard. The NP-hardness proof builds a formula whose satisfying assignments correspond exactly to accepting computations.

Do not confuse: A reduction to SAT is not an algorithm for finding an accepting computation. It only constructs a formula that has a satisfying assignment exactly when such a computation exists.

---

# 2. SAT and why it is in NP

The theorem says SAT is NP-complete, so the first responsibility is to show SAT belongs to NP. This part is straightforward, but it matters because NP-completeness has two sides. A problem cannot be NP-complete unless it is actually in NP.

## 2.1 The object being introduced: Boolean formulas and satisfying assignments

A Boolean formula is a finite expression built from variables using logical connectives such as AND, OR, and NOT. A truth assignment chooses true or false for every variable. A formula is satisfiable if there exists at least one assignment that makes the whole formula true.

This object is important because it naturally represents constraints. Each clause, subformula, or connective imposes a condition. A satisfying assignment is a simultaneous solution to all those conditions.

### Formal definition: SAT

The Boolean satisfiability problem, SAT, is the decision problem:

**Input:** A Boolean formula $\Phi$ over variables $x_1, x_2, \dots, x_m$.

**Question:** Does there exist a truth assignment $a : \{x_1, \dots, x_m\} \to \{\text{true}, \text{false}\}$ such that $\Phi$ evaluates to true under $a$?

Equivalently,

$$
\Phi \in SAT \quad \text{if and only if} \quad \exists a \; [\Phi(a)=\text{true}].
$$

### Interpretation

The existential quantifier is the important part. SAT asks whether there is some hidden choice of truth values that makes the formula true. This matches the structure of NP: a yes-instance has a certificate, and the certificate can be checked efficiently. For SAT, the certificate is simply the truth assignment.

### Assumptions and boundary conditions

The formula must be written in a finite representation whose size is the input length. Checking an assignment requires evaluating the formula in time polynomial in the formula length. This is true for the usual encodings of Boolean formulas because each connective and variable occurrence can be inspected a bounded number of times.

If a formula has exponentially many variables written implicitly, then that would be a different problem representation. SAT as used in Cook-Levin is the explicit finite formula problem.

### Fully worked example: verifying a SAT certificate

Consider the formula

$$
\Phi = (x \lor \neg y) \land (y \lor z) \land (\neg x \lor \neg z).
$$

This example is chosen because it is small enough to inspect fully, but it already shows the certificate-checking pattern that defines membership in NP.

Suppose the proposed certificate is

$$
x=\text{true}, \quad y=\text{false}, \quad z=\text{true}.
$$

We check the formula clause by clause.

The first clause is $x \lor \neg y$. Since $x$ is true, the whole clause is true. Also $y$ is false, so $\neg y$ is true, giving a second reason the clause is true.

The second clause is $y \lor z$. Here $y$ is false, but $z$ is true, so the clause is true.

The third clause is $\neg x \lor \neg z$. Since $x$ is true, $\neg x$ is false. Since $z$ is true, $\neg z$ is false. Therefore this clause is false.

Because the whole formula is an AND of the three clauses, one false clause makes the entire formula false. This certificate does not prove satisfiability.

Now try

$$
x=\text{true}, \quad y=\text{true}, \quad z=\text{false}.
$$

The first clause $x \lor \neg y$ is true because $x$ is true. The second clause $y \lor z$ is true because $y$ is true. The third clause $\neg x \lor \neg z$ is true because $z$ is false, so $\neg z$ is true. All clauses are true, so the assignment satisfies $\Phi$.

The general lesson is that verification is different from search. Finding the satisfying assignment may be difficult, but checking a proposed assignment is efficient.

### Misconception: NP does not mean "not polynomial"

The letters NP stand for nondeterministic polynomial time, not "non-polynomial." A problem in NP may or may not have a known polynomial-time algorithm. The defining feature is efficient verifiability of yes-instances.

### Connection to later material

SAT's membership in NP is simple. The deep part is the reverse direction: every NP problem reduces to SAT. Later reductions often start from SAT because Cook-Levin gives us permission to treat SAT as a representative of all NP verification problems.

### Retain / Do not confuse

Retain: SAT is in NP because a satisfying assignment is a short certificate, and evaluating a formula under an assignment is efficient.

Do not confuse: Checking a given assignment is not the same as finding one.

---

# 3. From NP to nondeterministic computation

To reduce every NP language to SAT, we need a common model for all NP computations. The canonical model used in Cook-Levin is a nondeterministic polynomial-time Turing machine. This is not because Turing machines are convenient for programming. They are used because they give a precise, low-level model whose configurations can be encoded locally.

## 3.1 The object being introduced: a nondeterministic Turing machine

A nondeterministic Turing machine is a formal machine whose transition relation may allow several possible next moves from a single configuration. A computation accepts if at least one branch reaches an accepting state. This existential branching is exactly what NP needs: a yes-instance is accepted if there exists a sequence of choices leading to acceptance.

For Cook-Levin, nondeterminism plays the role that a witness plays in verifier-based definitions of NP. The satisfying assignment to the SAT formula will choose one complete accepting branch.

### Formal definition: nondeterministic polynomial-time decision

A language $L$ is in NP if there exists a nondeterministic Turing machine $M$ and a polynomial $p$ such that for every input $w$ of length $n$:

1. Every computation branch of $M$ on $w$ halts within at most $p(n)$ steps.
2. If $w \in L$, then at least one computation branch of $M$ accepts $w$.
3. If $w \notin L$, then no computation branch of $M$ accepts $w$.

The polynomial $p$ is a time bound. It controls the size of the computation history that must be encoded.

### Interpretation

The word "nondeterministic" can be misleading. It does not mean random. A nondeterministic machine is not making probabilistic choices. Instead, it defines a tree of possible computation paths. Acceptance means existential success: at least one path accepts.

The Cook-Levin formula will not encode the whole tree. That would usually be too large. It encodes a single path and asks whether there exists a way to fill it in so that it is accepting. The existential quantifier in SAT replaces the existential branching of the machine.

### Assumptions and boundary conditions

The machine $M$ is fixed for the language $L$. The input $w$ varies. The polynomial time bound $p(n)$ is fixed once $M$ is fixed. For a given input length $n$, the maximum number of time steps is

$$
T = p(n).
$$

We may assume, by harmless standard modifications, that the machine has a designated accepting state, a designated rejecting state, and halts within the bound. We may also arrange that once it enters the accepting state, it remains in an accepting configuration for the remaining rows of the tableau. This padding convention simplifies the formula because we can require an accepting state somewhere, or require it at the final time, without changing the language decided by the machine.

These conventions do not change NP. They only make the encoding cleaner.

### Fully worked example: nondeterministic acceptance as existential choice

Imagine a nondeterministic machine $M$ that checks whether a string $w$ contains two positions satisfying some property. On input $w$, it first chooses a position $i$, then chooses a position $j$, and then checks deterministically whether the pair $(i,j)$ has the desired property.

If there is a good pair, then one branch chooses it and accepts. If there is no good pair, every branch eventually rejects. The machine's nondeterministic choices correspond to a certificate: the pair $(i,j)$.

This example is chosen because it makes clear that nondeterminism is not magic. It is a formal way to express "there exists a useful witness." In Cook-Levin, the witness will be even larger: it will be a full accepting computation history, including every nondeterministic choice and every resulting configuration.

### Misconception: the formula does not encode all branches

A frequent misconception is that the SAT formula must represent the entire nondeterministic computation tree. It does not. It represents one candidate branch. If the input is accepted, at least one branch works, so one satisfying assignment exists. If the formula has a satisfying assignment, that assignment identifies one valid accepting branch.

### Connection to later material

This one-branch view is essential for understanding NP reductions. NP is existential: there exists a certificate, there exists an accepting branch, there exists a satisfying assignment. Cook-Levin works because these existential statements can be aligned.

### Retain / Do not confuse

Retain: A nondeterministic machine accepts if some branch accepts. The Cook-Levin formula encodes one branch, not the whole tree.

Do not confuse: Nondeterministic choice is not probability. There are no likelihoods, distributions, or random outcomes in the proof.

---

# 4. The computation tableau

The main difficulty is turning an evolving computation into a static Boolean formula. The object that makes this possible is the computation tableau. A tableau is a table whose rows represent time and whose columns represent tape positions. It turns a computation into a finite rectangular object.

## 4.1 The object being introduced: a computation history as a table

A Turing machine computation changes over time. A Boolean formula, however, has no time. To encode a computation in a formula, we need to lay the whole computation out at once. The tableau does exactly that.

Each row of the tableau represents one complete configuration of the machine: the tape contents, the head position, and the current state. Row $0$ is the initial configuration on input $w$. Row $1$ is the result after one transition. Row $2$ is the result after two transitions, and so on. If the time bound is $T$, the tableau has rows indexed by

$$
t = 0,1,2,\dots,T.
$$

The columns represent the tape cells that the machine could possibly visit within $T$ steps. Since the head moves at most one cell per step, only polynomially many tape cells are relevant.

### Formal definition: tableau dimensions

Let $M$ be a nondeterministic Turing machine that halts within $T = p(n)$ steps on inputs of length $n$. For input $w$ of length $n$, the Cook-Levin tableau has:

- time rows $t = 0,1,\dots,T$;
- tape columns $i = 0,1,\dots,S-1$, where $S$ is a polynomial upper bound on the number of tape cells that can be relevant during $T$ steps.

For a one-tape machine that starts at the left end of the input and moves at most one square per step, one may take $S = T+1$ or $S = T+n+1$, depending on the exact tape convention. The important point is that $S$ is polynomial in $n$.

Each cell $(t,i)$ of the tableau contains a symbol from a finite alphabet $C$ of possible cell contents.

A common choice is

$$
C = \Gamma \cup (Q \times \Gamma),
$$

where $\Gamma$ is the tape alphabet and $Q$ is the set of machine states. A plain tape symbol $a \in \Gamma$ means that tape cell $i$ contains $a$ and the head is not scanning that cell at time $t$. A pair $(q,a) \in Q \times \Gamma$ means that tape cell $i$ contains $a$, the head is scanning cell $i$, and the machine is in state $q$ at time $t$.

### Interpretation

The extended alphabet $C$ packages three pieces of information into the row: tape symbols, head position, and state. Exactly one cell in a valid configuration should contain a state-symbol pair. That cell identifies where the head is and what state the machine is in. All other cells contain ordinary tape symbols.

This packaging is not logically necessary, but it is pedagogically useful. It lets each tableau cell have exactly one content. The formula can then enforce that the table is a sequence of configurations by enforcing exactly one content per cell and local consistency between adjacent rows.

### Assumptions and boundary conditions

The set $C$ is constant size because $M$ is fixed. It does not grow with the input $w$. This matters for polynomial size. If $C$ grew exponentially, the formula could become too large.

The number of rows and columns is polynomial because the machine runs in polynomial time. This is the central boundary condition of the proof. Cook-Levin relies on the computation history being polynomially large. If a machine ran for exponentially many steps, the tableau would generally be exponentially large and could not be written down by a polynomial-time reduction.

The tableau includes enough cells to contain every possible position the head can reach within $T$ steps. Cells outside that range are irrelevant because the head cannot reach them in time.

### Fully worked example: reading a small tableau row

Suppose the tape alphabet contains $0$, $1$, and blank $\sqcup$, and suppose the machine has a state $q$. A row of the tableau might look like

$$
0 \quad 1 \quad (q,0) \quad 1 \quad \sqcup \quad \sqcup.
$$

This row says the tape currently contains $0,1,0,1,\sqcup,\sqcup$ on the displayed cells, the head is scanning the third displayed cell, and the current state is $q$.

This example is chosen because it shows why the pair $(q,0)$ is not an extra cell. It is the content of one cell. It says both "the symbol here is $0$" and "the machine is currently here in state $q$."

If the transition relation says that, from state $q$ reading $0$, the machine may write $1$, move right, and enter state $r$, then the next row might locally become

$$
0 \quad 1 \quad 1 \quad (r,1) \quad \sqcup \quad \sqcup.
$$

Only the old head cell, its neighbor, and the state marker need to change. Distant tape cells stay the same.

The general lesson is that a global transition has a local footprint. This is the reason the formula can check transitions using small windows rather than comparing whole rows in one enormous condition.

### Misconception: a tableau is not itself a proof unless it is checked

An arbitrary table with symbols in it is not automatically a computation. It may have two heads, no head, a wrong initial row, illegal transitions, or no accepting state. The SAT formula exists to enforce exactly the conditions that make a table a valid accepting computation history.

### Connection to later material

The tableau is the bridge between computation and logic. Later parts of the proof introduce variables and clauses. Those clauses are not arbitrary; each one enforces a property needed for the tableau to be a legal accepting computation.

### Retain / Do not confuse

Retain: A tableau is a polynomial-size table representing one possible computation path over time.

Do not confuse: A row is a full configuration. A cell is only one tape position at one time.

---

# 5. Variables: turning tableau entries into Boolean choices

A Boolean formula can only talk about truth values. A tableau cell, however, is supposed to contain one symbol from a finite set $C$. The next step is therefore to introduce Boolean variables that express possible cell contents.

## 5.1 The object being introduced: cell-content variables

The formula needs a way to say things such as "at time $t$, tape position $i$ contains symbol $a$" or "at time $t$, the head is at position $i$ in state $q$ reading $a$." Each such statement becomes a Boolean variable.

The assignment to these variables is supposed to fill in the tableau. True variables mark the chosen contents; false variables mark contents not chosen.

### Formal definition: tableau variables

For every time $t \in \{0,1,\dots,T\}$, every tape position $i \in \{0,1,\dots,S-1\}$, and every cell content $c \in C$, introduce a Boolean variable

$$
X_{t,i,c}.
$$

The intended meaning is

$$
X_{t,i,c}=\text{true} \quad \text{if and only if cell } (t,i) \text{ contains } c.
$$

### Interpretation

The indices say exactly what the variable is about.

- $t$ fixes the time row.
- $i$ fixes the tape position.
- $c$ names a possible content for that cell.

For a fixed pair $(t,i)$, the variables $X_{t,i,c}$ range over all possible contents $c \in C$. A valid tableau must choose exactly one of them to be true.

### Assumptions and boundary conditions

The number of variables is

$$
(T+1) \cdot S \cdot |C|.
$$

Since $T$ and $S$ are polynomial in $n$, and $|C|$ is constant because $M$ is fixed, the number of variables is polynomial in $n$.

This is one of the key polynomial-size checks in the proof. The construction is useful only because it does not introduce exponentially many variables.

### Fully worked example: one cell with several possible contents

Suppose $C = \{0,1,\sqcup,(q,0),(q,1),(r,0),(r,1)\}$. For the tableau cell at time $3$ and position $5$, the construction introduces variables such as

$$
X_{3,5,0}, \quad X_{3,5,1}, \quad X_{3,5,\sqcup}, \quad X_{3,5,(q,0)}, \quad X_{3,5,(r,1)}.
$$

If $X_{3,5,(q,0)}$ is true, then the intended interpretation is that at time $3$, the head is scanning position $5$, the machine is in state $q$, and the symbol under the head is $0$.

But this interpretation is valid only if all other variables for the same cell are false. Otherwise the assignment might claim that the same cell contains both $(q,0)$ and $1$, which is impossible in a real computation. This is why the next family of clauses enforces uniqueness.

This example was chosen to show that variables alone do not encode validity. Variables provide a vocabulary. Clauses provide constraints.

### Misconception: the variable does not store a symbol

A Boolean variable stores only true or false. The collection of variables indexed by $c \in C$ jointly represents the choice of a symbol. This is a standard encoding pattern: represent a finite-valued object by several Boolean variables plus constraints forcing exactly one choice.

### Connection to later material

Once we have variables, every property of a valid computation must be expressed as a Boolean constraint on those variables. The rest of the proof constructs those constraints.

### Retain / Do not confuse

Retain: $X_{t,i,c}$ means "cell $(t,i)$ contains content $c$." For each fixed $(t,i)$, exactly one content should be true.

Do not confuse: The variable family is an encoding vocabulary, not yet a guarantee of a legal tableau.

---

# 6. The four kinds of constraints

The Cook-Levin formula is built by conjoining several groups of constraints. Each group solves one specific problem that an arbitrary assignment might otherwise have. The formula must force the assignment to describe a valid accepting computation, not just a random table.

The major constraint families are:

1. Cell constraints: every tableau cell contains exactly one content.
2. Start constraints: the first row is the initial configuration of $M$ on input $w$.
3. Accept constraints: some row contains an accepting state, or the final row is accepting under a padding convention.
4. Move constraints: each row legally follows from the previous row according to $M$'s transition relation.

The formula is the conjunction

$$
\Phi_{M,w}
= \Phi_{\text{cell}}
\land \Phi_{\text{start}}
\land \Phi_{\text{accept}}
\land \Phi_{\text{move}}.
$$

Each component blocks a different kind of invalid satisfying assignment.

---

# 7. Cell constraints: every position has exactly one content

The first problem is basic representation. A satisfying assignment could otherwise leave a cell empty by making all its content variables false, or could make a cell contradictory by making several contents true. Neither is allowed in a real tableau.

## 7.1 The object being introduced: exactly-one constraints

For every cell $(t,i)$, the formula must enforce that one and only one content $c \in C$ is selected. This is a local well-formedness condition. It does not yet say anything about the machine's computation; it only says the table is filled in coherently.

### Formal definition: cell constraints

For each fixed time $t$ and position $i$, include a clause requiring at least one content:

$$
\bigvee_{c \in C} X_{t,i,c}.
$$

For each pair of distinct contents $c,d \in C$ with $c \neq d$, include a clause forbidding both contents at once:

$$
\neg X_{t,i,c} \lor \neg X_{t,i,d}.
$$

Together these clauses force exactly one variable among $\{X_{t,i,c} : c \in C\}$ to be true.

### Interpretation

The first clause says the cell cannot be blank in the representational sense: it must contain some member of $C$. Notice that the tape blank symbol $\sqcup$ is itself a legitimate content. So "not empty" here means not undefined, not "not blank."

The pairwise clauses say the cell cannot contain two different things. If $X_{t,i,c}$ is true, then $X_{t,i,d}$ must be false for every $d \neq c$.

### Assumptions and boundary conditions

Because $C$ is finite and constant size, the number of pairwise exclusion clauses per cell is constant. There are polynomially many cells, so the total number of cell constraints is polynomial.

If $C$ were allowed to grow with the input, the pairwise exclusions would still be polynomial if $|C|$ were polynomial, but in the standard proof $C$ is constant because the machine is fixed.

### Fully worked example: exactly one content

Suppose for a particular cell $(t,i)$ there are three possible contents $C=\{a,b,c\}$. The exactly-one requirement is expressed by

$$
(X_{t,i,a} \lor X_{t,i,b} \lor X_{t,i,c})
$$

and

$$
(\neg X_{t,i,a} \lor \neg X_{t,i,b}),
\quad
(\neg X_{t,i,a} \lor \neg X_{t,i,c}),
\quad
(\neg X_{t,i,b} \lor \neg X_{t,i,c}).
$$

If all three variables are false, the first clause fails. So at least one must be true.

If two variables are true, say $X_{t,i,a}$ and $X_{t,i,b}$, then the clause $\neg X_{t,i,a} \lor \neg X_{t,i,b}$ fails. So at most one can be true.

Combining these facts gives exactly one true variable.

This example was chosen because exactly-one constraints are a recurring encoding pattern. Cook-Levin is not only a theorem about Turing machines; it also teaches how finite choices can be represented inside SAT.

### Misconception: "at least one" is not enough

It is tempting to include only the large OR clause. That would ensure every cell has some content, but it would not prevent multiple contents. A satisfying assignment could then describe impossible cells. The proof would fail in the reverse direction because a satisfying assignment would not necessarily decode into a real computation history.

### Connection to later material

The move constraints assume that each cell has a unique content. Without uniqueness, local windows would be ambiguous. Thus cell constraints are the foundation for decoding an assignment into a tableau.

### Retain / Do not confuse

Retain: Cell constraints make the table well-defined by forcing exactly one content per cell.

Do not confuse: A blank tape symbol is a content. It is different from an undefined cell in the encoding.

---

# 8. Start constraints: fixing the initial configuration

The formula is supposed to describe computations of $M$ on the particular input $w$. If the first row were allowed to vary freely, the formula might become satisfiable because the machine accepts some other input or starts from an impossible configuration. The start constraints prevent that.

## 8.1 The object being introduced: the initial row

The initial row is the anchor of the computation history. It says where the machine begins, what input is on the tape, where the head is, and what state the machine is in. Without this anchor, the tableau would not answer the original question about $w$.

### Formal definition: start constraints

Assume the machine starts in state $q_0$, with the head at cell $0$, and the input string

$$
w = w_0w_1\dots w_{n-1}
$$

written in cells $0$ through $n-1$, followed by blanks. Under the extended alphabet convention, the first cell contains $(q_0,w_0)$ if $n>0$. The remaining input cells contain their input symbols, and cells beyond the input contain blanks.

The start constraints set the row $t=0$ accordingly:

- $X_{0,0,(q_0,w_0)}$ is required to be true, for nonempty input.
- For each input cell $i$ with $1 \leq i \leq n-1$, $X_{0,i,w_i}$ is required to be true.
- For each relevant cell $i \geq n$, $X_{0,i,\sqcup}$ is required to be true.

For empty input, the analogous condition places $(q_0,\sqcup)$ in the starting cell.

### Interpretation

These constraints hardwire the input into the formula. This is why the formula is called $\Phi_{M,w}$ rather than just $\Phi_M$. The machine $M$ is fixed, but $w$ changes the start row, and therefore changes the formula.

The start constraints are simple unit constraints: they require individual variables to be true. The cell constraints then force the other possible contents of those cells to be false.

### Assumptions and boundary conditions

The exact form of the initial row depends on the Turing machine convention. Some machines use a left endmarker. Some place the head on the first input symbol. Some use separate input and work tapes. These differences do not affect the theorem. They only change the constant-size local details of the encoding.

What matters is that the initial configuration can be described by polynomially many fixed cell contents and that those contents can be generated efficiently from $w$.

### Fully worked example: start row for a short input

Let $w=101$, and suppose the relevant tape window has six cells. Suppose the machine starts in state $q_0$ at the first input cell. The intended first row is

$$
(q_0,1) \quad 0 \quad 1 \quad \sqcup \quad \sqcup \quad \sqcup.
$$

The start constraints require:

$$
X_{0,0,(q_0,1)},
\quad
X_{0,1,0},
\quad
X_{0,2,1},
\quad
X_{0,3,\sqcup},
\quad
X_{0,4,\sqcup},
\quad
X_{0,5,\sqcup}.
$$

Each requirement fixes one cell of row $0$. Because the cell constraints are already present, requiring $X_{0,1,0}$ also rules out $X_{0,1,1}$, $X_{0,1,\sqcup}$, and every state-symbol content at that same cell.

This example was chosen because it shows how the input is not merely referenced by the formula; it is embedded into the first row.

### Misconception: the formula is not universal for all inputs at once

The construction does not build one formula whose assignments choose both an input and an accepting computation. For the reduction, the input $w$ is already given. The formula asks whether this specific input is accepted.

### Connection to later material

The start constraints will be used in the soundness direction. When we decode a satisfying assignment, these constraints guarantee that the decoded computation begins with $M$ on $w$, not with some arbitrary configuration.

### Retain / Do not confuse

Retain: Start constraints hardwire the input $w$ into row $0$.

Do not confuse: $M$ is fixed by the language; $w$ is the varying instance being reduced to SAT.

---

# 9. Accept constraints: forcing successful computation

A legal computation history is not enough. The tableau must represent an accepting computation. The accept constraints express this final goal.

## 9.1 The object being introduced: acceptance inside the tableau

Acceptance is a state condition. Somewhere in the computation, the machine must enter its accepting state $q_{acc}$. Since the tableau records the state by placing a state-symbol pair in exactly one cell of each row, acceptance can be detected by looking for any cell containing $(q_{acc},a)$ for some tape symbol $a$.

### Formal definition: accept constraints

One common version requires that the accepting state occurs somewhere in the tableau:

$$
\bigvee_{t=0}^{T} \bigvee_{i=0}^{S-1} \bigvee_{a \in \Gamma} X_{t,i,(q_{acc},a)}.
$$

Another common version modifies the machine so that, once it accepts, it stays in an accepting configuration until time $T$. Then it is enough to require that the final row contains the accepting state:

$$
\bigvee_{i=0}^{S-1} \bigvee_{a \in \Gamma} X_{T,i,(q_{acc},a)}.
$$

Both versions are valid if the machine convention is handled consistently.

### Interpretation

The accept constraint is the existential goal of the tableau. It says that the computation path represented by the assignment is not merely legal; it reaches success.

If we use the final-row version, the proof usually assumes a padding convention: after accepting, the machine keeps producing legal accepting configurations until the time bound is reached. This avoids needing to identify the exact accepting time.

### Assumptions and boundary conditions

If the machine can halt before time $T$, then the tableau still has $T+1$ rows. To keep the move constraints meaningful after halting, we either require halting states to have self-loop transitions or pad the computation with repeated accepting or rejecting configurations. This is a standard harmless transformation.

The accept constraint must be compatible with the move constraints. If accepting configurations have no legal successors but the tableau has rows after acceptance, the formula may accidentally reject valid accepting computations unless padding is added.

### Fully worked example: final-row acceptance

Suppose $T=5$, $S=4$, and the tape alphabet is $\{0,1,\sqcup\}$. If we use the final-row convention, the accept clause is

$$
X_{5,0,(q_{acc},0)} \lor X_{5,0,(q_{acc},1)} \lor X_{5,0,(q_{acc},\sqcup)}
$$

$$
{}\lor X_{5,1,(q_{acc},0)} \lor X_{5,1,(q_{acc},1)} \lor X_{5,1,(q_{acc},\sqcup)}
$$

$$
{}\lor X_{5,2,(q_{acc},0)} \lor X_{5,2,(q_{acc},1)} \lor X_{5,2,(q_{acc},\sqcup)}
$$

$$
{}\lor X_{5,3,(q_{acc},0)} \lor X_{5,3,(q_{acc},1)} \lor X_{5,3,(q_{acc},\sqcup)}.
$$

The clause says that in the final row, at some position, the head is present and the state is $q_{acc}$. The symbol under the head may be $0$, $1$, or blank, so the clause includes all possibilities.

This example was chosen because it shows why the accepting condition quantifies over both tape position and scanned symbol. The accepting state alone is not stored separately; it is stored together with the scanned symbol in a cell content.

### Misconception: acceptance is not the same as having a true variable named "accept"

The tableau encoding does not usually introduce a separate global variable saying "the machine accepts." Acceptance must be witnessed by the presence of the accepting state in the encoded configuration. Otherwise the formula could set a global accept variable to true without proving that the computation actually reaches $q_{acc}$.

### Connection to later material

The accept constraint supplies the final step in the soundness proof. After decoding a satisfying assignment into a legal computation, this clause guarantees that the computation is accepting.

### Retain / Do not confuse

Retain: Accept constraints require the encoded computation to reach $q_{acc}$, usually in some row or in the final row after padding.

Do not confuse: A legal computation history can be rejecting. Cook-Levin needs a legal accepting history.

---

# 10. Move constraints: enforcing legal transitions

The most important part of the proof is the move constraint. It ensures that each row follows from the previous row according to the machine's transition relation. This is where computation is encoded.

The central insight is locality: a Turing machine transition changes only a small neighborhood around the head. Most cells simply copy their contents from one row to the next. Because of this locality, we do not need a huge formula that compares entire rows in one piece. We can enforce legality by checking small windows.

## 10.1 The object being introduced: local consistency

A valid computation has a global property: every row is the successor of the previous row. But this global property can be checked locally because a Turing machine's transition rule only looks at the current state, the symbol under the head, and then writes one symbol, changes state, and moves the head left or right.

The formula uses local windows to enforce that no illegal change occurs between adjacent rows.

### Formal definition: legal windows

Consider two adjacent rows, time $t$ and time $t+1$. For each position $i$, inspect a small neighborhood around $i$, such as columns $i-1$, $i$, and $i+1$ in both rows. This gives a local window:

$$
\begin{matrix}
\text{row } t: & c_{i-1} & c_i & c_{i+1} \\
\text{row } t+1: & d_{i-1} & d_i & d_{i+1}
\end{matrix}
$$

A window is legal if it can occur as part of some valid transition of $M$, or if it is an unchanged region far from the head.

The move constraints forbid every illegal local window.

### Interpretation

Instead of trying to write one enormous rule saying "row $t+1$ is a legal successor of row $t$," we write many small rules saying "no local neighborhood looks impossible." Since the Turing machine transition relation is local, these small checks are sufficient.

This is the same philosophical move that appears in many areas of mathematics and computer science: replace a global condition by enough local consistency conditions. The proof works because the underlying computation model is local.

### Assumptions and boundary conditions

The window size depends on the exact machine model and encoding. A three-cell neighborhood is standard for a one-tape Turing machine with head movement by one cell. If the model allowed the head to jump far away in one step, this local encoding would need to change.

Boundary cells require special handling. At the left and right edges of the displayed tape region, one may add fixed boundary markers or define windows only where all needed neighboring cells exist. Standard presentations use boundary symbols to make the local checks uniform. These are technical details, not conceptual obstacles.

The set of possible local windows is constant size because $C$ is constant size and the window has constant width. Therefore the list of illegal windows can be generated in polynomial time and contributes only polynomially many clauses.

### Fully worked example: a legal transition window

Suppose row $t$ contains the local pattern

$$
\cdots \quad b \quad (q,a) \quad c \quad \cdots
$$

and the machine has a transition that, when in state $q$ reading $a$, writes $a'$, moves right, and enters state $r$.

Then the next row should locally contain

$$
\cdots \quad b \quad a' \quad (r,c) \quad \cdots.
$$

The old head cell no longer contains the state. It now contains the written symbol $a'$. The right neighbor becomes the head position and stores both the new state $r$ and the symbol $c$ that was already in that cell.

This example was chosen because it displays the exact information flow in a right move. The new state marker moves into the neighboring cell; the symbol in that neighboring cell is not overwritten merely because the head moves there. It becomes paired with the new state.

A local window around these cells checks that this transformation is one of the transformations allowed by the transition relation. If the next row instead contained

$$
\cdots \quad b \quad a' \quad (s,c) \quad \cdots
$$

where $s$ is not an allowed next state, the window would be illegal and the formula would forbid it.

### Misconception: distant cells do not need a separate global copying rule

It may seem that the formula must explicitly say every non-head cell stays the same. In local-window presentations, this is folded into the legality of windows. If a far-away cell changed from $0$ to $1$ even though no head was nearby, some local window around that cell would show an unexplained change and would be forbidden.

### Connection to later material

Move constraints are the heart of the soundness proof. They ensure that a satisfying assignment cannot fake a computation by jumping from one configuration to an unrelated one. They also reveal why Turing machines are useful in the proof: their local transition structure is easy to encode in SAT.

### Retain / Do not confuse

Retain: Move constraints forbid illegal local windows between adjacent rows. Local consistency enforces global legal evolution.

Do not confuse: The formula does not compute the next row. It constrains the pair of rows so that the second could legally follow from the first.

---

# 11. How to turn local illegality into clauses

The previous section described local checks conceptually. Now we need to see how a Boolean formula forbids a specific illegal pattern. This step is small but crucial: it is the bridge from tableau reasoning to SAT syntax.

## 11.1 The object being introduced: pattern-forbidding clauses

A local window assigns particular contents to several tableau cells. If that pattern is illegal, the formula must prevent all those contents from occurring together. This is exactly what a disjunctive clause of negated variables does.

### Formal definition: forbidding an illegal window

Suppose an illegal window specifies that the following variables are all true:

$$
X_{t,i-1,c_{i-1}},
X_{t,i,c_i},
X_{t,i+1,c_{i+1}},
X_{t+1,i-1,d_{i-1}},
X_{t+1,i,d_i},
X_{t+1,i+1,d_{i+1}}.
$$

To forbid this exact illegal window, include the clause

$$
\neg X_{t,i-1,c_{i-1}}
\lor
\neg X_{t,i,c_i}
\lor
\neg X_{t,i+1,c_{i+1}}
\lor
\neg X_{t+1,i-1,d_{i-1}}
\lor
\neg X_{t+1,i,d_i}
\lor
\neg X_{t+1,i+1,d_{i+1}}.
$$

This clause says that at least one component of the illegal pattern must be absent.

### Interpretation

The clause is false only when every listed variable is true. That is exactly the forbidden case: the illegal window appears in full. If the tableau differs from that illegal pattern in even one cell, the clause is true.

So a single clause can ban one bad local configuration. The move formula is built by adding such clauses for every illegal local window at every applicable time and position.

### Assumptions and boundary conditions

The number of possible windows is constant with respect to $n$ because the window size and alphabet are fixed. For each adjacent pair of rows and each position, only constantly many window patterns need to be considered. Since there are polynomially many row pairs and positions, the total number of move clauses is polynomial.

The formula may not initially be in 3-CNF because a window-forbidding clause may have more than three literals. This is not a problem for SAT. If the target problem is 3-SAT, standard transformations convert the formula into an equisatisfiable 3-CNF formula with only polynomial blowup.

### Fully worked example: forbidding a simple illegal change

Suppose a region is far from the head. At time $t$, three adjacent cells contain

$$
0 \quad 0 \quad 1.
$$

At time $t+1$, suppose the same three cells contain

$$
0 \quad 1 \quad 1.
$$

If no head appears in or near this window, the middle cell changed from $0$ to $1$ without a transition causing it. This is illegal.

The corresponding forbidden-pattern clause is

$$
\neg X_{t,i-1,0}
\lor
\neg X_{t,i,0}
\lor
\neg X_{t,i+1,1}
\lor
\neg X_{t+1,i-1,0}
\lor
\neg X_{t+1,i,1}
\lor
\neg X_{t+1,i+1,1}.
$$

If a proposed tableau contains exactly that illegal window, all six variables are true, so all six negations are false, and the clause fails. If the proposed tableau differs in any one of those six positions, the clause is satisfied.

This example was chosen because it shows how a clause can enforce a negative rule: "this bad pattern must not occur." Many students expect formulas to describe good transitions directly, but forbidding bad local windows is often cleaner.

### Misconception: a long clause is not a sequence of steps

The clause is not saying to check the first literal, then the second, and so on as a computation. It is a static logical condition. It excludes exactly one simultaneous assignment pattern.

### Connection to later material

Pattern-forbidding clauses are the technical mechanism behind the reduction. Once the reader understands them, the rest of the proof becomes a size and correctness argument.

### Retain / Do not confuse

Retain: To forbid a bad pattern, write a clause saying at least one part of that pattern is not present.

Do not confuse: The clause does not describe a transition being taken. It rules out a local inconsistency.

---

# 12. Polynomial size of the construction

A reduction is useful only if it runs in polynomial time and produces an output of polynomial size. The tableau idea would not prove NP-hardness if the formula were exponentially large.

## 12.1 The object being introduced: the size bound

The size bound checks that every part of the formula is polynomial in $n=|w|$. The fixed machine $M$ may contribute constants, such as the number of states and tape symbols, but those constants do not grow with the input.

### Formal size analysis

Let

$$
T = p(n)
$$

be the time bound, and let $S$ be a polynomial bound on relevant tape cells, for example $S = T+n+1$.

The number of tableau cells is

$$
(T+1)S.
$$

The number of variables is

$$
(T+1)S|C|,
$$

which is polynomial because $T$ and $S$ are polynomial and $|C|$ is constant.

The cell constraints contribute polynomially many clauses: for each cell, one at-least-one clause and constantly many pairwise at-most-one clauses.

The start constraints contribute $S$ unit requirements, hence polynomially many.

The accept constraint contributes one large OR over at most $(T+1)S|\Gamma|$ possibilities, or over $S|\Gamma|$ possibilities if only the final row is used. This is polynomial.

The move constraints contribute polynomially many clauses because there are $T$ adjacent row pairs, $S$ positions, and only constantly many illegal local windows per position.

Therefore $\Phi_{M,w}$ has polynomial size and can be produced in polynomial time.

### Interpretation

The size analysis is not a side detail. It is where the polynomial-time hypothesis enters the proof. NP computations have polynomial-length histories, and polynomial-length histories can be written into polynomial-size formulas.

### Assumptions and boundary conditions

The machine $M$ is fixed. If the machine description were part of the input, then $|Q|$, $|\Gamma|$, and the transition relation would no longer be constants. There are universal-machine variants of the theorem that handle machine descriptions, but the standard language-reduction proof fixes $M$ for each language $L$.

The polynomial $p$ must be known or at least effectively bounded for the construction. In the theoretical setting, since $M$ is a polynomial-time machine deciding $L$, such a polynomial bound exists and can be incorporated into the reduction.

### Fully worked example: approximate size with a quadratic time bound

Suppose $M$ runs in time $T=n^2$, and use $S=T+n+1$. Then

$$
S = n^2+n+1,
$$

so the number of cells is

$$
(T+1)S = (n^2+1)(n^2+n+1),
$$

which is on the order of $n^4$.

If $|C|=20$, then the number of variables is about $20n^4$ up to lower-order terms. The number of clauses is also polynomial, because each cell and each local window contributes only constantly many constraints.

This example was chosen to make the polynomial-size claim concrete. The formula may be large, but it is not exponentially large.

### Misconception: large does not mean non-polynomial

Cook-Levin formulas are often enormous in practice. That does not matter for NP-completeness. Polynomial-time reductions may produce large outputs, as long as their size is bounded by a polynomial in the input length.

### Connection to later material

The polynomial-size argument is what qualifies the construction as a polynomial-time reduction. Without it, the logical equivalence between accepting computations and satisfying assignments would not establish NP-hardness.

### Retain / Do not confuse

Retain: The formula is polynomial size because the time bound, tape region, and number of local checks are polynomial.

Do not confuse: A proof of logical equivalence is not enough; the reduction must also be efficient.

---

# 13. Completeness: accepting computation implies satisfying assignment

Now we prove one direction of correctness. Completeness says that if the machine accepts the input, then the formula is satisfiable. The name "completeness" here means the formula does not miss any genuine accepting computation.

## 13.1 The object being introduced: encoding a real computation as an assignment

If $M$ accepts $w$, then there exists an accepting branch of computation. That branch produces a sequence of configurations. We write those configurations into the tableau and then set variables according to the table.

### Formal statement

If $M$ accepts $w$ within $T$ steps, then $\Phi_{M,w}$ is satisfiable.

### Interpretation

This direction is constructive at the level of proof. Given an accepting computation history, we know how to create a satisfying assignment: for each cell $(t,i)$, set $X_{t,i,c}$ to true exactly for the actual content $c$ appearing in that cell of the history.

### Assumptions and boundary conditions

If the accepting computation halts before time $T$, we use the padding convention so that the tableau still has all rows through time $T$. The accepting configuration repeats or evolves through a harmless self-loop until the final row.

The accepting branch must stay within the displayed tape region. This is guaranteed by choosing enough columns for any $T$-step computation.

### Fully worked proof of completeness

Assume $M$ accepts $w$. By the definition of nondeterministic acceptance, there is at least one branch of $M$'s computation on $w$ that reaches $q_{acc}$ within at most $T$ steps.

Write the configurations of that branch into the tableau. Row $0$ is the initial configuration. Row $1$ is the result of the first transition on that branch. Continue in this way until row $T$, padding after acceptance if necessary.

Now define the truth assignment. For each triple $(t,i,c)$, set

$$
X_{t,i,c}=\text{true}
$$

exactly when the actual tableau cell $(t,i)$ contains $c$. Set it to false otherwise.

We check the formula component by component.

The cell constraints are satisfied because every actual tableau cell has exactly one content. Therefore, for each fixed $(t,i)$, exactly one of the variables $X_{t,i,c}$ is true.

The start constraints are satisfied because row $0$ was chosen to be the true initial configuration of $M$ on $w$.

The accept constraints are satisfied because the selected branch is accepting, and padding ensures acceptance appears in the required row if the construction requires final-row acceptance.

The move constraints are satisfied because every adjacent pair of rows comes from a legal transition of $M$. Therefore no illegal local window appears.

Since every component of

$$
\Phi_{M,w}
= \Phi_{\text{cell} }
\land \Phi_{\text{start}}
\land \Phi_{\text{accept}}
\land \Phi_{\text{move}}
$$

is satisfied, the whole formula is satisfied.

This proof was chosen for detailed treatment because it shows the role of each constraint family. Each family corresponds to one feature of the accepting computation history.

### Misconception: completeness does not require finding the accepting branch efficiently

The proof says that if an accepting branch exists, then a satisfying assignment exists. It does not say we can efficiently find that branch. NP reductions preserve yes/no existence, not necessarily witnesses in an efficient practical way.

### Connection to later material

Completeness is one half of the equivalence needed for reductions. It proves that yes-instances of the original problem map to yes-instances of SAT.

### Retain / Do not confuse

Retain: A real accepting computation directly gives a satisfying assignment by setting exactly the variables that describe its tableau.

Do not confuse: Completeness alone does not prove the reduction correct. The reverse direction is equally necessary.

---

# 14. Soundness: satisfying assignment implies accepting computation

Soundness is the more delicate direction. It says that the formula cannot be satisfied by nonsense. Every satisfying assignment must decode into a genuine accepting computation of $M$ on $w$.

## 14.1 The object being introduced: decoding an assignment

A satisfying assignment is only a collection of truth values. To prove soundness, we must show that those truth values determine a tableau and that the tableau is valid.

The cell constraints are what make decoding possible. Without them, a cell might contain zero or multiple contents, so the assignment would not define a unique table.

### Formal statement

If $\Phi_{M,w}$ is satisfiable, then $M$ accepts $w$ within $T$ steps.

### Interpretation

This direction proves that the formula has no fake satisfying assignments. If someone claims to satisfy the formula, the clauses force that claim to correspond to a real accepting computation.

### Assumptions and boundary conditions

Soundness relies on the move constraints being strong enough. If the local-window rules are incomplete, a satisfying assignment might encode rows that look locally acceptable but do not form a legal computation. The proof depends on the standard fact that for the chosen Turing machine encoding, legality of adjacent configurations is captured by local windows.

Boundary conventions must also be included correctly. If edge cases at the left end of the tape are ignored, a fake computation might exploit the boundary.

### Fully worked proof of soundness

Assume $\Phi_{M,w}$ is satisfiable, and let $a$ be a satisfying assignment.

First, use the cell constraints. For each tableau position $(t,i)$, the exactly-one clauses guarantee that there is a unique content $c \in C$ such that

$$
X_{t,i,c}=\text{true}
$$

under $a$. Therefore the assignment defines a unique tableau: put content $c$ in cell $(t,i)$.

Second, use the start constraints. They force row $0$ of this decoded tableau to be the initial configuration of $M$ on input $w$.

Third, use the move constraints. These constraints forbid every illegal local window between adjacent rows. Since the assignment satisfies all move clauses, no forbidden local window appears. By the locality property of the Turing machine encoding, each row must therefore be a legal successor of the previous row. Hence the decoded rows form a valid computation path of $M$.

Fourth, use the accept constraints. They force the accepting state $q_{acc}$ to appear in the required place: somewhere in the tableau, or in the final row under the padded convention. Therefore the valid computation path is accepting.

Combining these conclusions, the satisfying assignment decodes into an accepting computation of $M$ on $w$. Thus $M$ accepts $w$.

This proof was chosen for detailed treatment because it is the part that prevents the construction from being merely suggestive. It shows that the formula characterizes accepting computations exactly.

### Misconception: local checks might seem too weak

It can feel surprising that local window checks enforce a whole computation. The reason they suffice is that a Turing machine transition is itself local. The head can only inspect and change a bounded neighborhood in one step. If every local neighborhood between two rows is compatible with such a transition, then the entire row-to-row change is legal.

This would not be true for a model where one step could arbitrarily rearrange the whole tape. The proof depends on the locality of the computational model.

### Connection to later material

Soundness proves that no-instances of the original language map to unsatisfiable formulas. This is what makes the reduction a true if-and-only-if transformation rather than just a witness generator.

### Retain / Do not confuse

Retain: A satisfying assignment decodes into a unique tableau, and the constraints force that tableau to be an accepting computation.

Do not confuse: The formula is not merely consistent with some parts of a computation. It must force the entire computation history.

---

# 15. Completing the theorem

We can now assemble the full Cook-Levin theorem. Each previous component solved one obstacle: SAT is in NP; arbitrary NP computations can be represented by polynomial-size tableaux; tableaux can be encoded with Boolean variables; and clauses can enforce exactly the valid accepting histories.

## 15.1 Formal theorem

**Cook-Levin Theorem.** SAT is NP-complete.

### Proof

First, SAT is in NP. A certificate for a yes-instance is a truth assignment to the variables. Given such an assignment, we can evaluate the formula in polynomial time and verify whether it is satisfied.

Second, SAT is NP-hard. Let $L$ be any language in NP. Then there exists a nondeterministic Turing machine $M$ and a polynomial $p$ such that $M$ decides $L$ in at most $p(n)$ steps on inputs of length $n$.

Given an input $w$, construct the formula

$$
\Phi_{M,w}
= \Phi_{\text{cell}}
\land \Phi_{\text{start}}
\land \Phi_{\text{accept}}
\land \Phi_{\text{move}}.
$$

The formula uses variables $X_{t,i,c}$ to describe the contents of a polynomial-size computation tableau for $M$ on $w$. The constraint families enforce, respectively, that each cell has exactly one content, that the first row is the initial configuration, that the computation accepts, and that adjacent rows follow legally according to $M$'s transition relation.

The construction has polynomial size and can be produced in polynomial time because the tableau has polynomially many rows and columns, and each local condition involves only a constant-size neighborhood.

By completeness, if $w \in L$, then $M$ has an accepting computation on $w$, which yields a satisfying assignment for $\Phi_{M,w}$.

By soundness, if $\Phi_{M,w}$ is satisfiable, then any satisfying assignment decodes into a valid accepting computation of $M$ on $w$, so $w \in L$.

Therefore

$$
w \in L \quad \text{if and only if} \quad \Phi_{M,w} \in SAT.
$$

So $L \leq_p SAT$. Since $L$ was an arbitrary language in NP, SAT is NP-hard. Since SAT is also in NP, SAT is NP-complete.

### Interpretation

The theorem says that Boolean satisfiability is expressive enough to encode every polynomial-time verifiable yes/no question. It does not say all NP problems look like SAT on the surface. It says they can be efficiently translated into SAT while preserving yes/no answers.

### Assumptions and boundary conditions

The proof uses a standard finite Turing machine model. Variations in the model, such as multiple tapes or different boundary conventions, do not change the theorem because they can be simulated with only polynomial overhead and encoded with analogous local constraints.

The proof establishes NP-completeness under polynomial-time many-one reductions. Other reduction notions exist, but the canonical Cook-Levin theorem is usually stated with polynomial-time many-one reductions.

### Fully worked example: what the theorem says for a generic NP problem

Suppose $L$ is the language of yes-instances for some problem whose solutions can be verified in polynomial time. For example, imagine $L$ consists of encodings of finite structures that have some efficiently checkable certificate.

Because $L \in NP$, there is a nondeterministic polynomial-time machine $M$ deciding $L$. For a particular instance $w$, Cook-Levin builds a formula $\Phi_{M,w}$.

If $w$ has a valid certificate, then $M$ has an accepting branch, so the tableau of that branch satisfies the formula.

If $\Phi_{M,w}$ is satisfiable, the satisfying assignment reveals an accepting branch of $M$, and therefore a valid certificate must exist.

This example is intentionally generic because the theorem is generic. The power of Cook-Levin is that it does not depend on the special structure of one problem. It depends only on efficient verifiability.

### Misconception: Cook-Levin does not prove P is different from NP

Cook-Levin proves SAT is NP-complete. It does not prove that SAT requires super-polynomial time. If someone proved SAT has a polynomial-time algorithm, then every problem in NP would have a polynomial-time algorithm, and $P=NP$. If someone proved SAT has no polynomial-time algorithm, then $P \neq NP$. Cook-Levin identifies SAT as central to the question; it does not resolve the question.

### Connection to later material

After Cook-Levin, NP-completeness proofs usually do not encode Turing machines again. Instead, they reduce SAT or 3-SAT to other problems. This creates a web of NP-complete problems: CLIQUE, VERTEX COVER, HAMILTONIAN CYCLE, SUBSET SUM, and many others. Cook-Levin is the root of that web.

### Retain / Do not confuse

Retain: SAT is NP-complete because it is efficiently verifiable and every NP computation can be encoded as a satisfiability instance.

Do not confuse: NP-completeness is about relative hardness under reductions, not about proving absolute lower bounds.

---

# 16. Why CNF and 3-SAT often appear after Cook-Levin

Many presentations of Cook-Levin prove that SAT is NP-complete, then quickly move to CNF-SAT or 3-SAT. This can make it seem as if the theorem depends on a special formula format. It does not. The core theorem is the computation-to-formula encoding. Normal forms are later refinements.

## 16.1 The object being introduced: conjunctive normal form

A formula is in conjunctive normal form, or CNF, if it is an AND of clauses, where each clause is an OR of literals. A literal is either a variable or the negation of a variable.

CNF is useful because the Cook-Levin constraints naturally look like conjunctions of local requirements. Each requirement can often be written as a clause, and the whole formula is an AND of those clauses.

### Formal definition: CNF-SAT and 3-SAT

A Boolean formula is in CNF if it has the form

$$
C_1 \land C_2 \land \cdots \land C_m,
$$

where each $C_j$ is a disjunction of literals.

In 3-CNF, each clause has exactly three literals, or at most three literals depending on the convention. The problem 3-SAT asks whether a given 3-CNF formula is satisfiable.

### Interpretation

CNF makes constraints explicit. Each clause is a condition that must be satisfied. A satisfying assignment must satisfy every clause simultaneously.

3-SAT is more restrictive than SAT, but still NP-complete. The restriction is strong enough to make reductions cleaner, yet not so strong that it destroys expressive power.

### Assumptions and boundary conditions

A long clause can be transformed into an equisatisfiable collection of shorter clauses by introducing auxiliary variables. This transformation preserves satisfiability, though not necessarily logical equivalence over the original variables in the strongest possible sense. It is enough for reductions because reductions need yes/no preservation.

The conversion must be polynomial size. Standard transformations satisfy this requirement.

### Fully worked example: why auxiliary variables are acceptable

Suppose a construction produces the long clause

$$
(a \lor b \lor c \lor d \lor e).
$$

To express this using clauses of size at most three, one may introduce new variables that represent partial progress through the disjunction. The exact transformation is less important here than the principle: the new variables do not change whether the original clause can be satisfied; they merely allow the same satisfiability condition to be represented with smaller clauses.

This example is chosen because it addresses a common worry. Adding variables may seem like changing the problem, but reductions are allowed to introduce auxiliary variables as long as satisfiability is preserved.

### Misconception: 3-SAT is not obviously easier because its clauses are shorter

Shorter clauses impose more structured constraints, but the problem remains NP-complete. The difficulty comes from satisfying many interacting constraints simultaneously, not from individual clauses being long.

### Connection to later material

Many classic NP-completeness proofs start from 3-SAT rather than SAT because the uniform clause size makes gadgets easier to design. Cook-Levin supplies the original source of hardness; the SAT-to-3-SAT conversion supplies a convenient normal form.

### Retain / Do not confuse

Retain: Cook-Levin's core proof is about encoding computations as formulas. CNF and 3-SAT are useful refinements.

Do not confuse: Equisatisfiability is enough for reductions. The transformed formula need not preserve every logical feature of the original formula.

---

# 17. Common failure modes in understanding the proof

Cook-Levin is conceptually simple once the main objects are in place, but the proof has several layers. Misunderstanding usually comes from collapsing those layers.

## 17.1 Confusing the machine, the input, and the formula

The machine $M$ is fixed for the language $L$. The input $w$ is the instance being tested. The formula $\Phi_{M,w}$ is constructed from both, but only $w$ varies across instances of the reduction for a fixed language.

If this distinction is lost, the theorem can sound like it builds one formula for an entire language. It does not. It builds one formula per input instance.

## 17.2 Confusing a computation path with a computation tree

A nondeterministic machine may have many branches. The tableau encodes one branch. SAT's existential assignment chooses the branch implicitly. The proof does not need to write the whole nondeterministic tree.

## 17.3 Confusing local consistency with weak checking

The move constraints are local, but not weak. They are local because the computational model is local. Every illegal global transition creates some illegal local symptom, and the formula forbids all such symptoms.

## 17.4 Confusing satisfiability with truth under all assignments

SAT asks whether there exists a satisfying assignment. It is not asking whether the formula is true under every assignment. The formula is designed so that satisfying assignments correspond to accepting histories. Most assignments will not satisfy it, just as most random tables are not valid accepting computations.

## 17.5 Confusing the theorem with a practical SAT encoding recipe

Cook-Levin is a theoretical polynomial-time reduction. It is not designed to produce compact practical SAT instances. Modern SAT encodings for real verification tasks often use more efficient representations. The theorem's purpose is universality and complexity classification, not engineering efficiency.

---

# 18. The proof in one coherent pass

The Cook-Levin proof can now be read as a single chain of necessity.

We want to prove SAT is NP-complete. SAT is in NP because a truth assignment is an efficiently checkable certificate.

To prove NP-hardness, take an arbitrary language $L \in NP$. Because $L$ is in NP, there is a nondeterministic polynomial-time Turing machine $M$ deciding it. For an input $w$, acceptance means there exists an accepting computation branch of length at most $T=p(|w|)$.

A branch of computation can be displayed as a tableau with polynomially many rows and columns. Each row is a configuration; each cell records either a tape symbol or a state-symbol pair that marks the head and current state.

Introduce variables $X_{t,i,c}$ saying that cell $(t,i)$ contains content $c$. Then build a formula with four responsibilities. Cell constraints make each cell contain exactly one content. Start constraints force row $0$ to be the initial configuration on $w$. Accept constraints require an accepting state. Move constraints forbid illegal local windows between adjacent rows.

The formula is polynomial size because the tableau is polynomial size and every local check has constant size. The formula is satisfiable exactly when there exists a valid accepting tableau. Such a tableau exists exactly when $M$ accepts $w$. Therefore $w \in L$ exactly when $\Phi_{M,w}$ is satisfiable.

Since every language in NP reduces to SAT, SAT is NP-hard. Since SAT is in NP, SAT is NP-complete.

---

# Final retention map

The Cook-Levin proof is best retained as a sequence of roles rather than as a memorized list of clauses.

The role of NP is to provide an existential polynomial-time computation.

The role of the nondeterministic Turing machine is to give a precise, local model of that computation.

The role of the tableau is to lay one possible computation branch out as a finite static object.

The role of the variables is to let a Boolean assignment choose the contents of the tableau.

The role of the constraints is to make sure the chosen tableau is well-formed, starts correctly, evolves legally, and accepts.

The role of the correctness proof is to show exact correspondence: accepting computations give satisfying assignments, and satisfying assignments give accepting computations.

The role of the size analysis is to show that this correspondence is achieved by a polynomial-time reduction.

The theorem matters because it turns SAT into the first universal NP problem. Once this is known, SAT becomes the starting point for much of complexity theory: to prove a new problem NP-hard, it is enough to show that SAT, or a known NP-complete problem derived from SAT, reduces to it.
