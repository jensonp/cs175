
# Constraint Satisfaction Problems, Search, Optimization, and Complexity

## Source and scope

These notes are a mastery-oriented teaching chapter built from the uploaded lecture on Constraint Satisfaction Problems together with the writing brief that requested deep, self-contained course notes rather than a summary. The lecture introduces the core CSP model, examples such as map coloring, Sudoku, Wordle, Minesweeper, Traveling Salesman, backtracking, local search, and objective functions, and it briefly touches Boolean satisfiability and WalkSAT. These notes preserve that scope but expand it substantially, especially on the foundational complexity ideas that were requested explicitly: **P, NP, NP-hard, NP-complete, reductions, decision versus search versus optimization, and how CSPs relate to SAT and TSP**.

---

# 1. Why constraint satisfaction problems exist

Constraint satisfaction problems appear because plain search is too weak a language for many problems, and plain algebra is too narrow.

Suppose you are given a puzzle, a schedule, a routing task, or a logic problem. The problem does not usually ask, “What path through actions should I take?” Instead, it asks something closer to: “Assign values to a collection of unknowns so that all the rules are obeyed.” In Sudoku, the unknowns are cell values. In map coloring, the unknowns are region colors. In scheduling, the unknowns are times, rooms, and resource assignments. In SAT, the unknowns are truth values. In Minesweeper, the unknowns are whether hidden frontier cells contain mines. In all of these, the central object is not a path but an **assignment**. The challenge is not just that there are many assignments. The challenge is that the rules couple variables together, so choosing one value often restricts many others.

This section exists because before we can talk about search algorithms, local inference, tractability, or complexity classes, we need a language for describing the problem itself. Without such a language, we are forced to treat every problem as a special case. The CSP framework gives a shared vocabulary: variables, domains, constraints, assignments, consistency, and solutions. Once that language is in place, general-purpose reasoning methods become possible.

## The object being introduced

A **constraint satisfaction problem** is a mathematical model for a situation in which we have unknown quantities, each quantity can take values from some allowed set, and not every combination of values is acceptable. The model answers the question:

> Can we choose one value for each variable so that every rule is satisfied?

What is fixed:
- the set of variables,
- the domain of each variable,
- the set of constraints.

What varies:
- the assignment of values to variables.

What conclusion the model allows:
- whether a satisfying assignment exists,
- what one such assignment is,
- in extended settings, which satisfying assignment is best according to some objective.

## Formal definition

A **constraint satisfaction problem (CSP)** consists of:

1. A finite set of variables  
   \[
   X = \{X_1, X_2, \dots, X_n\}.
   \]

2. For each variable \(X_i\), a nonempty domain \(D_i\) of values that \(X_i\) may take.

3. A finite set of constraints  
   \[
   C = \{C_1, C_2, \dots, C_m\}.
   \]

Each constraint \(C_j\) has:
- a **scope**, which is an ordered tuple or set of variables that participate in the constraint;
- a **relation** or **content**, which specifies which combinations of values for those variables are allowed.

An **assignment** is a mapping that gives values to some or all variables. A **complete assignment** assigns a value to every variable. A **solution** is a complete assignment that satisfies all constraints.

## Interpretation

This definition is simple, but it is doing a great deal of conceptual work.

The variables are the things we are trying to determine. The domains describe the legal possibilities for each variable before considering interactions. Constraints encode interactions. A domain says, “What could this variable be on its own?” A constraint says, “What combinations are allowed together?” That difference is foundational. If you lose it, CSPs become confusing very quickly.

The word “scope” matters because a constraint rarely talks about the whole problem. It usually talks about only a few variables at a time. That local structure is what makes inference possible. If every constraint involved every variable, we would lose much of the leverage that CSP algorithms depend on.

## Boundary conditions, assumptions, and failure modes

Several hidden assumptions are worth surfacing immediately.

First, the standard introductory CSP assumes a **finite** set of variables and finite domains. Many real systems involve continuous values, but the classical CSP framework in AI is most comfortable in the finite case.

Second, a CSP by itself is a **feasibility** problem, not yet an optimization problem. The question is whether there exists an assignment satisfying all constraints. If we later add preferences or costs, we move into constraint optimization.

Third, the framework is neutral about how constraints are represented. A constraint may be given extensionally by listing all allowed tuples, or intensionally by a formula or test such as \(X_i \neq X_j\). This matters computationally: the same mathematics can be much easier or harder to process depending on representation.

Fourth, “satisfying all constraints” is absolute in the basic model. There is no notion yet of “mostly satisfying” or “best trade-off.” Students sometimes import that idea too early because many real problems do involve preferences. Keep the distinction sharp: basic CSPs are about hard constraints.

## Fully worked example: map coloring

This example is chosen because it is the cleanest place to see the distinction between variables, domains, and constraints without the arithmetic distractions of more complicated puzzles.

Suppose a map has regions \(A, B, C, D\), and suppose adjacent regions must receive different colors. Let the colors be \(\{red, green, blue\}\).

### Setup

Variables:
\[
X = \{A, B, C, D\}.
\]

Domains:
\[
D_A = D_B = D_C = D_D = \{red, green, blue\}.
\]

Constraints:
- \(A \neq B\),
- \(A \neq C\),
- \(B \neq C\),
- \(B \neq D\).

### What is being checked

A complete assignment must pick one color for each region. To test whether an assignment is a solution, we inspect each adjacency constraint in turn.

Take the assignment:
\[
A = red,\quad B = green,\quad C = blue,\quad D = red.
\]

Check the constraints in order.

1. Check \(A \neq B\).  
   Here \(A = red\) and \(B = green\). They are different, so this constraint is satisfied.

2. Check \(A \neq C\).  
   Here \(A = red\) and \(C = blue\). Different again, so this is satisfied.

3. Check \(B \neq C\).  
   Here \(B = green\) and \(C = blue\). Satisfied.

4. Check \(B \neq D\).  
   Here \(B = green\) and \(D = red\). Satisfied.

Since all constraints are satisfied, this is a solution.

Now compare with:
\[
A = red,\quad B = red,\quad C = green,\quad D = blue.
\]

The first check already fails: \(A \neq B\) is false because both are red. That single failed constraint is enough to conclude the assignment is not a solution. We do not need to continue.

### Final interpretation

The example teaches the core pattern of all CSPs. A solution is not “a good guess.” It is not “mostly okay.” It is a complete assignment that survives every constraint check. The role of algorithms is to avoid enumerating all assignments blindly.

## Misconception block

**Do not confuse a domain restriction with a constraint.**

If a country may use only \(\{red, green\}\), that is a domain fact. If two countries must have different colors, that is a constraint. Domain restrictions are unary information about one variable. Constraints are relational information tying variables together.

## Connection to later material

Everything that comes later depends on this model. Backtracking search will explore partial assignments. Inference methods will try to shrink domains before a contradiction becomes unavoidable. Local search will allow complete assignments that violate constraints and try to repair them. Complexity theory will ask how hard it is, in the worst case, to decide whether a CSP has a solution. SAT and 3-SAT will turn out to be special cases of the same broad assignment-under-constraints template.

## Retain / Do not confuse

Retain:
- A CSP is about assigning values to variables under rules.
- Domains describe legal individual values.
- Constraints describe legal combinations.
- A solution is a complete assignment satisfying every constraint.

Do not confuse:
- unary restrictions with relational constraints,
- a complete assignment with a satisfying assignment,
- feasibility with optimization.

---

# 2. Assignments, partial information, and the logic of search

The previous section gave the model. This section exists because the moment we try to solve a CSP, we face a new question: how do we reason before a full assignment is known? Real algorithms do not usually jump directly to a complete assignment. They build one piece by piece. So we need a precise understanding of **partial assignments**, what it means for them to be consistent, and why local consistency is weaker than global solvability.

## The object being introduced

A **partial assignment** is an incomplete proposed solution. It fixes values for some variables and leaves the rest open. This object matters because systematic search moves through the space of partial assignments, not directly through the space of complete ones.

What is fixed:
- the CSP itself,
- which subset of variables has already been assigned.

What varies:
- which variables are assigned,
- what values they are assigned,
- whether that partial information can still be extended to a full solution.

What conclusion partial assignments allow:
- whether we can safely continue extending,
- whether we should backtrack immediately,
- whether local evidence has already made success impossible.

## Formal definition

A **partial assignment** is a mapping
\[
\alpha : S \to \bigcup_i D_i
\]
where \(S \subseteq \{X_1,\dots,X_n\}\), and for each \(X_i \in S\), \(\alpha(X_i) \in D_i\).

A partial assignment is **locally consistent** if every constraint whose entire scope lies inside \(S\) is satisfied by the assigned values.

A partial assignment is **extendable** if there exists a complete satisfying assignment that agrees with it on all already assigned variables.

## Interpretation

The key distinction is between being **locally consistent now** and being **extendable later**. A partial assignment can satisfy every constraint that is currently checkable and still be doomed. Why? Because some contradictions involve variables that have not yet all been assigned. Local consistency only checks constraints that are already fully instantiated. Extendability asks a stronger question: can the remaining unassigned variables be chosen in a way that rescues the current choices?

That gap is exactly why CSP solving is hard. If local consistency always implied extendability, search would be easy. But in general it does not.

## Boundary conditions, assumptions, and failure modes

The phrase “constraints whose entire scope lies inside \(S\)” matters. If a binary constraint involves one assigned variable and one unassigned variable, it is not yet fully testable in the strict sense of satisfaction. However, it may still allow pruning by inference, which is different from declaring success or failure outright.

A common failure mode in reasoning is this: students check only currently instantiated constraints, find no violation, and conclude that the current branch is promising. That is too strong. All they have shown is that the branch has not yet been refuted.

## Fully worked example: locally consistent but not extendable

This example is chosen because it isolates the difference between local consistency and actual solvability.

Let the variables be \(X, Y, Z\), each with domain \(\{1,2\}\), and constraints:
- \(X \neq Y\),
- \(Y \neq Z\),
- \(X = Z\).

Consider the partial assignment:
\[
X = 1,\quad Y = 2.
\]

### What is being checked

The assigned set is \(S = \{X,Y\}\). The constraint \(X \neq Y\) is fully inside \(S\), so we must check it. Since \(1 \neq 2\), it is satisfied.

The constraint \(Y \neq Z\) is not fully inside \(S\) because \(Z\) is not assigned yet. The constraint \(X = Z\) is also not fully inside \(S\). So by the definition above, the partial assignment is locally consistent.

Now ask the stronger question: can it be extended?

### Extension check

Because \(X = 1\) and \(X = Z\), any extension must set \(Z = 1\).

But because \(Y = 2\) and \(Y \neq Z\), setting \(Z = 1\) is actually fine. So this one is extendable.

Now instead consider:
\[
X = 1,\quad Y = 1.
\]

Immediately \(X \neq Y\) fails, so the assignment is not even locally consistent.

More interesting is a second problem with constraints:
- \(X \neq Y\),
- \(Y \neq Z\),
- \(Z \neq X\),
and domains still \(\{1,2\}\).

Take the partial assignment:
\[
X = 1,\quad Y = 2.
\]

This is locally consistent because \(X \neq Y\) holds. But can it be extended? The only remaining variable is \(Z\). It must satisfy:
- \(Z \neq Y = 2\), so \(Z\) must be \(1\),
- \(Z \neq X = 1\), so \(Z\) must be \(2\).

These requirements are incompatible. Therefore the partial assignment is locally consistent but not extendable.

### Final interpretation

This is the fundamental search hazard. The branch looks fine when inspected locally, but no full solution exists beneath it. Good CSP algorithms try to discover such dead ends as early as possible.

## Misconception block

**A partial assignment with no current violations is not the same thing as a promising partial assignment.**

It may merely be a contradiction that has not yet become visible.

## Connection to later material

Backtracking explores partial assignments. Forward checking and arc consistency try to detect non-extendability earlier by reasoning about unassigned variables. Complexity theory later explains why no polynomial-time method is known that can perfectly determine extendability in every general case.

## Retain / Do not confuse

Retain:
- Partial assignments are the states of systematic CSP search.
- Local consistency means no violated fully-instantiated constraints.
- Extendability is a stronger property than local consistency.

Do not confuse:
- “not yet contradicted” with “can be extended to a solution.”

---

# 3. Constraint languages, scopes, and representations

This section exists because not all constraints behave the same way computationally. Two CSPs may look similar at a high level yet differ dramatically in difficulty because of how their constraints are expressed and how many variables each one couples together. To understand later algorithms, we need more precise language for unary, binary, and higher-arity constraints, and for explicit versus implicit representations.

## The object being introduced

A **constraint** is a relation over the domains of variables in its scope. It is not merely a sentence in English and not merely an equation. It is a rule that classifies tuples as allowed or forbidden.

What is fixed:
- the scope of the constraint,
- the criterion for which tuples are allowed.

What varies:
- the tuple of values plugged into the scoped variables.

What conclusion it allows:
- whether a given local tuple is admissible.

## Formal definition

If a constraint \(C\) has scope \((X_{i_1}, \dots, X_{i_k})\), then its relation is a subset
\[
R_C \subseteq D_{i_1} \times \cdots \times D_{i_k}.
\]
A tuple \((a_1,\dots,a_k)\) satisfies \(C\) if and only if
\[
(a_1,\dots,a_k) \in R_C.
\]

A constraint is:
- **unary** if \(k=1\),
- **binary** if \(k=2\),
- **\(k\)-ary** in general if it involves \(k\) variables,
- **global** informally if it has a structured meaning over many variables, such as all-different.

## Interpretation

This definition says that a constraint is best thought of as a filter on tuples. The scope tells you which variables matter. The relation tells you which combinations pass. This is more precise than writing “\(X \neq Y\)” and moving on, because it explains what a constraint really is under the hood: a set of admissible local configurations.

Unary constraints shrink domains. Binary constraints create pairwise compatibility conditions. Higher-arity constraints encode interactions that cannot always be decomposed cleanly into binary pieces without changing problem structure or computational cost.

## Boundary conditions, assumptions, and failure modes

A frequent temptation is to convert every problem to binary constraints. Sometimes this is useful, but it can also introduce extra variables and obscure structure. For example, a global all-different constraint in Sudoku is more informative than a naïve set of pairwise inequalities if one wants strong propagation. Representation is not cosmetic. It affects what algorithms can infer efficiently.

Another point: a relation can be represented explicitly by listing allowed tuples, or implicitly by a condition such as “the sum equals 3” or “all values are distinct.” Explicit tables are concrete but can be huge. Implicit relations are compact but may require specialized procedures for efficient reasoning.

## Fully worked example: Sudoku and all-different

This example is chosen because it shows why higher-level constraint language matters.

In a standard 9-by-9 Sudoku, each cell is a variable. Let \(X_{r,c}\) denote the value in row \(r\), column \(c\), where \(1 \le r \le 9\) and \(1 \le c \le 9\). Each domain is initially \(\{1,\dots,9\}\), except clues, whose domains may be singleton sets.

One row constraint can be expressed as:
\[
all\text{-}different(X_{1,1}, X_{1,2}, \dots, X_{1,9}).
\]

### What is being checked

The object here is not nine separate facts but one structured relation over nine variables. A tuple is allowed exactly when all nine entries are distinct.

Take a candidate row assignment:
\[
(2,4,6,1,3,5,7,8,9).
\]
Each value lies in \(\{1,\dots,9\}\), and no value repeats. So this tuple satisfies the row constraint.

Now consider:
\[
(2,4,6,1,3,5,7,8,8).
\]
The last two entries repeat 8, so the tuple is not in the all-different relation. The row constraint is violated.

### Why the example matters

You could replace the row all-different relation by all pairwise inequalities:
\[
X_{1,i} \neq X_{1,j}\quad \text{for all } i<j.
\]
This captures the same satisfying set, but it loses the fact that these inequalities belong to one collective structure. Stronger inference procedures can exploit that global structure more effectively than treating the row as just a bag of separate binary constraints.

## Misconception block

**Do not think of a constraint as only an equation.**

A constraint can be inequality, membership in a table of allowed tuples, a counting condition, a global pattern like all-different, or any relation that can decide whether a tuple is allowed.

## Connection to later material

Forward checking and arc consistency often work at the level of binary compatibility, while stronger propagation can exploit global constraints. SAT will later be expressed in terms of clauses, which are also constraints. Complexity classifications often depend not just on the existence of constraints, but on their arity and language.

## Retain / Do not confuse

Retain:
- A constraint is a relation over the variables in its scope.
- Scope says which variables matter.
- Relation says which tuples are allowed.
- Representation affects computational behavior.

Do not confuse:
- the logical notation of a constraint with the mathematical object it denotes,
- pairwise decomposition with preserving full structural strength.

---

# 4. Canonical examples and what each one teaches

This section exists because abstract definitions are not enough for mastery. A serious student needs to see what structural pattern each classic example illustrates. Examples are not decoration. They are part of the theory because they reveal which modeling choices matter.

## 4.1 Map coloring

### Why this subsection exists

Map coloring is the simplest clean example of binary constraints. It teaches the CSP language with minimal distraction.

### The object being introduced

A graph-coloring CSP has one variable per region or node, a small color domain, and binary inequality constraints on adjacent pairs. It answers whether a legal coloring exists.

### Formal model

For graph \(G=(V,E)\) and color set \(K\), define one variable \(X_v\) for each \(v \in V\), domain \(D_v = K\), and for every edge \((u,v)\in E\), a constraint
\[
X_u \neq X_v.
\]

### Interpretation

This is a pure compatibility problem: adjacent objects cannot share a label.

### Worked example

Take triangle graph with vertices \(A,B,C\), and color set \(\{red,green\}\). The constraints are
\[
A \neq B,\quad B \neq C,\quad C \neq A.
\]

Assign \(A=red\). Then \(B\) must be green. Then \(C\) must be different from \(B\), so \(C=red\). But now \(C=A\), violating \(C \neq A\). The same contradiction arises if \(A=green\). So the graph is not 2-colorable.

This teaches a general lesson: odd cycles obstruct 2-colorability. The CSP language makes that structural fact visible as unavoidable inequality pressure around a cycle.

### Misconception block

A graph-coloring CSP is not about “guessing colors nicely.” It is exactly a feasibility problem over discrete labels with pairwise incompatibilities.

### Connection to later material

Graph coloring is a standard NP-complete decision problem when the number of colors is part of the input in the right way. It also serves as a prototype for scheduling, register allocation, and resource conflicts.

### Retain / Do not confuse

Retain:
- map coloring is binary CSP structure in its cleanest form.

Do not confuse:
- graphical adjacency with geometric distance or aesthetics.

## 4.2 Sudoku

### Why this subsection exists

Sudoku teaches how a puzzle with strong human familiarity becomes a CSP with many variables and highly structured constraints.

### The object being introduced

Each cell is a variable. Each variable has domain \(\{1,\dots,9\}\) unless fixed by a clue. Constraints enforce distinctness across rows, columns, and 3-by-3 blocks.

### Formal model

Variables:
\[
X_{r,c},\quad 1 \le r,c \le 9.
\]

Domains:
\[
D_{r,c} \subseteq \{1,\dots,9\},
\]
where clues use singleton domains.

Constraints:
- each row is all-different,
- each column is all-different,
- each 3-by-3 block is all-different.

### Interpretation

Sudoku is not arithmetic. The digits are labels subject to distinctness requirements. Their numerical meaning matters far less than the fact that they are nine distinct symbols.

### Fully worked example

Suppose in one row the current state is:
\[
(2, \_, 4, \_, 6, \_, \_, \_, \_).
\]
The missing values are \(\{1,3,5,7,8,9\}\).

Take the empty position in column 2. Suppose the column already contains \(\{8,6,5,1\}\), and the 3-by-3 block already contains \(\{2,4,8\}\).

Now check the possible values in order.

- Start from row-allowed set \(\{1,3,5,7,8,9\}\).
- Remove values already present in the column: remove \(8,6,5,1\). Only \(6\) was not row-allowed, so removing column conflicts leaves \(\{3,7,9\}\).
- Remove values already present in the block: remove \(2,4,8\). None of these are in \(\{3,7,9\}\), so the remaining domain stays \(\{3,7,9\}\).

So the local reasoning concludes that this cell cannot yet be fixed, but its domain has shrunk from 9 values to 3. That is exactly the kind of domain reduction CSP inference lives on.

### Misconception block

Sudoku solving is not fundamentally about adding, subtracting, or parity. It is about structured constraint propagation plus search when propagation stalls.

### Connection to later material

Sudoku is a natural testbed for backtracking, forward checking, and arc consistency. It also illustrates the difference between human-style deduction and general-purpose CSP algorithms.

### Retain / Do not confuse

Retain:
- Sudoku is a CSP of distinctness, not arithmetic.
- Clues become singleton domains.
- Inference reduces domains before search commits values.

Do not confuse:
- a reduced domain with a solved variable.

## 4.3 Minesweeper

### Why this subsection exists

Minesweeper is valuable because it shows that CSPs are not only about symbolic labels. They can also encode local counting constraints over binary variables.

### The object being introduced

Frontier cells become binary variables:
- 1 means mine,
- 0 means no mine.

Each revealed numbered cell imposes a sum constraint over neighboring hidden variables.

### Formal model

For each relevant hidden frontier cell \(v\), introduce a variable \(X_v \in \{0,1\}\).

For each revealed numbered cell \(c\), let \(N(c)\) be the set of hidden neighboring frontier cells and let \(L(c)\) be the effective label after subtracting already-marked mines. Then impose:
\[
\sum_{v \in N(c)} X_v = L(c).
\]

### Interpretation

This is a beautiful modeling move. A visual puzzle becomes a linear counting CSP over binary variables. The numbers on the board are not probabilities. They are exact local equations.

### Fully worked example

Suppose a revealed cell has effective label 1 and has exactly two adjacent hidden frontier variables \(X\) and \(Y\). The constraint is
\[
X + Y = 1,\qquad X,Y \in \{0,1\}.
\]

Check the possible pairs:
- \((0,0)\): sum is 0, so disallowed.
- \((0,1)\): sum is 1, allowed.
- \((1,0)\): sum is 1, allowed.
- \((1,1)\): sum is 2, disallowed.

So the constraint says exactly one of the two neighboring cells is a mine.

Now suppose a second adjacent clue forces \(Y=0\). Then the first constraint immediately implies \(X=1\). This illustrates the general pattern: local equations combine, and one domain reduction can trigger another.

### Misconception block

A Minesweeper clue does not say “probably one nearby mine.” It says exactly one, after accounting for already identified mines. The uncertainty comes from not knowing which variable assignments realize the equation.

### Connection to later material

Minesweeper illustrates backtracking over binary variables and local constraint checks. It also connects naturally to NP-completeness discussions, because generalized Minesweeper decision problems are computationally hard.

### Retain / Do not confuse

Retain:
- Minesweeper is a binary CSP with counting constraints.

Do not confuse:
- exact clue equations with probabilistic guesses.

## 4.4 Wordle

### Why this subsection exists

Wordle is useful because it demonstrates that a CSP model can coexist with information-gathering strategy. It is not only about satisfying known constraints, but about choosing actions that generate useful future constraints.

### The object being introduced

One can model the unknown word as a tuple of character variables and convert feedback patterns into constraints on positions and letter counts.

### Interpretation

Wordle is not a pure static CSP because the constraints are revealed gradually through guesses. Each guess acts like an experiment. That makes the game a bridge between CSP reasoning and decision-making under information gain.

### Worked example

Suppose the hidden word has 5 positions \(X_1,\dots,X_5\). Start with domains equal to the alphabet. After guessing a word, feedback imposes constraints.

If position 2 gets green on letter \(A\), then:
\[
X_2 = A.
\]
The domain of \(X_2\) collapses to \(\{A\}\).

If position 4 gets yellow on letter \(R\), then:
- \(X_4 \neq R\),
- at least one of the other positions must contain \(R\), subject to count rules.

If a letter receives gray in a context where no duplicate-count complication is present, that letter can be removed from all positions.

The general lesson is that domains and cross-position constraints are updated after every round, and a good next guess may be chosen not only for consistency with the current possibilities, but for its expected information gain.

### Misconception block

Wordle feedback is not just a set of independent positional facts. Repeated letters make the constraints about counts as well as positions.

### Connection to later material

Wordle provides intuition for entropy-guided search, information gain, and the broader idea that solving can involve both consistency maintenance and strategic query selection.

### Retain / Do not confuse

Retain:
- Wordle can be modeled as variables, domains, and feedback-induced constraints.

Do not confuse:
- “yellow” with “this position has the letter,”
- gray-letter logic with the simpler no-duplicate case only.

---

# 5. Systematic search: why backtracking is the baseline

This section exists because once the CSP model is defined, the most direct solution method is to construct assignments step by step and undo decisions when they lead to contradiction. This is the baseline general-purpose method for finite CSPs. Everything more sophisticated should be understood first as an attempt to make backtracking fail earlier, branch less, or infer more.

## The object being introduced

**Backtracking search** is a depth-first exploration of the space of partial assignments. At each step, one unassigned variable is chosen, a value from its current domain is tentatively assigned, and the resulting partial assignment is checked for consistency. If a contradiction is found, the algorithm returns to the previous decision point and tries another value.

What is fixed:
- the CSP,
- the current partial assignment,
- the set of unassigned variables.

What varies:
- which variable is chosen next,
- which value is tried,
- how much inference is done after the choice.

What conclusion it allows:
- whether a branch can still possibly contain a solution.

## Formal definition

At the conceptual level, backtracking search operates on states that are partial assignments. A transition extends the current assignment by assigning one previously unassigned variable. A branch is abandoned when the partial assignment is inconsistent with the constraints.

## Interpretation

The crucial point is that backtracking does **not** enumerate all complete assignments independently. It reuses partial work. That is why it is already better than blind enumeration. If a contradiction appears after assigning the first five variables, there is no need to complete the remaining hundred variables on that branch. The branch is already dead.

## Boundary conditions, assumptions, and failure modes

Backtracking is complete for finite CSPs: if a solution exists, it will eventually find one; if none exists, it will eventually prove failure. But “eventually” can still mean exponential time in the worst case.

Another subtlety: the meaning of “check consistency” depends on what inference is bundled into the step. The minimal version checks only whether any fully instantiated constraint is violated. More advanced versions run forward checking or maintain arc consistency after each assignment.

## Fully worked example: backtracking on a small map

This example is chosen because the branching structure is easy to visualize.

Variables: \(A,B,C\), domain \(\{red, green\}\), constraints:
- \(A \neq B\),
- \(B \neq C\),
- \(A \neq C\).

This is the triangle again.

### Step-by-step reasoning

Start with no assignments.

1. Choose \(A\).  
   Try \(A = red\). No constraint is yet violated because every constraint involving \(A\) also involves an unassigned variable.

2. Choose \(B\).  
   Try \(B = red\). Now check \(A \neq B\). This fails because both equal red. So this branch is impossible. Backtrack within the choices for \(B\).

3. Try the next value for \(B\): \(B = green\).  
   Check \(A \neq B\). This now holds. Continue.

4. Choose \(C\).  
   Try \(C = red\).  
   Check \(B \neq C\): green versus red, so okay.  
   Check \(A \neq C\): red versus red, so fail. Reject this value.

5. Try \(C = green\).  
   Check \(B \neq C\): green versus green, fail.

Now \(C\) has no values left, so backtrack to \(B\). But \(B\) has no values left besides the two already tried, so backtrack to \(A\).

6. Try the next value for \(A\): \(A = green\).  
   The symmetric reasoning repeats and also fails.

Conclusion: no solution exists.

### What each check means

At each assignment, the search checks the constraints that have become testable. A failed check means not merely “this value is poor,” but “no completion beneath this partial assignment can work.”

### Final interpretation

Backtracking does not need to see every full coloring to know the triangle is not 2-colorable. It detects impossibility at the earliest moment each contradiction becomes visible.

## Misconception block

**Backtracking is not the same as brute-force enumeration of all full assignments.**

It is still exponential in the worst case, but it cuts off branches as soon as they become impossible.

## Connection to later material

Variable ordering, value ordering, and constraint propagation all exist to improve backtracking. Branch-and-bound will later extend the same depth-first structure to optimization problems.

## Retain / Do not confuse

Retain:
- Backtracking explores partial assignments depth-first.
- Contradictions prune whole subtrees.
- It is complete but can still be exponentially slow.

Do not confuse:
- a depth-first systematic search with local search over complete states.

---

# 6. Why backtracking can still be hard: future constraints and delayed failure

This section exists because students often understand backtracking mechanically but not intellectually. They know the procedure, yet they do not see why it can still waste enormous time. The core reason is delayed failure: a partial assignment can look harmless locally while being globally doomed.

## The object being introduced

The key object here is the distinction between:
- constraints involving only already assigned variables,
- constraints involving one or more future variables.

The problem is that future constraints can hide contradictions until deep in the search tree.

## Interpretation

When backtracking extends a partial assignment, it knows only part of the future. A bad early choice may not trigger any immediate violation, even though it leaves no possible values for some variable far downstream. The later that impossibility becomes visible, the more search effort is wasted.

## Boundary conditions, assumptions, and failure modes

This issue becomes severe when constraints are sparse but highly interacting, or when domains are large enough that locally harmless choices still cause long-range trouble.

A common overgeneralization is to think that “small local checks” are all that matter. In fact, CSP solving is often about turning future contradictions into present contradictions.

## Fully worked example: why order matters

Take variables \(X,Y,Z,W\), all with domain \(\{1,2,3\}\), and constraints:
- \(X = Y\),
- \(Y = Z\),
- \(Z = W\),
- \(X \neq W\).

### What the structure says

The first three constraints force all four variables to have the same value if the assignment is complete. But the last constraint says the first and last must differ. Therefore no solution exists.

### What happens in naïve backtracking

Suppose the search order is \(X, Y, Z, W\).

1. Assign \(X=1\). No contradiction yet.
2. Assign \(Y=1\). Satisfies \(X=Y\).
3. Assign \(Z=1\). Satisfies \(Y=Z\).
4. Assign \(W=1\). Satisfies \(Z=W\), but now violates \(X \neq W\).

The contradiction appears only after the fourth variable.

If instead one had stronger inference, then as soon as \(X=1\), the chain of equalities would force \(W=1\), which immediately clashes with \(X \neq W\). The dead branch could be detected much earlier.

### Final interpretation

The entire purpose of look-ahead and propagation is to make this kind of impossibility visible sooner.

## Misconception block

A problem can be hard for backtracking not because each local check is expensive, but because contradictions may surface only after many locally legal steps.

## Connection to later material

Forward checking and arc consistency will now make conceptual sense: they are tools for anticipating failure instead of waiting passively for it.

## Retain / Do not confuse

Retain:
- Backtracking suffers when failure is delayed.
- Future constraints are the source of hidden dead ends.

Do not confuse:
- “cheap local checks” with “easy problem.”

---

# 7. Inference and propagation: making contradictions appear earlier

This section exists because search alone is too passive. If we merely assign values and wait for explicit violations, we often discover dead ends too late. Inference procedures actively reason about what current assignments imply for remaining domains.

## The object being introduced

**Constraint propagation** takes a partial assignment or a set of current domains and removes values that can no longer participate in any solution consistent with the current information.

What is fixed:
- the current CSP state,
- already made assignments,
- current domains.

What varies:
- which unsupported values are removed,
- whether any domain becomes empty.

What conclusion it allows:
- whether the current branch is already impossible,
- which future choices remain viable.

## Formal definition

A propagation procedure is a sound domain-reduction process: it removes values from domains only when those values cannot occur in any solution extending the current state.

Two foundational forms are:
- **forward checking**,
- **arc consistency**.

## Interpretation

Propagation is not guessing. It is deduction. It does not say which value must be chosen next unless a domain becomes singleton. It says which values are no longer possible.

## 7.1 Forward checking

### Why this subsection exists

Forward checking is the simplest look-ahead idea. It is the first serious improvement over raw backtracking because it inspects the immediate consequences of the latest assignment on future variables.

### The object being introduced

After assigning one variable, forward checking looks at every neighboring unassigned variable and deletes domain values that are now incompatible with the new assignment.

### Formal definition

Suppose variable \(X\) is assigned value \(a\). For each unassigned variable \(Y\) sharing a constraint with \(X\), remove from \(D_Y\) every value \(b\) such that the pair \((a,b)\) violates the relevant constraint between \(X\) and \(Y\). If any domain becomes empty, the current branch fails immediately.

### Interpretation

Forward checking answers the question: **given what I just committed to, which future values became impossible right away?**

It is strictly stronger than doing nothing, but weaker than full arc consistency, because it only reacts to the latest assignment and only one step ahead.

### Worked example

This example is chosen because the domain deletion is transparent.

Variables \(A,B,C\), each with domain \(\{red,green,blue\}\). Constraints:
- \(A \neq B\),
- \(A \neq C\).

Assign \(A = red\).

Now forward checking inspects neighbors \(B\) and \(C\).

- For \(B\), any value equal to red is incompatible with \(A \neq B\), so remove red from \(D_B\).  
  New domain:
  \[
  D_B = \{green, blue\}.
  \]

- For \(C\), the same reasoning applies.  
  New domain:
  \[
  D_C = \{green, blue\}.
  \]

If some neighbor had domain \(\{red\}\) before the assignment, it would now become empty, and failure could be detected immediately.

### Misconception block

Forward checking does **not** fully reason through chains of implications. It only sees immediate consequences of the current assignment.

### Connection to later material

Forward checking is often combined with variable-ordering heuristics. It is fast enough to use at each search node and can dramatically reduce wasted branching.

### Retain / Do not confuse

Retain:
- Forward checking prunes neighboring future domains after an assignment.

Do not confuse:
- deleted values with assigned values,
- immediate pruning with full consistency enforcement.

## 7.2 Arc consistency

### Why this subsection exists

Forward checking may miss deeper incompatibilities. Arc consistency goes further by enforcing a local support condition across pairs of variables, whether or not one of them was just assigned.

### The object being introduced

For a binary constraint between \(X\) and \(Y\), a value \(a \in D_X\) is supported by \(Y\) if there exists some \(b \in D_Y\) such that the pair \((a,b)\) satisfies the constraint. Arc consistency removes values with no support.

### Formal definition

A binary CSP is **arc consistent** on arc \(X \to Y\) if for every value \(a \in D_X\), there exists some value \(b \in D_Y\) such that the pair \((a,b)\) satisfies the constraint between \(X\) and \(Y\).

A binary CSP is arc consistent if every directed arc is arc consistent.

### Interpretation

Arc consistency asks not whether a value is currently contradictory, but whether it still has at least one compatible partner in each neighboring variable. If a value has no possible partner, it is already dead and should be removed even if no explicit assignment has yet chosen it.

### Boundary conditions

Arc consistency is usually stated for binary CSPs. Higher-arity generalizations exist, but the details change. Also, arc consistency alone does not guarantee global solvability. It is a local condition.

### Fully worked example

This example is chosen because it shows how pruning can cascade.

Variables:
- \(X \in \{1,2,3\}\),
- \(Y \in \{2,3\}\).

Constraint:
\[
X < Y.
\]

Check each value of \(X\) for support in \(Y\).

- \(X=1\): supported, because \(1<2\) and \(1<3\).
- \(X=2\): supported, because \(2<3\).
- \(X=3\): unsupported, because there is no value in \(\{2,3\}\) such that \(3<Y\).

So remove 3 from \(D_X\), leaving:
\[
D_X = \{1,2\}.
\]

Now check the reverse arc \(Y \to X\).

- \(Y=2\): supported because \(1<2\).
- \(Y=3\): supported because \(1<3\) or \(2<3\).

So \(D_Y\) stays \(\{2,3\}\).

This small example shows the support logic directly: a value survives only if a compatible partner exists on the other end of the arc.

### Misconception block

**Arc consistency does not mean every surviving value participates in a full solution.**

It only means each value has local support on every relevant neighbor.

### Connection to later material

Maintaining arc consistency during search often catches dead ends much earlier than raw backtracking. It is one of the central “inference” ideas mentioned in the lecture.

### Retain / Do not confuse

Retain:
- Arc consistency is about support.
- Unsupported values are removed.
- It is stronger than forward checking but still local.

Do not confuse:
- local support with guaranteed global extendability.

## 7.3 Maintaining arc consistency during search

### Why this subsection exists

Arc consistency as a preprocessing step is useful, but assignments made during search can invalidate supports. So one often re-establishes arc consistency after every assignment.

### The object being introduced

**MAC** means maintaining arc consistency throughout backtracking search.

### Interpretation

Think of MAC as repeatedly re-solving the local compatibility picture every time a decision changes the state of the problem.

### Worked example

Suppose \(X,Y,Z\) each initially have domain \(\{1,2\}\), with constraints:
- \(X = Y\),
- \(Y = Z\),
- \(X \neq Z\).

Assign \(X=1\), so \(D_X = \{1\}\).

Maintaining arc consistency now propagates:

1. From \(X=Y\), the only supported value in \(D_Y\) is 1, so \(D_Y\) becomes \(\{1\}\).
2. From \(Y=Z\), the only supported value in \(D_Z\) is 1, so \(D_Z\) becomes \(\{1\}\).
3. From \(X \neq Z\), value 1 in \(D_Z\) is not supported against \(X=1\), so \(D_Z\) becomes empty.

An empty domain means the current assignment \(X=1\) cannot lead to any solution. Search can backtrack immediately.

### Final interpretation

Without propagation, this contradiction may have appeared only later. MAC compresses the discovery of failure.

### Retain / Do not confuse

Retain:
- MAC means re-enforcing arc consistency after each search decision.
- Empty domain means immediate failure of the current branch.

Do not confuse:
- aggressive pruning with risky guessing. Proper propagation is deductively sound.

---

# 8. Variable ordering and value ordering: choosing where to branch

This section exists because once search is combined with propagation, the next major source of performance difference is *where* and *how* the algorithm branches. The same CSP can be easy or difficult depending on which variable is chosen next and which values are tried first.

## The object being introduced

A **variable-ordering heuristic** chooses the next unassigned variable. A **value-ordering heuristic** chooses the order in which candidate values for that variable are tried.

These heuristics do not change correctness. They change the shape of the search tree.

## Interpretation

Search becomes easier when it discovers dead ends early and successful assignments early. Good variable ordering aims to make contradictions appear sooner. Good value ordering aims to try values that preserve future flexibility.

## 8.1 Minimum remaining values intuition

### Why this subsection exists

When some variable has very few legal values left, it is risky to postpone it. If it is going to fail, better to learn that now.

### The object being introduced

The familiar idea is often called **minimum remaining values (MRV)**: choose the unassigned variable with the smallest current domain.

### Interpretation

A small domain signals fragility. Such a variable is closer to contradiction than one with many options. Assigning it first tends to expose impossible branches earlier.

### Worked example

Suppose after propagation:
- \(D_A = \{2\}\),
- \(D_B = \{1,3,4,5\}\),
- \(D_C = \{2,3\}\),
- \(D_D = \{1,2,3,4,5,6\}\).

Choosing \(A\) next is usually sensible because there is only one possible value. Either it works and triggers further propagation, or it quickly exposes failure. Delaying it gains nothing.

### Misconception block

MRV is not “choose the variable with the smallest original domain.” It uses the **current** domain after all reductions so far.

### Connection to later material

MRV is especially powerful when combined with forward checking or MAC, because domain sizes are then informative.

### Retain / Do not confuse

Retain:
- choose fragile variables early.

Do not confuse:
- original domain size with current remaining options.

## 8.2 Least constraining value intuition

### Why this subsection exists

Once a variable is chosen, the order of values matters. Some values cut off many future possibilities; others leave the rest of the problem flexible.

### The object being introduced

The usual idea is **least constraining value**: try the value that rules out the fewest options for neighboring unassigned variables.

### Interpretation

If multiple values are locally legal, prefer the one that preserves future freedom. This does not guarantee success, but it often reduces backtracking.

### Worked example

Suppose \(A\) is connected to \(B\) and \(C\) by inequality constraints. Current domains:
- \(D_A = \{red, green\}\),
- \(D_B = \{red\}\),
- \(D_C = \{red, green, blue\}\).

If we try \(A=red\), then \(B\) loses its only value and the branch fails immediately.

If we try \(A=green\), then \(B\) keeps red, and \(C\) loses only green, leaving \(\{red,blue\}\).

So \(green\) is the better value to try first because it preserves more future support.

### Misconception block

Least constraining value is not about what seems “most popular” or “most common.” It is about how many future domain values remain legal after the choice.

### Retain / Do not confuse

Retain:
- values should be judged by how much future flexibility they preserve.

Do not confuse:
- local legality with future friendliness.

---

# 9. Search versus inference, and systematic versus local search

This section exists because the lecture explicitly distinguishes these ideas, and the distinction is foundational. Students often mix them together because both are used in the same solver. But they answer different questions.

## The object being introduced

There are two major conceptual axes:

1. **Search versus inference**
2. **Systematic search versus local search**

These are not cosmetic labels. They describe different state spaces and different kinds of reasoning.

## Formal distinction

- **Search** explores choices.
- **Inference** derives consequences of current information without branching.

Among search methods:
- **systematic search** usually works over partial consistent assignments,
- **local search** usually works over complete assignments that may violate constraints.

## Interpretation

Inference is deductive compression: it shrinks the problem without committing beyond logical consequence. Search handles the remaining uncertainty by branching.

Systematic search thinks globally about completing a partial solution. Local search starts from a full but possibly flawed candidate and makes small changes to improve it.

## Boundary conditions

The distinction is conceptual, not absolute. A practical solver can interleave search and inference at every node. Local search may also contain randomness or greediness rather than full systematic guarantees.

## Fully worked comparison

Consider a Sudoku-like CSP.

- Inference step: from row, column, and block restrictions, conclude that a certain cell cannot contain 1, 3, or 8. No branching happened. The solver merely derived consequences.
- Systematic search step: choose one cell and tentatively assign 5. This is a commitment among alternatives.
- Local search step: start from a full grid that may violate constraints and swap values or reassign one variable to reduce the number of conflicts.

The three actions are different even if they occur within one overall solving process.

## Misconception block

**Inference is not the same as search with very few branches.**  
Inference makes only logically forced reductions. Search chooses among alternatives not yet determined by logic.

## Connection to later material

Branch-and-bound is systematic search for optimization. WalkSAT is local search for satisfiability. Complexity theory will classify the underlying decision problems independently of whether we solve them by inference-heavy or search-heavy methods.

## Retain / Do not confuse

Retain:
- inference deduces,
- search branches,
- systematic search uses partial assignments,
- local search uses complete states and repairs them.

Do not confuse:
- domain reduction with value commitment,
- local search neighborhoods with search-tree branches.

---

# 10. From feasibility to optimization: soft constraints and objective functions

This section exists because many real problems are not just “find any satisfying assignment.” They ask for the best feasible assignment, or even the least-bad assignment when all preferences cannot be satisfied simultaneously. The lecture points out this transition explicitly. We now need to make it conceptually precise.

## The object being introduced

A **constraint optimization problem** extends a CSP by adding a numerical objective. Hard constraints define what is allowed. The objective measures how good a complete assignment is among the allowed ones, or sometimes how costly its violations are.

What is fixed:
- the variables, domains, and hard constraints,
- the objective function.

What varies:
- the complete assignment.

What conclusion it allows:
- which assignments are feasible,
- which feasible assignment is optimal.

## Formal definition

A **constraint optimization problem (COP)** consists of:
- a CSP \((X,D,C)\),
- an objective function
  \[
  f: \text{complete assignments} \to \mathbb{R},
  \]
  to be minimized or maximized.

If some constraints are **soft**, they may be converted into cost terms and absorbed into the objective.

## Interpretation

The key distinction is between:
- **hard constraints**, which may not be violated,
- **soft constraints or preferences**, which may be traded off according to cost.

In a pure CSP, all feasible solutions are equally acceptable. In a COP, feasibility is only the beginning.

## Boundary conditions and failure modes

Students often blur the boundary between hard and soft constraints. That is dangerous. If a rule is truly mandatory, it cannot simply be given a high but finite penalty unless one accepts the possibility of violating it. Modeling requires deciding which rules are inviolable and which are preferences.

Also, the path to the solution usually does not matter in CSP optimization. What matters is the complete assignment itself. This is unlike path-planning formulations where path cost accumulates along a trajectory.

## Fully worked example: exam scheduling with preferences

This example is chosen because it cleanly separates hard feasibility from soft quality.

Suppose we schedule two exams \(E_1\) and \(E_2\) into time slots \(\{morning, afternoon\}\).

Hard constraint:
- they cannot be in the same slot because many students take both.

Soft preference:
- \(E_1\) should preferably be in the morning, but afternoon is allowed at cost 1.

Variables:
- \(X_1\) for \(E_1\),
- \(X_2\) for \(E_2\).

Domains:
\[
D_1 = D_2 = \{morning, afternoon\}.
\]

Hard constraint:
\[
X_1 \neq X_2.
\]

Objective:
\[
f(X_1,X_2) =
\begin{cases}
0 & \text{if } X_1 = morning,\\
1 & \text{if } X_1 = afternoon.
\end{cases}
\]

### Check feasible assignments

The complete assignments are:
- \((morning, afternoon)\), feasible,
- \((afternoon, morning)\), feasible,
- \((morning, morning)\), infeasible,
- \((afternoon, afternoon)\), infeasible.

Now evaluate objective on feasible ones:
- \(f(morning, afternoon)=0\),
- \(f(afternoon, morning)=1\).

Therefore the optimal solution is \((morning, afternoon)\).

### Final interpretation

The example teaches the layered reasoning:
1. filter by hard constraints,
2. compare surviving complete assignments by objective.

## Misconception block

A soft constraint is not just “a normal constraint that matters less.” It is a preference represented numerically so that trade-offs can be made.

## Connection to later material

Traveling Salesman, weighted CSPs, and branch-and-bound all rely on this feasibility-versus-quality distinction. Complexity also changes: optimization problems are usually at least as hard as their feasibility counterparts.

## Retain / Do not confuse

Retain:
- hard constraints define admissibility,
- soft constraints contribute to the objective,
- optimization compares complete assignments, not partial ones directly.

Do not confuse:
- feasibility with optimality,
- penalties with hard impossibility.

---

# 11. Branch-and-bound: depth-first optimization with pruning

This section exists because once an objective enters the picture, ordinary backtracking is no longer enough. We need a way to explore candidate assignments while discarding branches that cannot possibly beat the best solution already found. Branch-and-bound is the standard idea.

## The object being introduced

**Branch-and-bound** is a systematic search method for optimization. It keeps:
- a current best complete solution, giving an **upper bound** for minimization,
- a lower bound on the best solution achievable below any partial assignment.

If the lower bound for a branch is already no better than the current best known solution, the branch can be pruned.

What is fixed:
- the optimization problem,
- the current incumbent best solution.

What varies:
- the partial assignment being explored,
- the bound computed for that partial assignment.

What conclusion it allows:
- whether exploring that branch can still improve the incumbent.

## Formal definition

For a minimization problem:
- let \(U\) be the cost of the best complete solution found so far,
- let \(L(n)\) be a lower bound on the cost of any complete solution extending search node \(n\).

If
\[
L(n) \ge U,
\]
then node \(n\) can be pruned, because no completion below it can improve the incumbent.

## Interpretation

The logic is extremely clean. The upper bound comes from reality: a genuine solution already found. The lower bound comes from optimism: the best this branch could possibly do, even under the most favorable completion. If even that optimistic estimate is not good enough, the branch is hopeless.

## Boundary conditions

Branch-and-bound depends on the lower bound being valid. For minimization, it must never overestimate the true best possible completion cost below the node. Otherwise one may prune away the real optimum.

Also, good performance depends heavily on finding a decent incumbent early and having informative bounds. With weak bounds, the method degenerates toward exhaustive search.

## Fully worked example: tiny route optimization

This example is chosen because the bound logic is easier to see in a small problem than in full TSP.

Suppose we must choose an order for visiting cities \(A,B,C\) starting at \(S\) and returning to \(S\). Imagine a partial route has already fixed \(S \to A\), with current accumulated cost
\[
g = 7.
\]

Suppose a lower-bound estimate for completing the rest of the tour from this partial route is
\[
h = 5.
\]

Then the branch lower bound is:
\[
L = g + h = 12.
\]

Assume we already found a complete tour of cost
\[
U = 11.
\]

Now compare:
\[
L = 12 \ge 11 = U.
\]

Since every completion of this partial route must cost at least 12, and we already have a solution of cost 11, this branch cannot improve the incumbent. It is safe to prune.

Now suppose instead another branch has
\[
g = 6,\qquad h = 3,
\]
so
\[
L = 9.
\]

Because \(9 < 11\), this branch might still lead to a better tour, so it must be explored.

### Final interpretation

Branch-and-bound is not guessing that a branch is bad. It is proving that even its best-case completion is not competitive.

## Misconception block

The lower bound is not a prediction of the final cost. It is a guaranteed floor. For pruning, validity matters more than tightness, though tightness helps efficiency.

## Connection to later material

This method links CSP search ideas to optimization and to heuristic search concepts like admissible estimates. It is especially relevant for TSP and weighted scheduling problems.

## Retain / Do not confuse

Retain:
- upper bound comes from best known complete solution,
- lower bound comes from optimistic estimate on a branch,
- prune when the branch cannot beat the incumbent.

Do not confuse:
- an estimate used for pruning with an arbitrary heuristic guess.

---

# 12. Local search for CSPs: complete states, conflicts, and repair

This section exists because systematic search is not always the practical winner, especially on large or weakly structured problems. The lecture explicitly introduces local search, and it is important to understand that it changes the state space completely.

## The object being introduced

In local search for CSPs, a state is usually a **complete assignment**, even if it violates constraints. The algorithm repeatedly changes one or a few variable values to improve an objective such as the number of violated constraints.

What is fixed:
- the complete set of variables and domains,
- a cost or conflict function.

What varies:
- the current complete assignment.

What conclusion it allows:
- whether nearby assignments improve quality,
- whether the search should move, restart, or randomize.

## Formal definition

A typical local-search formulation for a CSP uses:
- state space: all complete assignments,
- neighborhood: assignments differing from the current one in a small local way,
- objective:
  \[
  cost(s) = \text{number of violated constraints in state } s,
  \]
  or a weighted version.

A solution is any state with cost 0.

## Interpretation

This is a profound shift from backtracking. Systematic search insists on staying consistent so far. Local search is willing to live temporarily in inconsistent states if that makes it easier to navigate toward a better one.

## Boundary conditions and failure modes

Local search is usually incomplete unless enhanced by restart strategies or special structure. It can get trapped in local minima, plateaus, or cycles. Its strength is speed and scalability; its weakness is the lack of worst-case guarantees.

## Fully worked example: 3SAT as local search

This example is chosen because the lecture mentions 3SAT and WalkSAT, and SAT is the clearest place to see conflict-based local improvement.

Consider the Boolean formula:
\[
(\neg x_2 \vee \neg x_3 \vee x_4)
\wedge
(x_1 \vee x_4 \vee \neg x_7)
\wedge
(x_1 \vee \neg x_4 \vee x_6)
\wedge
(\neg x_1 \vee \neg x_3 \vee \neg x_5)
\wedge
(\neg x_4 \vee x_5 \vee \neg x_6).
\]

A complete state assigns each variable either true or false.

Suppose the current assignment is:
\[
x_1=0,\ x_2=1,\ x_3=1,\ x_4=1,\ x_5=0,\ x_6=0,\ x_7=0.
\]

Now evaluate each clause.

1. \((\neg x_2 \vee \neg x_3 \vee x_4)\)  
   Since \(x_2=1\), \(\neg x_2=0\). Since \(x_3=1\), \(\neg x_3=0\). Since \(x_4=1\), the third literal is 1. Clause satisfied.

2. \((x_1 \vee x_4 \vee \neg x_7)\)  
   \(x_1=0\), \(x_4=1\), so satisfied.

3. \((x_1 \vee \neg x_4 \vee x_6)\)  
   \(x_1=0\), \(\neg x_4=0\), \(x_6=0\). All three are false, so this clause is violated.

4. \((\neg x_1 \vee \neg x_3 \vee \neg x_5)\)  
   \(\neg x_1=1\), so satisfied.

5. \((\neg x_4 \vee x_5 \vee \neg x_6)\)  
   \(\neg x_4=0\), \(x_5=0\), \(\neg x_6=1\), so satisfied.

So exactly one clause is violated. The conflict cost is 1.

Now ask: which single-variable flip improves the situation? If we flip \(x_6\) from 0 to 1, clause 3 becomes satisfied because \(x_6\) becomes true. But check clause 5 after the flip:
\[
(\neg x_4 \vee x_5 \vee \neg x_6) = (0 \vee 0 \vee 0),
\]
so clause 5 becomes violated. The total number of violated clauses stays 1.

If instead we flip \(x_1\) from 0 to 1, clause 3 becomes satisfied because \(x_1\) becomes true, and clause 4 remains satisfied because although \(\neg x_1\) becomes false, \(\neg x_5\) remains true. Then all five clauses are satisfied, so the conflict cost drops to 0.

### Final interpretation

The example teaches the pattern of local search:
- define a complete-state cost,
- inspect neighboring states,
- choose a move that reduces cost if possible.

## Misconception block

Local search for CSPs does not search through partial assignments. It searches through complete assignments, including bad ones.

## Connection to later material

WalkSAT, stochastic local search, simulated annealing, and many heuristic optimization methods fit this pattern. For very large SAT instances, local search can be extremely effective in practice even though it lacks full worst-case guarantees.

## Retain / Do not confuse

Retain:
- local search uses complete assignments,
- objective often equals number of conflicts,
- moves are local repairs.

Do not confuse:
- local improvement with proof of optimality or completeness.

---

# 13. WalkSAT and the role of randomness

This section exists because greedy local improvement alone often gets stuck. The lecture mentions WalkSAT precisely because it illustrates a broader idea: randomness can be a feature, not a bug, when the search landscape contains traps.

## The object being introduced

**WalkSAT** is a local-search algorithm for SAT that repeatedly chooses a currently false clause and flips either:
- a variable that greedily improves satisfaction,
- or a randomly chosen variable from that clause.

The random step is what helps escape local traps.

## Interpretation

The algorithm alternates between exploitation and exploration. Pure greed exploits current information but may stall on plateaus or local minima. Random moves explore alternative regions of the state space.

## Boundary conditions

WalkSAT is not complete in the strict worst-case sense if run with a fixed flip limit and then allowed to fail. Its power is empirical speed on many large instances, not a guarantee of success on every input.

## Fully worked example

Take two false clauses under the current assignment. Suppose the algorithm selects one false clause:
\[
(a \vee b \vee \neg c).
\]
Because the clause is currently false, all three literals are false under the present assignment. That means:
- \(a = false\),
- \(b = false\),
- \(\neg c = false\), so \(c = true\).

To make the clause true, at least one of these underlying variable settings must be flipped:
- set \(a\) to true,
- or set \(b\) to true,
- or set \(c\) to false.

A greedy step examines which flip would maximize the number of satisfied clauses overall. A random step chooses one of those clause variables without that calculation.

The general lesson is that randomness is not replacing logic. It is compensating for the myopia of purely local objective improvement.

## Misconception block

Randomized search is not the same as uninformed search. The randomness in WalkSAT is targeted: it acts within a currently violated clause.

## Connection to later material

This idea generalizes far beyond SAT. Random restarts, noisy hill climbing, and annealing all use controlled randomness to escape local structure that would trap a purely deterministic method.

## Retain / Do not confuse

Retain:
- WalkSAT mixes greedy repair with random moves.

Do not confuse:
- strategic stochasticity with aimless guessing.

---

# 14. Decision, search, and optimization: three problem types that students often blur

This section exists because complexity theory becomes confusing immediately if one does not separate these three problem forms. The same real-world problem often has all three versions, and they do not ask exactly the same question.

## The object being introduced

For many combinatorial problems, there are at least three related formulations:

1. **Decision problem**: does there exist a solution with a stated property?
2. **Search problem**: find such a solution.
3. **Optimization problem**: find the best solution.

What is fixed:
- the problem instance.

What varies:
- the kind of answer requested.

What conclusion it allows:
- yes/no,
- a witness assignment,
- or an optimal witness.

## Formal distinctions

- Decision version of CSP:
  “Does there exist a complete assignment satisfying all constraints?”

- Search version of CSP:
  “Find a complete satisfying assignment.”

- Optimization version:
  “Find a satisfying assignment minimizing or maximizing a given objective,” or “find the minimum-conflict assignment.”

## Interpretation

Decision problems are central in complexity theory because they are easiest to classify formally. But search and optimization are often what users actually want. The important insight is that these forms are related but not identical.

## Fully worked example: Traveling Salesman

This example is chosen because TSP is the classical place where the distinction is unavoidable.

Suppose cities and distances are given.

- **Decision TSP**: Is there a tour visiting every city exactly once and returning to the start with total cost at most \(B\)?
- **Search TSP**: Produce a tour satisfying that bound, if one exists.
- **Optimization TSP**: Find the minimum-cost tour.

The optimization version is what people usually mean informally by “solve TSP.” But NP-completeness statements are typically made about the **decision** version.

### What remains fixed and what changes

The graph and edge weights stay fixed. Only the question changes. The decision version asks about existence under a threshold \(B\). The optimization version asks for the actual minimum.

## Misconception block

NP-complete is a label for decision problems. People casually say “TSP is NP-complete,” but the precise statement concerns an associated decision version. The optimization version is NP-hard.

## Connection to later material

This distinction is indispensable when we define P, NP, NP-hard, and NP-complete. It also clarifies why branch-and-bound solves optimization while SAT is usually posed as decision.

## Retain / Do not confuse

Retain:
- decision asks yes/no,
- search asks for a witness,
- optimization asks for the best witness.

Do not confuse:
- the informal problem name with the precise complexity-class statement.

---

# 15. Polynomial time, exponential time, and why worst-case complexity matters

This section exists because the requested material includes NP, NP-hard, and NP-complete, and those notions only make sense against the backdrop of tractability. We need to explain why polynomial time is the dividing line used in complexity theory, while also being honest about what it does and does not mean.

## The object being introduced

An algorithm’s **time complexity** measures how its running time grows with input size \(n\). Complexity theory classifies problems by whether they can be solved in time bounded by some polynomial in \(n\), such as \(n^2\), \(n^3\), or \(n^{10}\), versus exponential forms such as \(2^n\) or \(n!\).

## Interpretation

Polynomial time is treated as the formal notion of efficient or tractable computation because polynomial growth scales qualitatively better than exponential growth as input size increases. This is not because every polynomial is practically fast, nor because every exponential method is useless on small instances. It is a worst-case asymptotic distinction.

## Boundary conditions

Worst-case complexity is a guarantee, not an average. Some NP-hard problems are easy on many practical instances. Some polynomial-time algorithms are too slow or memory-heavy for real use. Complexity theory is about principled limits and classifications, not direct performance prediction on every instance.

## Fully worked growth comparison

This example is chosen because students often hear “exponential is bad” without feeling it.

Take input size \(n=20\):
- \(n^2 = 400\),
- \(n^3 = 8000\),
- \(2^n = 1,048,576\),
- \(n! \approx 2.43 \times 10^{18}\).

Now take \(n=50\):
- \(n^3 = 125,000\),
- \(2^{50} \approx 1.13 \times 10^{15}\).

The lesson is not just that exponential is bigger. It is that each extra unit of input size multiplies the work in a fundamentally more dangerous way.

## Misconception block

Polynomial time does not mean “fast in practice,” and exponential time does not mean “hopeless for every real instance.” These are complexity-theoretic categories, not performance guarantees for a specific machine and dataset.

## Connection to later material

P will collect decision problems solvable in polynomial time. NP will collect decision problems whose yes-instances can be verified in polynomial time given a certificate. NP-hard and NP-complete are then defined relative to polynomial-time reductions.

## Retain / Do not confuse

Retain:
- polynomial versus exponential is an asymptotic tractability distinction.

Do not confuse:
- theoretical tractability with immediate practical speed.

---

# 16. The class P

This section exists because P is the baseline against which NP and NP-completeness are defined. Without P, the rest of the hierarchy floats without anchor.

## The object being introduced

**P** is the class of decision problems solvable by a deterministic algorithm in polynomial time.

What is fixed:
- a decision problem.

What varies:
- the input instance.

What conclusion it allows:
- whether the problem can always be decided in polynomial time.

## Formal definition

A decision problem is in **P** if there exists a deterministic algorithm and a polynomial \(p(n)\) such that for every input of length \(n\), the algorithm correctly answers yes or no in at most \(p(n)\) time.

## Interpretation

P contains decision problems for which we know an algorithm whose worst-case running time grows at most polynomially with input size. It is the formal class of efficiently solvable decision problems under the standard model.

## Boundary conditions

P is defined for decision problems. Optimization problems are usually discussed via their decision versions or via function classes outside the scope of a first course.

Also, membership in P depends on the encoding of the input, though standard reasonable encodings usually preserve the broad classification.

## Fully worked example: graph reachability

This example is chosen because it is a clean decision problem.

Problem: given a directed graph \(G\) and vertices \(s\) and \(t\), is there a path from \(s\) to \(t\)?

A breadth-first search or depth-first search explores the graph from \(s\), marking visited vertices. Each edge and vertex is processed a bounded number of times. The running time is polynomial in the size of the graph representation. Therefore reachability is in P.

### What is being checked at each step

The search inspects outgoing edges from discovered vertices. When a new vertex is reached, it is marked. If \(t\) is reached, answer yes. If exploration ends without reaching \(t\), answer no.

### Final interpretation

The importance of this example is not just that it is easy. It shows what a P result looks like: a clear, general algorithm with polynomial worst-case guarantee.

## Misconception block

P is not “problems that seem easy.” It is a formal class based on polynomial-time algorithms we actually know.

## Connection to later material

Once P is clear, NP can be understood as a broader class defined by efficient verification. The biggest open question in classical complexity is whether \(P = NP\).

## Retain / Do not confuse

Retain:
- P consists of decision problems solvable in polynomial time.

Do not confuse:
- “I can solve small instances quickly” with “the problem is in P.”

---

# 17. The class NP

This section exists because students often hear “NP means not polynomial,” which is false. The class NP is about verifiability of yes-instances, not about being hard.

## The object being introduced

**NP** is the class of decision problems for which a yes-answer has a certificate that can be verified in polynomial time by a deterministic algorithm.

What is fixed:
- a decision problem,
- a proposed certificate or witness.

What varies:
- the input instance,
- whether the certificate indeed proves a yes-answer.

What conclusion it allows:
- whether yes-instances admit efficiently checkable witnesses.

## Formal definition

A decision problem \(L\) is in **NP** if there exists a polynomial-time deterministic verification algorithm \(V\) and a polynomial \(q(n)\) such that:
- for every input \(x\),
- \(x \in L\) if and only if there exists a certificate \(y\) with \(|y| \le q(|x|)\) and
  \[
  V(x,y) = yes.
  \]

## Interpretation

NP is the class of problems for which a claimed yes-solution can be checked efficiently. It does **not** say we know how to find that witness efficiently. Verification may be easy even when discovery is hard.

## Boundary conditions and common confusions

Two clarifications matter.

First, NP stands for nondeterministic polynomial time historically, but for learning purposes the certificate-verification view is usually clearer.

Second, NP contains P, because if you can solve a problem efficiently, then you can certainly verify a yes-instance efficiently: simply solve it and compare.

## Fully worked example: SAT in NP

This example is chosen because SAT is the canonical NP problem.

Problem: given a Boolean formula in conjunctive normal form, is there an assignment of truth values that makes it true?

### Certificate

A certificate is simply a truth assignment to the variables.

### Verification

Given the formula and the assignment, verify by evaluating each clause in turn.

For each clause:
1. inspect its literals,
2. determine whether at least one literal is true under the certificate,
3. if any clause is false, reject the certificate,
4. if all clauses are true, accept.

If the formula has \(m\) clauses and total representation size \(N\), this check is polynomial in \(N\).

### Final interpretation

The important lesson is that SAT belongs to NP not because it is known to be easy, but because once someone hands you an assignment, checking it is efficient.

## Misconception block

**NP does not mean “not polynomial.”**  
It also does not mean “hard.” Some NP problems are in P.

## Connection to later material

NP is the universe within which NP-complete problems live. To show a problem is NP-complete, one must usually show both:
- the problem is in NP,
- the problem is at least as hard as every problem in NP via reductions.

## Retain / Do not confuse

Retain:
- NP is about polynomial-time verification of yes-certificates.
- \(P \subseteq NP\).

Do not confuse:
- easy to verify with easy to solve,
- NP with “probably intractable” as a definition.

---

# 18. NP-hard and NP-complete

This section exists because these are the labels the user explicitly requested, and they are central to the theory of CSPs, SAT, Sudoku, graph coloring, and TSP. The definitions must be stated carefully because small imprecision creates major confusion.

## The object being introduced

Two notions are being introduced:

1. **NP-hard**: at least as hard as every problem in NP, under polynomial-time reduction.
2. **NP-complete**: both NP-hard and itself in NP.

These classify decision problems relative to the hardest problems in NP.

## Formal definitions

A decision problem \(H\) is **NP-hard** if for every problem \(L \in NP\), there exists a polynomial-time reduction from \(L\) to \(H\).

A decision problem \(C\) is **NP-complete** if:
1. \(C \in NP\),
2. \(C\) is NP-hard.

## Interpretation

NP-hard means: if you could solve \(H\) efficiently, then you could solve every problem in NP efficiently by first reducing it to \(H\). So \(H\) is at least as hard as the entire class NP.

NP-complete means: this problem sits inside NP and is among the hardest problems there.

## Boundary conditions

Several precision points matter.

First, NP-hardness is defined using reductions from **every** NP problem, not just from some famous hard-looking example.

Second, NP-hard problems need not be in NP. They may be optimization problems or even undecidable problems in more advanced settings. NP-complete problems must be decision problems in NP.

Third, the reduction must be polynomial-time. Hardness statements depend on this efficiency requirement.

## Fully worked conceptual example: why optimization TSP is NP-hard, not NP-complete

Take the optimization Traveling Salesman Problem: find the minimum-cost tour.

This is not a decision problem because its output is a tour and its minimum cost, not a yes/no answer. Therefore the phrase “NP-complete” does not apply directly to it. The correct statement is that the optimization problem is NP-hard.

Now form the decision version:

> Given a weighted graph and bound \(B\), is there a tour with total cost at most \(B\)?

If this decision version is in NP and NP-hard, then it is NP-complete.

Why is it in NP? Because a certificate is a proposed tour. We can verify in polynomial time that:
1. each city appears exactly once,
2. the tour returns to the start,
3. the total cost is at most \(B\).

That check is polynomial in the input size.

### Final interpretation

This example teaches the importance of problem form. Informally saying “TSP is NP-complete” skips a crucial distinction.

## Misconception block

**NP-hard does not mean “hard in practice,” and NP-complete does not mean “harder than NP-hard.”**

NP-complete is a subset of NP-hard. Every NP-complete problem is NP-hard, but not every NP-hard problem is NP-complete.

## Connection to later material

Once reductions are understood, one can show that many natural CSP variants are NP-complete. This explains why general-purpose exact algorithms often rely on pruning, heuristics, or local search rather than expecting polynomial-time success in all cases.

## Retain / Do not confuse

Retain:
- NP-hard = every NP problem reduces to it.
- NP-complete = in NP and NP-hard.
- Optimization problems are typically NP-hard rather than NP-complete.

Do not confuse:
- hardness class labels with empirical runtime on one instance.

---

# 19. Polynomial-time reductions: the language of hardness

This section exists because NP-hardness and NP-completeness are meaningless without reductions. A reduction is the bridge that transfers hardness from one problem to another.

## The object being introduced

A **polynomial-time reduction** transforms instances of one decision problem into instances of another so that yes-answers are preserved exactly.

What is fixed:
- source problem \(A\),
- target problem \(B\).

What varies:
- the specific instance \(x\) of \(A\),
- the transformed instance \(f(x)\) of \(B\).

What conclusion it allows:
- solving \(B\) efficiently would also solve \(A\) efficiently.

## Formal definition

A problem \(A\) polynomial-time reduces to problem \(B\), written
\[
A \le_p B,
\]
if there exists a polynomial-time computable function \(f\) such that for every instance \(x\),
\[
x \in A \iff f(x) \in B.
\]

## Interpretation

A reduction is not just a similarity or analogy. It is a precise translation. It says that the computational content of problem \(A\) can be encoded inside problem \(B\) with only polynomial overhead.

## Boundary conditions and failure modes

The direction matters enormously.

If
\[
A \le_p B,
\]
then \(B\) is at least as hard as \(A\). Students often reverse this mentally. The reduction goes from the known hard problem to the candidate target problem.

Also, the equivalence must preserve yes/no answers. A sloppy transformation that only “sort of resembles” the original problem proves nothing.

## Fully worked conceptual example: SAT to 3SAT

This example is chosen because 3SAT is a central NP-complete problem and the reduction pattern is widely reused.

Suppose SAT allows clauses of arbitrary length, while 3SAT requires exactly 3 literals per clause. The reduction transforms each long clause into a conjunction of 3-literal clauses using fresh auxiliary variables. The transformation is designed so that the original formula is satisfiable if and only if the new 3CNF formula is satisfiable.

The details of the clause gadgets can be technical, but the conceptual structure is what matters:
1. start from a known NP-complete problem,
2. rewrite each local structure using a bounded-size gadget,
3. ensure satisfiability is preserved in both directions,
4. keep the transformation polynomial in input size.

### Final interpretation

This is the standard strategy for proving a new problem NP-hard: encode a known hard problem into it without changing the existence of solutions.

## Misconception block

A reduction is not a solver. It is a translator. Its point is to transfer hardness or membership, not to solve the source problem directly.

## Connection to later material

CSP hardness results usually come from reductions out of SAT or 3SAT. Once you understand reductions, the classification of graph coloring, Hamiltonian cycle, and many CSP variants becomes conceptually unified.

## Retain / Do not confuse

Retain:
- reduce from a known hard problem to the target problem.
- the direction \(A \le_p B\) means \(B\) is at least as hard as \(A\).

Do not confuse:
- source and target direction in a hardness proof.

---

# 20. SAT, 3SAT, and CSP: one family seen from different angles

This section exists because SAT is the canonical NP-complete problem, 3SAT appears explicitly in the lecture, and CSPs are deeply related to it. A serious student should see them as members of one conceptual family rather than disconnected topics.

## The object being introduced

**SAT** asks whether a Boolean formula has a satisfying truth assignment. **3SAT** is the restricted version where every clause has exactly three literals. Both can be viewed as CSPs:
- variables are Boolean,
- domains are \(\{0,1\}\),
- clauses are constraints.

## Formal model

For SAT:
- variables \(x_1,\dots,x_n\),
- domains \(\{false,true\}\),
- one constraint per clause, satisfied when at least one literal in the clause is true.

For 3SAT, every clause constraint has scope size 3.

## Interpretation

SAT is a CSP where each constraint is a logical clause. CSP is the more general language. SAT is one especially important special case because of its central role in complexity theory and practical solving.

## Fully worked example

Take the 3SAT formula:
\[
(\neg x_2 \vee \neg x_3 \vee x_4)
\wedge
(x_1 \vee x_4 \vee \neg x_7).
\]

Treat each clause as a 3-ary constraint.

For the first clause, the only forbidden local assignments are those making all three literals false. That means:
- \(x_2 = true\),
- \(x_3 = true\),
- \(x_4 = false\).

So this clause constraint allows all \(2^3 = 8\) local assignments except that one forbidden tuple.

The second clause similarly forbids:
- \(x_1 = false\),
- \(x_4 = false\),
- \(x_7 = true\).

This perspective reveals a useful pattern: a clause is a very compact way to describe a local constraint relation over Boolean variables.

## Misconception block

SAT is not “something different from CSP.” It is a structured Boolean CSP. The difference is mostly one of language, special-purpose theory, and solver technology.

## Connection to later material

The NP-completeness of 3SAT provides a common starting point for reductions to many other combinatorial problems, including general CSP variants, graph problems, and planning problems.

## Retain / Do not confuse

Retain:
- SAT is Boolean constraint satisfaction.
- 3SAT restricts clause size to 3.
- Clause constraints forbid exactly those local assignments making all literals false.

Do not confuse:
- the syntax of a formula with the underlying constraint relation.

---

# 21. Why general CSP is computationally hard

This section exists because after learning all the modeling and algorithmic machinery, one might ask: why not hope for a universally efficient exact algorithm? Complexity theory answers that question.

## The object being introduced

The general finite-domain CSP decision problem asks:

> Given variables, finite domains, and constraints, does a satisfying assignment exist?

In broad unrestricted form, this problem is NP-complete.

## Interpretation

This means two things together:
1. if someone hands you a complete assignment, checking it is polynomial-time;
2. the problem is at least as hard as every problem in NP.

So in the general case, we do not expect a polynomial-time exact algorithm unless \(P=NP\).

## Why it is in NP

A certificate is a complete assignment. Verification checks, for each variable, that the chosen value lies in its domain, and for each constraint, that the projected tuple lies in the allowed relation. Provided the representation of constraints supports polynomial-time checking, verification is polynomial.

## Why it is NP-hard

At a high level, SAT reduces naturally to CSP:
- each Boolean variable becomes a CSP variable with domain \(\{0,1\}\),
- each clause becomes a local constraint forbidding exactly one local tuple.

Thus a SAT instance is already a special case of CSP. Since SAT is NP-hard, general CSP is NP-hard.

## Fully worked reduction sketch from 3SAT to CSP

This example is chosen because it shows the reduction almost transparently.

Take any 3SAT instance with variables \(x_1,\dots,x_n\) and clauses \(C_1,\dots,C_m\).

Construct a CSP:
- for each Boolean variable \(x_i\), create CSP variable \(X_i\) with domain \(\{0,1\}\),
- for each clause such as \((x_1 \vee \neg x_4 \vee x_6)\), create a constraint on \((X_1,X_4,X_6)\) that allows exactly the tuples making at least one of the literals true.

Now compare answers:
- if the formula is satisfiable, the satisfying truth assignment is a satisfying CSP assignment;
- if the CSP has a satisfying assignment, interpret 1 as true and 0 as false to obtain a satisfying truth assignment for the formula.

The translation is polynomial in size and preserves yes/no answers. Therefore general CSP is NP-hard.

## Misconception block

NP-completeness of general CSP does not mean every structured CSP instance is hard. Many restricted CSP families are polynomial-time solvable.

## Connection to later material

This explains why tractable subclasses and structural restrictions matter so much. It also explains why heuristics, propagation, and local search are central in practice.

## Retain / Do not confuse

Retain:
- unrestricted finite-domain CSP is NP-complete.
- hardness comes from the ability to encode SAT.

Do not confuse:
- worst-case hardness with every instance being difficult.

---

# 22. Tractable islands: when CSP becomes easier

This section exists because complexity theory should not leave the impression that CSPs are hopeless. The right lesson is subtler: unrestricted general CSP is hard, but special structure can make it tractable.

## The object being introduced

A **tractable subclass** is a restricted family of CSPs for which polynomial-time solving is possible.

Common sources of tractability include:
- very small or restricted constraint languages,
- special graph structure,
- tree-like dependency patterns,
- strongly exploitable global constraints.

## Interpretation

The purpose of modeling is not merely to state the problem. It is often to expose structure that algorithms can exploit. Hardness results tell us not to expect miracles in full generality. Structural results tell us where miracles are actually possible.

## Worked example: tree-structured binary CSP intuition

Suppose a binary CSP has a constraint graph that forms a tree rather than containing cycles. Then information can often be propagated inward and assignments chosen in a way that avoids exponential blowup.

Why is the tree shape helpful? Because cycles create mutual dependencies that can keep constraints hidden until later. Trees allow information to flow without circular reinforcement.

A full dynamic-programming treatment would go beyond this chapter’s scope, but the main lesson is essential: graph structure matters.

## Misconception block

NP-complete does not mean “nothing useful can be done.” It means there is unlikely to be one polynomial-time algorithm handling all instances of the unrestricted problem.

## Connection to later material

This viewpoint connects CSP to graphical models, treewidth, decompositions, and advanced exact inference methods.

## Retain / Do not confuse

Retain:
- hardness is a statement about the general case.
- restricted structure can restore tractability.

Do not confuse:
- “general CSP is hard” with “all CSPs are equally hard.”

---

# 23. Classical problems and their complexity labels

This section exists because students often remember names like SAT, 3SAT, Sudoku, graph coloring, Hamiltonian cycle, and TSP, but forget which version belongs to which complexity label.

## The object being introduced

We now assemble a conceptual map rather than a new definition.

## Interpretation

The point is not rote memorization. The point is to understand *why* each label applies.

## Common examples

### SAT
- Decision problem.
- In NP because assignments verify quickly.
- NP-complete.

### 3SAT
- Decision problem.
- In NP because assignments verify quickly.
- NP-complete.
- Especially important as a source problem for reductions.

### Graph coloring
- Decision version: can this graph be colored with at most \(k\) colors?
- In NP because a coloring is easy to verify.
- NP-complete for appropriate formulations.

### Sudoku
- Generalized decision versions are NP-complete.
- Verification of a filled grid is polynomial.
- Hardness comes from the ability to encode general constraint structure.

### TSP
- Decision version with budget \(B\): NP-complete.
- Optimization version: NP-hard.

### General CSP
- Decision version: NP-complete, under standard finite explicit representations.

## Misconception block

Do not memorize labels without problem form. Always ask:
1. Is this a decision problem?
2. Is a certificate polynomially checkable?
3. What known hard problem reduces to it?

## Connection to later material

This disciplined habit prevents the most common complexity mistakes in algorithms, AI, optimization, and theory courses.

## Retain / Do not confuse

Retain:
- always pair a complexity label with the precise problem statement.

Do not confuse:
- an informal problem name with its exact classified version.

---

# 24. How CSP algorithms and complexity theory fit together

This section exists because students sometimes treat algorithms and complexity as separate subjects. They are not. Complexity explains why the algorithmic toolbox for CSPs looks the way it does.

## The object being introduced

We now connect:
- modeling,
- propagation,
- systematic search,
- local search,
- optimization,
- hardness theory.

## Interpretation

General CSP is NP-complete, so one should not expect a universal polynomial-time exact solver. That is why:
- propagation is used to shrink the practical search space,
- heuristics are used to make the search tree favorable,
- branch-and-bound is used for optimization pruning,
- local search is used when exact guarantees are too costly,
- special structure is exploited whenever possible.

Complexity theory is not merely a negative statement. It explains why these methods are rational and necessary.

## Worked synthesis example: Sudoku solver design

Suppose you are building a Sudoku solver.

1. Model each cell as a variable and row/column/block conditions as all-different constraints.
2. Use propagation first to shrink domains from clue information.
3. If unsolved, choose a variable with minimum remaining values.
4. Try values in an order that preserves future flexibility.
5. After each assignment, propagate again.
6. If one wanted only a fast approximate or entertainment-oriented solver for huge generalized variants, one might consider local search instead.

Each design choice now has a theoretical explanation:
- propagation combats delayed failure,
- variable ordering reduces branching,
- local search trades guarantees for scalability,
- worst-case hardness explains why such sophistication is needed at all.

## Misconception block

Complexity theory does not replace algorithms. It tells you what kind of algorithms to hope for, and what compromises to expect.

## Connection to later material

This integration carries directly into probabilistic graphical models, integer programming, SAT solving, planning, scheduling, and machine learning with combinatorial subproblems.

## Retain / Do not confuse

Retain:
- theory explains the need for the algorithmic toolkit.
- algorithms exploit structure despite worst-case hardness.

Do not confuse:
- a hardness theorem with an instruction to give up on solving real instances.

---

# 25. Common misconceptions collected in one place

This section exists because many errors in this area are conceptual rather than algebraic. Seeing them together helps stabilize the big picture.

## Misconception 1: NP means not polynomial

False. NP means yes-instances have polynomially verifiable certificates.

## Misconception 2: NP-complete means impossible to solve

False. It means no polynomial-time algorithm is known for all instances, and one is unlikely unless \(P=NP\). Small or structured instances may still be easy.

## Misconception 3: Backtracking is just brute force

Incomplete truth. It is exponential in the worst case, but it prunes partial assignments and can be dramatically better than enumerating all full assignments.

## Misconception 4: Arc consistency solves the problem

False. Arc consistency is local. A CSP can be arc consistent and still unsatisfiable.

## Misconception 5: Local search and backtracking explore the same state space

False. Backtracking explores partial assignments. Local search explores complete assignments, often inconsistent ones.

## Misconception 6: A soft constraint is just a weaker hard constraint

False. A soft constraint contributes to preference or cost. A hard constraint defines feasibility.

## Misconception 7: TSP is NP-complete

Imprecise. The decision version is NP-complete. The optimization version is NP-hard.

## Misconception 8: SAT is different in kind from CSP

False. SAT is a special Boolean CSP with clause constraints.

---

# 26. What to look for when solving new problems

This section exists because mastery means transfer. The reader should not leave with only a list of named examples. They should know what pattern to recognize in new problems.

## The object being introduced

A **problem-analysis checklist** for recognizing and solving CSP-like problems.

## Interpretation

When facing a new combinatorial problem, ask the following in order.

### 1. What are the variables?

Identify the unknown quantities. These should be the objects whose values define a candidate solution.

### 2. What are their domains?

State clearly what values are legal before interactions are considered.

### 3. What are the hard constraints?

Write the exact relations that determine admissibility. Ask which variables each one touches.

### 4. Are there soft constraints or preferences?

If yes, separate them from hard constraints and define an objective.

### 5. What structure do the constraints have?

Are they binary, counting, all-different, clause-like, tree-shaped, sparse, dense?

### 6. Which solving approach fits best?

- strong propagation + backtracking for exact finite CSP,
- branch-and-bound for optimization,
- local search for large approximate or satisfiability-style settings,
- structural methods if the graph is tree-like.

### 7. Which complexity form matters?

Ask whether the target task is decision, search, or optimization. This determines which complexity labels are appropriate.

## Worked transfer example: seating arrangement

Suppose guests must be seated at tables:
- enemies cannot share a table,
- close collaborators should preferably sit together,
- tables have capacity limits.

Now the pattern should be recognizable:
- variables: each guest’s table assignment,
- domains: available tables,
- hard constraints: enemy separation, capacity,
- soft constraints: collaborator preference,
- objective: maximize preferred pairings or minimize penalties.

The same conceptual toolkit transfers immediately.

## Retain / Do not confuse

Retain:
- good modeling begins with variables, domains, constraints, and structure.

Do not confuse:
- the surface story of a problem with its underlying assignment structure.

---

# 27. Final synthesis

Constraint satisfaction is one of the cleanest general languages for discrete reasoning. It begins from a simple question: assign values to variables so that all rules are obeyed. But from that simple question grows an entire conceptual ecosystem.

The model itself gives the core objects: variables, domains, constraints, assignments, and solutions. Examples like map coloring, Sudoku, Minesweeper, Wordle, and SAT reveal that these objects are not tied to one application area. They are a common grammar for puzzles, logic, scheduling, routing, and combinatorial design.

Systematic search then enters because full solutions are rarely visible immediately. Partial assignments become the state space. Backtracking is the baseline mechanism: commit, check, and undo when necessary. Yet delayed failure makes naïve backtracking inefficient, so inference becomes essential. Forward checking and arc consistency are attempts to make the future speak sooner. Variable and value ordering shape the search tree further by deciding where branching pressure is greatest and which choices preserve flexibility.

When feasibility is not enough, optimization extends the model. Hard constraints define admissibility, soft constraints define preference, and branch-and-bound uses bounds to prune branches that cannot improve on the best known solution. Local search offers a different philosophy altogether: begin with a complete candidate, even an inconsistent one, and repair it through local moves. SAT and WalkSAT show how powerful that strategy can be when exact systematic search is too expensive.

Complexity theory explains why all of this machinery is needed. General CSP, SAT, and many related decision problems are NP-complete. Their yes-instances are easy to verify, yet no polynomial-time algorithm is known for solving them in full generality. Optimization versions such as TSP are NP-hard. These labels do not mean that real instances cannot be solved. They mean that one should not expect one universal efficient exact method for every unrestricted case. That is why structure, reductions, propagation, heuristics, and approximation matter so much.

The deepest lesson is this: the field is unified. Modeling, algorithms, and complexity are not separate topics. They are three views of the same reality.

- Modeling tells you what the problem is.
- Algorithms tell you how to exploit the structure you exposed.
- Complexity tells you what level of difficulty is unavoidable in general.

A student who understands that triangle is no longer just memorizing CSP vocabulary. They are learning how to think about discrete reasoning problems in a way that transfers across AI, algorithms, optimization, logic, and beyond.

---

# 28. High-value takeaways for long-term retention

## Retain

- A CSP is a finite set of variables, domains, and constraints.
- A solution is a complete assignment satisfying every hard constraint.
- Partial assignments can be locally consistent without being extendable.
- Backtracking explores partial assignments; local search explores complete assignments.
- Forward checking prunes immediate future values; arc consistency removes unsupported values.
- Hard constraints define feasibility; soft constraints define preference or cost.
- Branch-and-bound prunes optimization branches using lower and upper bounds.
- SAT is a Boolean CSP; 3SAT is a restricted NP-complete version.
- P means polynomial-time solvable decision problems.
- NP means yes-certificates are polynomial-time verifiable.
- NP-hard means at least as hard as every NP problem.
- NP-complete means both in NP and NP-hard.
- Decision, search, and optimization versions of a problem must be distinguished precisely.

## Do not confuse

- domain restrictions with relational constraints,
- local consistency with guaranteed solvability,
- inference with branching,
- backtracking with local search,
- feasibility with optimality,
- NP with “not polynomial,”
- NP-complete with “impossible,”
- optimization TSP with decision TSP,
- a reduction with a solver,
- worst-case hardness with typical practical behavior.

---
