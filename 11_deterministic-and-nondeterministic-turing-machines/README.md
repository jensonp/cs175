# Deterministic and Nondeterministic Turing Machines

## Chapter orientation

This chapter introduces two central models of computation: the **deterministic Turing machine** and the **nondeterministic Turing machine**. These models are not introduced because real computers literally look like them. They are introduced because they isolate the essential structure of computation in a form precise enough to reason about what can be computed, what can be decided, and how much time or space computation requires.

A Turing machine is a mathematical object designed to answer a foundational question:

> What does it mean, in the most general formal sense, for a problem to be solvable by mechanical computation?

The deterministic model captures ordinary step-by-step computation: at every moment, the machine has exactly one next move determined by its current situation. The nondeterministic model generalizes this by allowing several possible next moves from the same situation. This does not mean the machine guesses magically in any physical sense. It means the computation is represented as a branching tree of possible histories, and the machine accepts if at least one branch reaches acceptance.

The distinction between deterministic and nondeterministic machines becomes especially important later in complexity theory. Deterministic machines define classes such as **P**. Nondeterministic machines define classes such as **NP**. The Cook-Levin theorem, for example, depends on understanding nondeterministic computation as a finite accepting computation history that can be encoded and checked locally.

This chapter is written to build the concepts from first principles. It explains not only the definitions, but why each part of the definition is needed, what each object means, what assumptions are hidden in the notation, and what misconceptions should be avoided.

---

# 1. Why Turing Machines Are Introduced

## 1.1 The problem Turing machines solve

Before defining a Turing machine, it is worth asking why we need such a model at all. Informally, we already understand computation: a computer receives input, follows instructions, uses memory, and eventually may produce an answer. But informal understanding is not enough for proving theorems about computation. If we want to prove that a problem is solvable, unsolvable, efficiently solvable, or unlikely to be efficiently solvable, we need a formal model.

The model must be strong enough to represent ordinary algorithms, but simple enough that proofs about it are possible. This is the balance Turing machines achieve. They are deliberately minimal: one tape, one head, finitely many internal states, and a transition rule. Yet this minimal structure is powerful enough to simulate any standard algorithmic process.

The reason this section exists is that later definitions will look artificial unless we understand the purpose of the model. A Turing machine is not a programming language. It is a proof object. Its simplicity gives us a common mathematical language for talking about algorithms.

## 1.2 The object being introduced

A **Turing machine** is an abstract computing device. It has:

- a finite control, represented by states;
- an infinite tape, used as memory;
- a tape head, which reads and writes one cell at a time;
- a transition rule, which says how the machine moves from one moment to the next;
- designated halting states, usually accepting and rejecting states.

The fixed parts of the machine are its states, alphabets, transition rule, start state, accept state, and reject state. The varying part is the computation itself: the tape contents, the head position, and the current state change over time.

The machine answers questions about strings. Usually the input is a finite string over some alphabet, and the machine either accepts, rejects, or runs forever. By looking at which strings are accepted, we associate the machine with a language.

## 1.3 Formal definition of the common Turing machine framework

A standard single-tape Turing machine is built from the following components:

$$
M = (Q, \Sigma, \Gamma, \delta, q_0, q_{\mathrm{accept}}, q_{\mathrm{reject}})
$$

where:

- $Q$ is a finite set of states.
- $\Sigma$ is the input alphabet, not containing the blank symbol.
- $\Gamma$ is the tape alphabet, where $\Sigma \subseteq \Gamma$ and the blank symbol $\sqcup$ belongs to $\Gamma$.
- $\delta$ is the transition function or transition relation, depending on whether the machine is deterministic or nondeterministic.
- $q_0 \in Q$ is the start state.
- $q_{\mathrm{accept}} \in Q$ is the accepting halt state.
- $q_{\mathrm{reject}} \in Q$ is the rejecting halt state.
- $q_{\mathrm{accept}} \neq q_{\mathrm{reject}}$.

The exact form of $\delta$ is the main difference between deterministic and nondeterministic Turing machines. For deterministic machines, $\delta$ gives at most one next move. For nondeterministic machines, $\delta$ gives a set of possible next moves.

## 1.4 Interpretation

The tuple notation is compact, but every component has a job. The set $Q$ represents the machine's finite internal memory. The input alphabet $\Sigma$ tells us what symbols may appear in the original input. The tape alphabet $\Gamma$ is usually larger, because during computation the machine may need extra markers that were not in the original input. The blank symbol $\sqcup$ fills all tape cells that have not been written.

The start state $q_0$ determines where the computation begins. The accept and reject states determine two kinds of halting outcomes. The transition rule determines how the machine behaves during nonhalting computation.

The most important conceptual distinction is this:

> The input alphabet describes what the machine is allowed to receive. The tape alphabet describes what the machine is allowed to use while working.

This distinction matters because many algorithms need temporary markings. For example, a machine checking whether a string has the same number of $a$'s and $b$'s may mark symbols it has already matched. Those marks belong to the tape alphabet, not necessarily to the input alphabet.

## 1.5 Boundary conditions and assumptions

Several assumptions are usually made unless stated otherwise.

First, the tape is infinite in at least one direction, and often in both directions depending on the convention. This difference usually does not change what can be computed. A one-way infinite tape can simulate a two-way infinite tape with encoding tricks, and a two-way infinite tape can obviously simulate a one-way tape.

Second, the input is finite. Even though the tape is infinite, the machine begins with only finitely many nonblank input symbols. The rest of the tape is blank.

Third, the machine has only finitely many states and finitely many tape symbols. This is crucial. If a machine were allowed infinitely many states or infinitely many built-in symbols, it could hide unbounded information in its definition, which would destroy the model's purpose.

Fourth, each step is local. The machine reads only the symbol under its head, writes only to that cell, changes state, and moves the head one cell left or right, or possibly stays still if that convention is allowed.

Fifth, halting is not guaranteed unless the machine is specifically a decider. A Turing machine may run forever on some inputs.

## 1.6 Worked example: why a tape alphabet must be larger than an input alphabet

This example is chosen because it exposes a common hidden assumption. Beginners often think that if the input alphabet is $\{0,1\}$, then the tape may only contain $0$'s and $1$'s forever. That is not correct. The tape alphabet may include extra working symbols.

Suppose we want a machine to check whether an input over $\{0,1\}$ contains at least one $1$. The input alphabet is:

$$
\Sigma = \{0,1\}
$$

This says that legal input strings are built only from $0$'s and $1$'s. But during the computation, the machine might want to mark visited cells. It could use a special symbol $X$ to replace each scanned $0$, so it remembers that the cell has already been inspected. Then the tape alphabet might be:

$$
\Gamma = \{0,1,X,\sqcup\}
$$

The symbol $X$ is not part of the input language. It is a working mark. The machine is not accepting strings containing $X$ as original input; it is using $X$ internally.

The setup checks the role of each alphabet:

- $\Sigma$ controls the input format.
- $\Gamma$ controls the symbols available during computation.
- $\sqcup$ fills unused tape cells.
- $X$ is a temporary marker introduced by the machine's own operation.

The conclusion is that the input alphabet and tape alphabet answer different questions. The input alphabet asks, "What can the external input look like?" The tape alphabet asks, "What symbols may appear on the machine's work tape during computation?"

## 1.7 Misconception block: a Turing machine is not a real hardware design

A Turing machine is not meant to be an efficient physical computer. Its tape is idealized. Its head movement is primitive. Its instruction format is intentionally simple. The purpose is not engineering realism; the purpose is mathematical clarity.

The important claim is not that computers are built like Turing machines. The important claim is that Turing machines capture the same notion of algorithmic computability as ordinary programming languages, provided we ignore practical limitations such as finite memory and hardware speed.

## 1.8 Connection to later material

The Turing machine framework becomes the foundation for three major lines of theory.

First, it supports **decidability theory**, where we ask which languages can be decided at all.

Second, it supports **recognizability theory**, where we distinguish accepting positive instances from always halting on every input.

Third, it supports **complexity theory**, where we ask how many steps or tape cells are needed as a function of input length.

The deterministic and nondeterministic variants use the same basic architecture, but they define different ways of organizing possible computation paths. That difference is the main subject of the rest of this chapter.

## 1.9 Retain / Do not confuse

Retain:

- A Turing machine is a formal model for mechanical computation.
- The input alphabet $\Sigma$ describes legal input symbols.
- The tape alphabet $\Gamma$ describes all symbols the machine may use on its tape.
- The blank symbol is part of the tape alphabet, not the input alphabet.
- A computation may accept, reject, or run forever unless the machine is known to be a decider.

Do not confuse:

- the input alphabet with the tape alphabet;
- the machine's finite description with its potentially unbounded computation;
- the abstract model with a physical computer;
- halting with accepting.

---

# 2. Configurations: The Instantaneous State of a Computation

## 2.1 Why configurations must be introduced

A Turing machine definition tells us what the machine is allowed to do, but it does not by itself describe a particular moment during a run. To reason about a computation, especially in proofs, we need a precise object that captures the complete current situation of the machine.

That object is called a **configuration**. Without configurations, we cannot rigorously define what it means for one step to follow from another, what it means for a computation to halt, or how to encode an entire computation history. Later, when proving results such as Cook-Levin, configurations are the rows of a tableau. The entire proof depends on the idea that a computation can be represented as a sequence of configurations.

## 2.2 The object being introduced

A configuration is a snapshot of a Turing machine at one moment. It contains exactly the information needed to determine what can happen next:

- the current state;
- the tape contents that matter;
- the head position.

For a deterministic machine, a nonhalting configuration determines at most one next configuration. For a nondeterministic machine, a nonhalting configuration may determine several possible next configurations.

The fixed object is the machine $M$. The varying object is the configuration, which changes step by step as $M$ runs.

## 2.3 Formal definition

A configuration of a Turing machine is a finite description of:

1. the current state $q \in Q$;
2. the current tape contents, with all but finitely many cells blank;
3. the current head position.

A common notation writes a configuration as:

$$
u q v
$$

where $u$ and $v$ are strings over the tape alphabet $\Gamma$, $q$ is the current state, and the head is positioned on the first symbol of $v$. If $v$ is empty, the head is understood to be scanning a blank cell immediately to the right of $u$.

## 2.4 Interpretation

The notation $u q v$ should be read as follows. The tape has the string $uv$ written on the relevant finite region. The machine is currently in state $q$. The head is scanning the first symbol of $v$. The string $u$ lies to the left of the head, and $v$ begins at the head.

For example, the configuration

$$
01q7X0
$$

means that the machine is in state $q7$, the relevant tape contents are $01X0$, and the head is scanning the $X$. The symbols $0$ and $1$ are to the left of the head. The symbol $X$, followed by $0$, begins at the head.

The notation is not the machine itself. It is a description of one moment in one computation of that machine.

## 2.5 Boundary conditions and assumptions

The configuration notation suppresses infinitely many blank symbols. This is safe because at any finite time, only finitely many cells can have been visited or written. The rest of the tape remains blank and does not need to be written explicitly.

However, this suppression must be handled carefully. If the head moves beyond the displayed region, the missing cell is treated as blank. The notation $u q v$ is therefore a compact representation, not a claim that the tape ends after $uv$.

Another boundary condition concerns halting states. If $q = q_{\mathrm{accept}}$ or $q = q_{\mathrm{reject}}$, the configuration is halting. There is no ordinary next computation step from a halting configuration.

Finally, different textbooks use slightly different configuration notation. Some put the state before the scanned symbol; others use underlining or indexed tape positions. These notational differences do not change the concept.

## 2.6 Worked example: reading a configuration

This example is chosen because understanding configurations is essential before one can understand either deterministic or nondeterministic computation.

Consider the configuration:

$$
abqXc
$$

Assume the tape alphabet contains $a$, $b$, $X$, $c$, and $\sqcup$. The configuration tells us that the relevant tape region currently looks like:

$$
abXc
$$

The machine is in state $q$. The head is scanning the first symbol after the state symbol, namely $X$. The symbols $a$ and $b$ are to the left of the head. The symbol $c$ is immediately to the right of the scanned cell.

If the transition rule says that in state $q$, scanning $X$, the machine should write $Y$, enter state $r$, and move right, then the next configuration has to reflect all three changes:

1. The scanned $X$ becomes $Y$.
2. The state changes from $q$ to $r$.
3. The head moves one cell to the right, so it now scans $c$.

The next configuration is therefore:

$$
abYr c
$$

Usually we would write this without the spacing as:

$$
abYrc
$$

The conclusion each step allows is specific. The write operation changes the tape. The state update changes the internal control. The head move changes which symbol is scanned next. A valid next configuration must account for all three.

## 2.7 Misconception block: the state symbol is not written on the tape

In the notation $u q v$, the symbol $q$ is not a tape symbol. It is inserted into the written representation to show where the head is and what state the machine is in. The actual tape contains only symbols from $\Gamma$, not states from $Q$.

This matters when encoding computations. If a proof encodes configurations as strings, it may include state symbols as part of the encoding. But the encoded representation is not the literal tape contents; it is a mathematical description of a machine snapshot.

## 2.8 Connection to later material

Configurations are the building blocks of computation histories. A complete run of a machine can be viewed as a sequence:

$$
C_0, C_1, C_2, \ldots
$$

where $C_0$ is the start configuration and each next configuration follows legally from the previous one.

For deterministic machines, this sequence has at most one continuation at each step. For nondeterministic machines, it becomes a branching tree because a configuration may have several legal successors. Later, when reductions encode computation as logic formulas, the formula does not encode a vague process. It encodes configurations and local validity checks between neighboring configurations.

## 2.9 Retain / Do not confuse

Retain:

- A configuration is a complete snapshot of a Turing machine computation.
- It records the state, tape contents, and head position.
- The notation $u q v$ usually means the head scans the first symbol of $v$.
- A computation history is a sequence of configurations.

Do not confuse:

- the state marker in a configuration notation with an actual tape symbol;
- a finite written representation with a finite tape;
- a configuration with the machine itself;
- a halting configuration with a rejected configuration only. Accepting and rejecting are both halting outcomes.

---

# 3. Deterministic Turing Machines

## 3.1 Why deterministic machines are introduced first

Deterministic Turing machines formalize the kind of computation most people already have in mind when they think of an algorithm. At every step, the current situation determines exactly what happens next. There is no branching, no choice, and no ambiguity.

This model is introduced first because it gives the baseline notion of computation. When we later define nondeterminism, the contrast will be meaningful only if we first understand determinism precisely. A nondeterministic machine is not a completely different object; it changes one part of the deterministic definition, namely the transition rule.

Deterministic machines also provide the foundation for deciders, recognizers, computable functions, and deterministic time complexity. When we say an algorithm solves a decision problem in polynomial time, the standard formal meaning is that a deterministic Turing machine decides the language in polynomial time.

## 3.2 The object being introduced

A **deterministic Turing machine**, abbreviated **DTM**, is a Turing machine whose transition rule assigns at most one legal move to each possible combination of current state and scanned tape symbol.

The fixed part is the machine's transition function. The varying part is the computation produced when the machine is run on a particular input. Since there is no branching, one input produces one computation path.

The DTM answers this question:

> Given the current state and the symbol under the head, what is the unique next action?

That unique action specifies a symbol to write, a state to enter, and a direction to move.

## 3.3 Formal definition

A deterministic Turing machine is a tuple:

$$
M = (Q, \Sigma, \Gamma, \delta, q_0, q_{\mathrm{accept}}, q_{\mathrm{reject}})
$$

where $Q$, $\Sigma$, $\Gamma$, $q_0$, $q_{\mathrm{accept}}$, and $q_{\mathrm{reject}}$ have the meanings described earlier, and the transition function has the form:

$$
\delta : (Q \setminus \{q_{\mathrm{accept}}, q_{\mathrm{reject}}\}) \times \Gamma
\to Q \times \Gamma \times \{L,R\}
$$

depending on convention, $\{L,R\}$ may be replaced by $\{L,R,S\}$, where $S$ means stay in place.

If:

$$
\delta(q,a) = (r,b,D)
$$

then when the machine is in state $q$, scanning symbol $a$, it writes symbol $b$, enters state $r$, and moves its head in direction $D$.

## 3.4 Interpretation

The transition function is the machine's program. Its input is not the whole tape. It sees only two pieces of information: the current state and the currently scanned tape symbol. Its output is the next local action.

The word "deterministic" means that for each valid input pair $(q,a)$, there is at most one prescribed action. If the transition function is total on nonhalting states, then there is exactly one action for every nonhalting state-symbol pair. Some presentations allow the transition function to be partial; in that case, a missing transition can be treated as halting without accepting, or converted into an explicit reject transition.

The crucial point is not whether the function is total or partial. The crucial point is uniqueness. There is never a moment when the deterministic machine has two different legal moves from the same configuration.

## 3.5 Boundary conditions and assumptions

The transition function is normally not defined on accepting or rejecting states. Once the machine enters $q_{\mathrm{accept}}$ or $q_{\mathrm{reject}}$, computation stops. This prevents meaningless questions such as "What does the machine do after accepting?"

The accept and reject states must be distinct. If they were the same state, halting would not distinguish yes from no.

The input is placed on the tape before computation begins, usually starting at the leftmost tape cell, with the head scanning the first input symbol. If the input is empty, the head begins on a blank cell.

The machine may run forever. Determinism does not imply termination. It only implies uniqueness of the next move while the computation continues.

The direction set is a convention. Some definitions allow only $L$ and $R$, while others allow $S$. Allowing the head to stay still is convenient but does not change the class of languages that can be recognized or decided, because a stay move can be simulated by a short sequence of left and right moves with additional states.

## 3.6 Fully worked example: a DTM deciding whether a binary string contains a 1

This example is chosen because it is simple enough to inspect completely, while still showing the meaning of states, transitions, acceptance, rejection, and head movement.

Consider the language:

$$
L = \{w \in \{0,1\}^* : w \text{ contains at least one } 1\}
$$

A deterministic machine deciding $L$ should scan the input from left to right. If it sees a $1$, it accepts. If it reaches the blank after the input without seeing any $1$, it rejects.

The relevant objects are:

- The input alphabet is $\Sigma = \{0,1\}$.
- The tape alphabet is $\Gamma = \{0,1,\sqcup\}$.
- The machine needs a scanning state $q_{\mathrm{scan}}$, an accept state, and a reject state.
- The start state can be $q_{\mathrm{scan}}$.

The transition behavior is:

1. If the machine is scanning $0$, it has not yet found a $1$. It should keep searching by moving right.
2. If the machine is scanning $1$, it has found evidence that the input belongs to $L$. It should accept.
3. If the machine is scanning $\sqcup$, it has passed the end of the finite input without finding a $1$. It should reject.

The important checks are ordered by what the scanned symbol means.

When the scanned symbol is $0$, the machine cannot conclude that the string lacks a $1$, because there may be a $1$ later. So the only justified conclusion is "continue."

When the scanned symbol is $1$, the machine can immediately conclude membership in $L$, because the language only requires at least one $1$. No later symbols can undo that fact. So acceptance is justified.

When the scanned symbol is blank, the machine has reached the first blank after the input. Under the standard input convention, all remaining cells to the right are blank unless the machine has written there, and in this example it has not. The machine can conclude that no $1$ appeared in the input. So rejection is justified.

Now consider the input $00010$. The computation begins with the head on the first symbol. The machine scans the first $0$, moves right, scans the second $0$, moves right, scans the third $0$, moves right, and then scans $1$. At that moment the condition for acceptance is met. The machine enters $q_{\mathrm{accept}}$, and the computation halts.

Consider instead the input $0000$. The machine scans each $0$ and moves right. Eventually it reaches the blank immediately after the input. Since no $1$ was seen before the blank, the machine enters $q_{\mathrm{reject}}$.

The general lesson is that a deterministic decider's reasoning often follows a pattern: maintain some finite information in the state, inspect the current symbol, and move until a decisive condition is reached. In this example, the finite information is simply "no $1$ has been seen yet."

## 3.7 Misconception block: deterministic does not mean predictable to the user

A deterministic machine may be difficult for a human to analyze. It may run for a very long time. Its behavior may depend on complicated tape markings. But mathematically, determinism means only that there is a unique next move from each nonhalting configuration.

Do not confuse "deterministic" with "easy to understand" or "fast." A deterministic computation can be long, complex, and impractical.

## 3.8 Connection to later material

DTMs are used to define deterministic language recognition, decidability, and deterministic complexity classes. A language is in $P$, for example, if some deterministic Turing machine decides it in time bounded by a polynomial in the input length.

DTMs also serve as the comparison point for nondeterministic machines. When complexity theory asks whether $P = NP$, it is asking whether every problem whose solutions can be verified through nondeterministic-style existence can also be solved efficiently by deterministic computation.

## 3.9 Retain / Do not confuse

Retain:

- A DTM has at most one legal move from any nonhalting state-symbol pair.
- One input produces one computation path.
- Determinism does not guarantee halting.
- The transition function is local: it sees only the current state and scanned symbol.
- A DTM decides a language only if it halts on every input.

Do not confuse:

- deterministic with fast;
- deterministic with always halting;
- the current state with the whole memory of the computation;
- a partial transition function with nondeterminism. Missing transitions are not branching choices.

---

# 4. Acceptance, Rejection, Recognition, and Decidability for DTMs

## 4.1 Why these distinctions are necessary

Once we have a deterministic machine, we need to say what it means for the machine to solve a problem. It is not enough to say that the machine accepts some strings. A machine may accept the strings in a language but loop forever on strings outside the language. That behavior is useful in some contexts, but it is not the same as deciding the language.

This section exists because many errors in computability theory come from collapsing three different outcomes: accepting, rejecting, and looping. A correct understanding of deterministic machines requires keeping these outcomes separate.

## 4.2 The objects being introduced

There are two important kinds of language-level behavior.

A machine **recognizes** a language if it accepts exactly the strings in the language, while it may either reject or loop on strings not in the language.

A machine **decides** a language if it accepts exactly the strings in the language and rejects every string not in the language, always halting.

Recognition is about correct acceptance of yes-instances. Decidability is about correct and terminating classification of all instances.

## 4.3 Formal definitions

Let $M$ be a deterministic Turing machine and let $L \subseteq \Sigma^*$.

$M$ **recognizes** $L$ if for every string $w \in \Sigma^*$:

$$
w \in L \quad \text{if and only if} \quad M \text{ accepts } w.
$$

Equivalently:

- if $w \in L$, then $M$ accepts $w$;
- if $w \notin L$, then $M$ does not accept $w$, meaning it either rejects or runs forever.

$M$ **decides** $L$ if for every string $w \in \Sigma^*$:

- if $w \in L$, then $M$ accepts $w$;
- if $w \notin L$, then $M$ rejects $w$;
- in all cases, $M$ halts.

A language is **Turing-recognizable** if some Turing machine recognizes it. A language is **decidable** if some Turing machine decides it.

## 4.4 Interpretation

Recognition is one-sided success. The machine is reliable when it says yes, but it may fail to give a final answer on no-instances. Decidability is two-sided success. The machine must eventually give the correct answer for every input.

The phrase "$M$ accepts $w$" has a precise meaning: the computation starting from the initial configuration on input $w$ eventually enters $q_{\mathrm{accept}}$. The phrase "$M$ rejects $w$" means it eventually enters $q_{\mathrm{reject}}$. The phrase "$M$ loops on $w$" means it never enters either halting state.

In deterministic computation, each input has only one run, so these outcomes are mutually exclusive: accept, reject, or loop.

## 4.5 Boundary conditions and assumptions

A recognizer is allowed to run forever on inputs outside its language. This is not a bug in the definition; it is the point of the distinction.

A decider must halt on every input. It is not enough that it usually halts, or that it halts on all inputs in the language. It must halt on both yes-instances and no-instances.

A rejecting halt is different from looping. Both are nonacceptance, but only rejection gives a definite no answer.

Some texts define machines with only an accept halt and treat all other halting as rejection. Others explicitly include accept and reject states. The conceptual distinction remains the same.

## 4.6 Fully worked example: recognition without decidability behavior

This example is chosen because it shows why acceptance alone does not imply decision.

Let $L$ be the language of binary strings containing at least one $1$. The DTM from the previous section decides $L$, because it accepts strings with a $1$ and rejects strings with no $1$.

Now modify the machine. It still scans right until it sees a $1$. If it sees a $1$, it accepts. But if it reaches the blank at the end without seeing a $1$, instead of rejecting, it moves right forever over blank cells.

This modified machine still recognizes $L$. For any input containing at least one $1$, the machine eventually sees a $1$ and accepts. For any input not containing a $1$, the machine never accepts. That satisfies the recognition definition.

But it does not decide $L$. On input $000$, for example, the machine does not halt. It gives no final answer. The boundary between recognition and decision appears exactly here: the machine is correct about yes-instances, but incomplete on no-instances.

The general lesson is that "does not accept" includes both rejection and nontermination. When proving decidability, one must show halting on every input, not merely correctness of acceptance.

## 4.7 Misconception block: rejecting and looping are not equivalent

It is tempting to say that if a machine does not accept, then it rejects. That is false. A computation may fail to accept because it runs forever.

This distinction is essential in undecidability. Many undecidable languages are recognizable: there is a machine that eventually accepts yes-instances, but no machine can always halt with the right yes/no answer.

## 4.8 Connection to later material

Recognition and decidability become central in the study of the halting problem, reductions, recursively enumerable languages, and decidable languages. In complexity theory, the focus often shifts to deciders because time complexity is normally measured for computations that halt on all inputs.

For nondeterministic machines, the acceptance condition changes in an important way: acceptance means at least one branch accepts. That makes it even more important to understand acceptance, rejection, and nontermination carefully before moving to nondeterminism.

## 4.9 Retain / Do not confuse

Retain:

- A recognizer must accept exactly the strings in the language.
- A recognizer may loop on strings outside the language.
- A decider must halt on every input.
- Rejection is a halting no answer.
- Looping is not a no answer; it is no answer at all.

Do not confuse:

- nonacceptance with rejection;
- recognizability with decidability;
- halting with accepting;
- correctness on yes-instances with full decision power.

---

# 5. Nondeterministic Turing Machines

## 5.1 Why nondeterministic machines are introduced

Nondeterministic Turing machines are introduced to formalize a different way of representing search. Many computational problems have the following structure: a proposed solution is easy to check, but finding such a solution may require exploring many possibilities.

For example, consider satisfiability. Given a Boolean formula, it may be hard to find a satisfying assignment. But if someone gives you an assignment, checking whether it satisfies the formula is straightforward. Nondeterminism models this kind of "there exists a successful choice sequence" structure.

A nondeterministic machine does not need to be interpreted as a physical device that magically guesses correctly. It is a mathematical model in which computation branches into multiple possible continuations. The machine accepts if at least one branch accepts.

This section cannot be skipped because nondeterminism is the foundation of NP, reductions involving verification, and the Cook-Levin theorem. Understanding nondeterminism as branching computation prevents many later misconceptions.

## 5.2 The object being introduced

A **nondeterministic Turing machine**, abbreviated **NTM** or **NDTM**, is a Turing machine whose transition rule may allow multiple legal next moves from the same current state and scanned symbol.

The fixed object is the machine and its finite transition relation. The varying object is no longer a single computation path. Instead, a given input produces a computation tree. Each node is a configuration, and each edge represents one legal transition.

The machine answers this question:

> Is there at least one legal computation path from the start configuration to an accepting configuration?

This existential question is the core of nondeterministic acceptance.

## 5.3 Formal definition

A nondeterministic Turing machine is a tuple:

$$
N = (Q, \Sigma, \Gamma, \delta, q_0, q_{\mathrm{accept}}, q_{\mathrm{reject}})
$$

where $Q$, $\Sigma$, $\Gamma$, $q_0$, $q_{\mathrm{accept}}$, and $q_{\mathrm{reject}}$ have their usual meanings, but the transition rule has the form:

$$
\delta : (Q \setminus \{q_{\mathrm{accept}}, q_{\mathrm{reject}}\}) \times \Gamma
\to \mathcal{P}(Q \times \Gamma \times \{L,R\})
$$

Here $\mathcal{P}(S)$ denotes the power set of $S$, the set of all subsets of $S$.

If:

$$
\delta(q,a) = \{(r_1,b_1,D_1), (r_2,b_2,D_2), \ldots, (r_k,b_k,D_k)\}
$$

then when the machine is in state $q$, scanning symbol $a$, it may choose any one of these $k$ moves. Each move produces a different possible successor configuration.

## 5.4 Interpretation

The transition rule of an NTM returns a set of possible actions rather than a single action. If that set has size zero, the branch has no legal continuation. Depending on convention, such a branch may be treated as rejecting or simply dead. What matters for acceptance is whether some branch reaches $q_{\mathrm{accept}}$.

The power set notation can look abstract, but its role is simple. The expression $\mathcal{P}(Q \times \Gamma \times \{L,R\})$ says that for each state-symbol pair, the transition rule returns a finite collection of possible triples. Each triple is one possible next move.

A deterministic machine is a special case of a nondeterministic machine where each transition set has at most one element. Thus nondeterminism extends determinism; it does not replace it.

## 5.5 Boundary conditions and assumptions

An NTM still has a finite description. It may branch during computation, but its transition rule is finite. There is no infinite menu of choices built into one step.

Each branch follows ordinary Turing machine rules. A branch writes one symbol, changes to one state, and moves one cell at a time. Nondeterminism affects choice among transitions, not the local mechanics of a transition.

Acceptance is existential: one accepting branch is enough. Rejection is usually universal for halting trees: the machine rejects an input only if all branches reject or die without accepting, under conventions where all branches halt. If some branches run forever and none accept, the machine does not accept; depending on the formal setting, it may fail to decide.

For complexity classes such as NP, we usually restrict attention to nondeterministic deciders running within a time bound on all branches. This prevents infinite branches from disrupting the definition.

## 5.6 Fully worked example: an NTM for strings containing either 00 or 11

This example is chosen because it illustrates nondeterministic branching without requiring a complicated problem. The language is:

$$
L = \{w \in \{0,1\}^* : w \text{ contains } 00 \text{ or } 11 \text{ as a substring}\}
$$

A deterministic machine could scan the input and remember the previous symbol. A nondeterministic machine can be described differently: it may choose a position and check whether that position begins a repeated-symbol pair.

The nondeterministic idea is not that the machine knows where the pair is. The idea is that the computation tree contains one branch for each possible choice of position. If any chosen position starts $00$ or $11$, that branch accepts.

The object being varied is the chosen position. The input string is fixed. The machine's transition relation allows branches that move right different numbers of times before checking.

Consider input:

$$
w = 010011
$$

There are repeated pairs at positions $3$-$4$, where the substring is $00$, and at positions $5$-$6$, where the substring is $11$, using one-based indexing.

The computation begins at the leftmost symbol. At each position, the NTM has two conceptual options:

1. choose this position as the start of the candidate pair;
2. skip this position and move right.

These options create branches. On the branch that chooses position 1, the machine sees $0$ followed by $1$, so that branch fails. On the branch that chooses position 2, the machine sees $1$ followed by $0$, so that branch fails. On the branch that chooses position 3, the machine sees $0$ followed by $0$, so that branch accepts.

Because at least one branch accepts, the NTM accepts $010011$.

Now consider input:

$$
w = 01010
$$

Every adjacent pair alternates: $01$, $10$, $01$, $10$. Each branch that chooses a position and checks the next symbol fails. The branch that keeps skipping eventually reaches the end. No branch accepts. Therefore the NTM does not accept this input. If the machine is designed so every branch halts, then it rejects this input.

The general lesson is that nondeterminism expresses existential search. The machine accepts because there exists a position that passes the local check. It does not need all choices to work.

## 5.7 Misconception block: nondeterminism is not parallelism in the ordinary engineering sense

It is common to imagine an NTM as a machine that runs all branches in parallel. This image can be useful at first, but it is not the formal definition. The formal definition is a branching computation tree with an existential acceptance condition.

Actual parallel hardware has resource constraints and synchronization costs. Nondeterminism is a mathematical abstraction. It is used because it captures the structure of "there exists a certificate" or "there exists a successful sequence of choices."

## 5.8 Connection to later material

Nondeterministic machines are central to complexity theory. The class NP can be defined as the set of languages decidable by a nondeterministic Turing machine in polynomial time. Equivalently, NP can be described using polynomial-time verification of certificates.

The bridge between these two views depends on understanding nondeterministic computation as a finite sequence of choices. A certificate can encode the choices of an accepting branch. A deterministic verifier can then check that those choices produce a valid accepting computation.

This is also the conceptual bridge behind Cook-Levin: an accepting nondeterministic computation can be encoded as a tableau, and the existence of such a tableau can be expressed as a Boolean satisfiability instance.

## 5.9 Retain / Do not confuse

Retain:

- An NTM may have several legal moves from the same configuration.
- One input produces a computation tree, not a single path.
- The NTM accepts if at least one branch accepts.
- Deterministic machines are special cases of nondeterministic machines.
- Nondeterminism models existential search.

Do not confuse:

- "some branch accepts" with "all branches accept";
- nondeterminism with randomness;
- nondeterminism with ordinary parallel hardware;
- a branching computation tree with multiple different machines.

---

# 6. Computation Trees for Nondeterministic Machines

## 6.1 Why computation trees are necessary

For deterministic machines, a computation can be represented as a single sequence of configurations. For nondeterministic machines, that representation is no longer enough. From one configuration, several next configurations may be possible. Therefore the natural object is a tree.

This section exists because many later statements about nondeterministic machines are really statements about paths in a tree. Without the tree picture, the acceptance condition can seem magical. With the tree picture, it becomes precise: acceptance means that at least one root-to-node path reaches an accepting configuration.

## 6.2 The object being introduced

A **computation tree** for an NTM $N$ on input $w$ is a rooted tree whose nodes are configurations.

The root is the start configuration of $N$ on $w$. The children of a node are exactly the configurations that can be reached by one legal nondeterministic transition from that node. Accepting configurations are accepting nodes. Rejecting configurations are rejecting nodes. Branches may be finite or infinite unless the machine is guaranteed to halt on all branches.

The fixed objects are the machine $N$ and input $w$. The varying objects are the branches of the tree, each representing one possible sequence of nondeterministic choices.

## 6.3 Formal definition

Let $N$ be an NTM and $w$ an input string. The computation tree $T_{N,w}$ is defined as follows:

- The root is the initial configuration $C_0$ of $N$ on $w$.
- If a node is labeled by a nonhalting configuration $C$, its children are exactly the configurations $C'$ such that $C$ yields $C'$ by one legal transition of $N$.
- If a node is labeled by a halting configuration, it has no children.

The NTM $N$ accepts $w$ if $T_{N,w}$ contains at least one accepting node.

## 6.4 Interpretation

The computation tree organizes all possible runs at once. Each path from the root corresponds to one possible history of choices. At each branching point, the machine's transition relation offers multiple legal moves. Following one child means committing to one of those moves on that branch.

The tree is not necessarily finite. If some branch loops forever, the tree may have infinite depth. If the machine has a bounded running time on all branches, then the tree has finite depth bounded by that time.

The acceptance condition is existential over paths. The input is accepted if there exists a path whose final node is accepting.

## 6.5 Boundary conditions and assumptions

If the transition relation has at most $b$ possible moves from any state-symbol pair, then each node has at most $b$ children. The number $b$ is finite because the machine has a finite transition rule.

If the NTM runs for at most $t(n)$ steps on inputs of length $n$, then every branch has length at most $t(n)$. The total number of branches can still be exponential in $t(n)$, but each individual branch is only $t(n)$ steps long.

This distinction between branch length and number of branches is fundamental. Polynomial time for an NTM means every branch has polynomial length. It does not mean the computation tree has polynomially many nodes.

## 6.6 Fully worked example: a binary branching computation tree

This example is chosen because it shows how a small branching factor can still create many possible paths.

Suppose an NTM has exactly two possible choices at each of the first three steps. For simplicity, call the choices $A$ and $B$. The input is fixed, and the machine's choices generate possible paths such as:

$$
AAA,\ AAB,\ ABA,\ ABB,\ BAA,\ BAB,\ BBA,\ BBB
$$

There are eight possible length-three choice sequences. If the branch corresponding to $BAB$ reaches an accepting configuration, then the NTM accepts the input, regardless of what happens on the other seven branches.

The step-by-step structure is:

1. At depth $0$, there is one root configuration.
2. At depth $1$, there are at most two configurations, one for each first choice.
3. At depth $2$, each depth-one node may have two children, giving at most four configurations.
4. At depth $3$, there may be at most eight configurations.

The important conclusion is that nondeterministic time counts depth, not total tree size. If a machine makes one choice per step for three steps, each branch has length three, even though the tree may contain many nodes.

The general lesson is that nondeterminism can represent exponentially many possible choice sequences using a polynomial-length branch. This is one reason nondeterminism is powerful in complexity theory.

## 6.7 Misconception block: polynomial nondeterministic time does not mean polynomially many branches

A nondeterministic machine running in $n^2$ steps may have exponentially many branches if it has at least two choices at many steps. The time bound controls the length of each branch, not the total number of branches in the computation tree.

This distinction is crucial. NP is not the class of problems where a deterministic machine can explicitly enumerate all nondeterministic branches in polynomial time. Explicit enumeration may require exponential time.

## 6.8 Connection to later material

Computation trees connect directly to certificates. A single accepting path can be described by listing the choices made along that path. If each branch has polynomial length, then this list of choices has polynomial size. A deterministic verifier can simulate the machine while following those choices.

This observation is one reason the machine-based definition of NP and the verifier-based definition of NP are equivalent. The computation tree supplies the missing bridge: nondeterministic acceptance means existence of a path, and a certificate can identify that path.

## 6.9 Retain / Do not confuse

Retain:

- An NTM computation on one input is represented by a tree of configurations.
- Each path is one possible sequence of nondeterministic choices.
- Acceptance means at least one accepting node exists.
- A polynomial time bound limits branch depth, not total tree size.

Do not confuse:

- number of steps along a branch with number of branches;
- existence of one accepting path with acceptance of all paths;
- a computation tree with a deterministic execution trace.

---

# 7. Deterministic versus Nondeterministic Transition Rules

## 7.1 Why the transition rule deserves separate comparison

The difference between DTMs and NTMs is sometimes described casually as "one has choices and the other does not." That is true, but too vague for proof. The precise difference lies in the type of the transition rule.

This section exists to make that difference exact. Once the transition-rule distinction is clear, many later facts follow naturally: a DTM has one path, an NTM has a tree; deterministic acceptance follows one run, nondeterministic acceptance asks for one successful branch; deterministic simulation of nondeterminism may require exploring many branches.

## 7.2 The objects being compared

For a DTM, the transition rule is a function returning one move:

$$
\delta_D(q,a) = (r,b,D)
$$

For an NTM, the transition rule returns a set of moves:

$$
\delta_N(q,a) = \{(r_1,b_1,D_1), \ldots, (r_k,b_k,D_k)\}
$$

In both cases, the input to the rule is a current state $q$ and a scanned symbol $a$. In both cases, a move specifies a next state, a symbol to write, and a head direction. The difference is the number of possible moves.

## 7.3 Formal comparison

A deterministic transition function has type:

$$
\delta_D : (Q \setminus \{q_{\mathrm{accept}},q_{\mathrm{reject}}\}) \times \Gamma
\to Q \times \Gamma \times \{L,R\}
$$

A nondeterministic transition function has type:

$$
\delta_N : (Q \setminus \{q_{\mathrm{accept}},q_{\mathrm{reject}}\}) \times \Gamma
\to \mathcal{P}(Q \times \Gamma \times \{L,R\})
$$

A DTM can be viewed as an NTM where every transition set has exactly one element, or at most one element under a partial-transition convention.

## 7.4 Interpretation

The deterministic function makes the next configuration a consequence of the current configuration. The nondeterministic function makes the next configuration one of several legal possibilities.

This changes the shape of reasoning. For a deterministic machine, to prove that the machine accepts $w$, one follows the unique computation and shows that it reaches $q_{\mathrm{accept}}$. For a nondeterministic machine, to prove that it accepts $w$, one only needs to exhibit one accepting path. To prove that it rejects $w$, one must rule out every accepting path, usually by showing that all branches halt and reject.

## 7.5 Boundary conditions and assumptions

The power set in the nondeterministic transition type does not allow infinite branching in standard Turing machines. Because $Q$, $\Gamma$, and the direction set are finite, the set $Q \times \Gamma \times \{L,R\}$ is finite, and every subset is finite.

A deterministic transition function is not nondeterministic merely because it is complicated. Complexity of the rule is not branching. Branching means multiple legal next moves from the same state-symbol pair.

A partial deterministic transition function should not be confused with nondeterminism. If $\delta(q,a)$ is undefined, that means there is no move, not many moves.

## 7.6 Fully worked example: same local situation, different meanings

This example is chosen because it isolates the exact point where determinism and nondeterminism diverge.

Suppose the machine is in state $q$ scanning symbol $0$.

For a DTM, suppose:

$$
\delta_D(q,0) = (r,1,R)
$$

There is only one legal action. The machine must write $1$, enter state $r$, and move right. If someone proposes that the machine could instead write $0$ and move left, that proposal is not part of the machine's computation. It is simply illegal.

For an NTM, suppose:

$$
\delta_N(q,0) = \{(r,1,R),(s,0,L)\}
$$

Now there are two legal actions. One branch writes $1$, enters $r$, and moves right. Another branch writes $0$, enters $s$, and moves left. Both branches are legitimate continuations of the same configuration.

The conclusion depends on the type of transition rule. In the deterministic case, the current configuration has one successor. In the nondeterministic case, the current configuration has two successors. This single local difference propagates into a global difference: a path versus a tree.

## 7.7 Misconception block: nondeterminism does not mean the transition rule is unknown

The transition rule of an NTM is completely specified. There is no uncertainty about what moves are allowed. Nondeterminism means that several moves are permitted, not that the machine's behavior is unspecified.

This matters because formal proofs can inspect the transition relation exactly. When checking whether a computation branch is valid, we do not appeal to intuition about guessing; we verify that each step follows one of the allowed transitions.

## 7.8 Connection to later material

The transition-rule comparison is used directly in simulations. A deterministic machine can simulate a nondeterministic one by systematically exploring its computation tree. This may be expensive, but it shows that nondeterminism does not expand the class of decidable languages. It may, however, change time complexity dramatically.

The same comparison also explains why local constraints in Cook-Levin work. A tableau row can legally follow the previous row if the local change around the head matches one of the allowed nondeterministic transitions.

## 7.9 Retain / Do not confuse

Retain:

- A DTM transition rule returns one move.
- An NTM transition rule returns a set of moves.
- The local difference creates a global path-versus-tree difference.
- A DTM is a special case of an NTM.

Do not confuse:

- many possible inputs with nondeterminism;
- a complicated deterministic rule with a nondeterministic rule;
- undefined deterministic transitions with multiple choices;
- nondeterminism with an unknown or random transition rule.

---

# 8. Nondeterminism and Verification

## 8.1 Why verification enters the discussion

Nondeterministic computation is often easier to understand through verification. Many problems ask whether there exists an object satisfying some condition. A nondeterministic machine can be imagined as choosing such an object and then checking it. A deterministic verifier receives the object as a certificate and checks it directly.

This section exists because the verifier viewpoint is one of the most important ways nondeterministic machines are used later. It connects the machine model to the language of witnesses, certificates, and polynomial-time checking.

## 8.2 The object being introduced

A **certificate** is extra information that supports membership of an input in a language. A **verifier** is a deterministic machine that checks whether the certificate proves membership.

For a language $L$, a verifier $V$ checks pairs $(w,c)$, where $w$ is the original input and $c$ is the certificate. The input $w$ belongs to $L$ if there exists some certificate $c$ such that $V$ accepts $(w,c)$.

The fixed object is the verifier $V$. The varying objects are the input $w$ and the possible certificate $c$.

## 8.3 Formal definition

A language $L$ has a verifier $V$ if:

$$
w \in L \quad \text{if and only if} \quad \exists c \text{ such that } V(w,c) \text{ accepts.}
$$

In the polynomial-time setting, $V$ must run in time polynomial in $|w|$, and there must be a polynomial bound on the length of certificates needed for strings in $L$.

## 8.4 Interpretation

The certificate is not a proof in the broad philosophical sense. It is a finite string that the verifier can check mechanically. The verifier does not need to discover the certificate. It only needs to confirm that a proposed certificate is valid.

This matches nondeterminism. An accepting branch of an NTM can be described by the sequence of choices made along the branch. That sequence is a certificate. Conversely, an NTM can nondeterministically choose a certificate and then run the deterministic verifier.

Thus, nondeterminism and verification are two ways of expressing the same existential structure:

$$
\text{There exists a successful choice sequence.}
$$

or:

$$
\text{There exists a certificate accepted by the verifier.}
$$

## 8.5 Boundary conditions and assumptions

A certificate must have bounded length in complexity theory. If certificates were allowed to be arbitrarily long with no bound, the notion would not support polynomial-time classification.

The verifier must reject invalid certificates, but it does not need to explain why they are invalid. It only needs to halt with the correct accept/reject result for the given pair.

The existence condition is one-sided. For $w \in L$, at least one certificate must work. For $w \notin L$, no certificate may work.

The certificate is not necessarily unique. Many different certificates may prove the same input belongs to the language.

## 8.6 Fully worked example: satisfiability as verification

This example is chosen because it is the canonical bridge from nondeterminism to NP.

Let $L_{\mathrm{SAT}}$ be the language of satisfiable Boolean formulas. A formula $\varphi$ belongs to $L_{\mathrm{SAT}}$ if there exists a truth assignment that makes $\varphi$ true.

The certificate is a truth assignment to the variables of $\varphi$. If $\varphi$ has variables $x_1,\ldots,x_n$, the certificate can be a lenght-$ n $ string of truth values.

The verifier receives $(\varphi,c)$. It checks:

1. The certificate assigns a truth value to each variable of $\varphi$.
2. Each occurrence of each variable is evaluated according to that assignment.
3. Each clause or subformula is evaluated according to the Boolean connectives.
4. The final value of $\varphi$ is true.

If the final value is true, the verifier accepts. If it is false, the verifier rejects that certificate.

For example, consider:

$$
\varphi = (x_1 \lor \neg x_2) \land (x_2 \lor x_3)
$$

Let the certificate assign:

$$
x_1 = \mathrm{false}, \quad x_2 = \mathrm{false}, \quad x_3 = \mathrm{true}.
$$

The first clause is:

$$
x_1 \lor \neg x_2 = \mathrm{false} \lor \mathrm{true} = \mathrm{true}.
$$

The second clause is:

$$
x_2 \lor x_3 = \mathrm{false} \lor \mathrm{true} = \mathrm{true}.
$$

Since both clauses are true, the whole conjunction is true. The verifier accepts this certificate.

The conclusion is not merely that this one assignment works. The conclusion is that the formula is satisfiable because there exists at least one assignment that works. The verifier does not need to test all assignments once a valid certificate is supplied.

The general lesson is that nondeterministic acceptance corresponds to the existence of a witness whose validity can be checked.

## 8.7 Misconception block: a verifier does not solve the search problem by itself

A verifier checks a proposed certificate. It does not necessarily find one. For SAT, checking a given assignment is easy, but finding a satisfying assignment may be difficult.

This is the heart of the distinction between solving and verifying. NP is not defined by problems whose answers are easy to find. It is defined by problems whose yes-instances have efficiently checkable certificates.

## 8.8 Connection to later material

The verifier viewpoint is essential for understanding NP-completeness. To prove a problem is in NP, one usually describes a certificate and explains how to verify it in polynomial time. To prove NP-hardness, one usually shows how to transform known hard verification problems into the problem at hand.

Nondeterministic Turing machines provide the machine-based definition. Verifiers provide the problem-solving intuition. Both viewpoints are needed for mastery.

## 8.9 Retain / Do not confuse

Retain:

- A certificate is information that supports a yes answer.
- A verifier checks a certificate deterministically.
- $w \in L$ means at least one certificate is accepted.
- $w \notin L$ means no certificate is accepted.
- Nondeterministic accepting branches correspond to certificates.

Do not confuse:

- verifying a solution with finding a solution;
- existence of one valid certificate with all certificates being valid;
- a certificate with an arbitrary hint that need not be checkable;
- NP with problems that are necessarily easy to solve.

---

# 9. Simulating Nondeterminism Deterministically

## 9.1 Why simulation matters

Nondeterministic machines appear more powerful than deterministic machines because they can branch into many possible computations. A natural question is whether this branching lets them compute languages that deterministic machines cannot compute at all.

The answer, for standard Turing machines, is no for computability and decidability: deterministic machines can simulate nondeterministic machines by exploring their computation trees. However, the simulation may be much slower. This distinction between computability and efficiency is one of the deepest themes in theoretical computer science.

This section exists to separate two claims that are often confused:

1. Nondeterminism does not expand what is computable or decidable.
2. Nondeterminism may dramatically affect how efficiently a problem can be solved.

## 9.2 The object being introduced

A deterministic simulation of an NTM is a DTM that explores the NTM's computation tree in a systematic way. The simulator accepts if it finds an accepting branch. If the NTM is a decider whose branches all halt, the simulator can eventually determine rejection by exhausting all branches.

The fixed object is the nondeterministic machine being simulated. The varying object is the finite or infinite computation tree generated by a particular input.

## 9.3 Formal statement

If a language is recognized by a nondeterministic Turing machine, then it is recognized by a deterministic Turing machine.

If a language is decided by a nondeterministic Turing machine whose every branch halts, then it is decided by a deterministic Turing machine.

For time complexity, if an NTM runs in time $t(n)$ and has bounded branching factor $b$, a deterministic simulation can explore at most about $b^{t(n)}$ branches. Thus polynomial nondeterministic time may correspond to exponential deterministic simulation by direct tree exploration.

## 9.4 Interpretation

The deterministic simulator treats nondeterministic choices as objects to enumerate. For example, if the NTM has at most $b$ choices at every step, then a branch of length $t$ can be described by a sequence of $t$ choice numbers, each between $1$ and $b$. The simulator can try these sequences one by one and check whether any sequence leads to acceptance.

If the original NTM has an accepting branch, eventually the simulator will try the corresponding sequence and accept. If the NTM is guaranteed to halt on all branches within a finite bound, the simulator can also conclude rejection after all possible branches have been checked.

The key conceptual point is that nondeterminism can be unfolded into deterministic search. The cost is the size of the search tree.

## 9.5 Boundary conditions and assumptions

For recognizers, care is needed. If the NTM has infinite branches, a deterministic simulator that explores one branch completely before moving to the next may get stuck forever on a nonaccepting infinite branch and fail to find an accepting branch elsewhere. To avoid this, the simulator must explore the tree in a fair level-by-level manner.

For deciders with time bounds, this issue is simpler because all branches halt within a known or bounded number of steps. The simulator can explore all branches up to that bound.

The branching factor is finite because the machine's transition relation is finite. Without finite branching, level-by-level simulation would become more subtle.

## 9.6 Fully worked example: deterministic search through nondeterministic choices

This example is chosen because it shows exactly what deterministic simulation checks.

Suppose an NTM has at most two choices at each step, called choice $0$ and choice $1$, and every branch halts within three steps. The possible choice sequences of length at most three include:

$$
0,\ 1,\ 00,\ 01,\ 10,\ 11,\ 000,\ 001,\ldots,111.
$$

A deterministic simulator can check these possibilities systematically.

For each choice sequence, it starts from the initial configuration and follows the choices in order. At each step, it checks whether the specified choice is legal from the current configuration. If it is not legal, that sequence does not describe a real branch. If it is legal, the simulator updates the simulated configuration. If the simulated branch reaches $q_{\mathrm{accept}}$, the simulator accepts the original input.

If no choice sequence up to the maximum branch length leads to acceptance, and every genuine branch is known to halt within that length, the simulator rejects.

The order of checks matters:

1. Fix the input and the NTM.
2. Bound the branch length.
3. Enumerate possible choice sequences up to that length.
4. For each sequence, verify step by step that it describes a legal branch.
5. Accept if any legal branch accepts.
6. Reject only after all possible branches have been ruled out.

The conclusion is that nondeterministic acceptance can be converted into deterministic exhaustive search. What may be lost is efficiency, not correctness.

## 9.7 Misconception block: deterministic simulation does not prove $P = NP$

Since a deterministic machine can simulate a nondeterministic machine, one might think this proves that $P = NP$. It does not.

The direct simulation may take exponential time because the number of branches may grow exponentially with the branch length. $P = NP$ asks whether every polynomial-time nondeterministic computation can be simulated by a polynomial-time deterministic computation. The standard tree exploration simulation does not provide that.

## 9.8 Connection to later material

This simulation result explains why nondeterminism does not change decidability but may change complexity. In computability theory, deterministic and nondeterministic recognition are equivalent in power. In complexity theory, the relationship between deterministic polynomial time and nondeterministic polynomial time is the famous unresolved $P$ versus $NP$ problem.

The simulation idea also clarifies why certificates are useful. Instead of enumerating all branches, a certificate points to one branch directly. Verification checks that branch without searching the whole tree.

## 9.9 Retain / Do not confuse

Retain:

- A DTM can simulate an NTM by exploring its computation tree.
- Fair exploration is needed when branches may be infinite.
- For bounded-time NTMs, simulation can enumerate all bounded-length branches.
- The simulation may be exponentially slower.
- Nondeterminism does not expand decidability, but it may affect efficiency.

Do not confuse:

- computability equivalence with polynomial-time equivalence;
- existence of a deterministic simulation with efficient deterministic simulation;
- branch length with number of branches;
- finding an accepting branch with verifying a given branch.

---

# 10. Deterministic and Nondeterministic Time

## 10.1 Why time must be treated carefully

Once machines are defined, it is natural to ask how long they take. But time means something different for deterministic and nondeterministic computations unless we define it carefully.

For a deterministic machine, one input creates one computation path, so the running time is the number of steps on that path. For a nondeterministic machine, one input creates many branches. We need to specify whether the time bound applies to one branch, all branches, or the whole tree.

Complexity theory uses the length of the longest branch. This section exists because misunderstanding that convention leads directly to misunderstanding NP.

## 10.2 The object being introduced

The **running time** of a DTM on input $w$ is the number of steps before it halts.

The **running time** of an NTM on input $w$, when it is used as a decider, is the maximum number of steps taken by any branch before halting.

A machine runs in time $t(n)$ if for every input of length $n$, its running time is at most $t(n)$.

## 10.3 Formal definitions

A DTM $M$ runs in time $t(n)$ if, for every input $w$ with $|w|=n$, $M$ halts on $w$ within at most $t(n)$ steps.

An NTM $N$ runs in time $t(n)$ if, for every input $w$ with $|w|=n$, every branch of $N$'s computation on $w$ halts within at most $t(n)$ steps.

The class $P$ consists of languages decidable by a DTM in polynomial time.

The class $NP$ consists of languages decidable by an NTM in polynomial time.

## 10.4 Interpretation

For DTMs, time is path length because there is only one path. For NTMs, time is maximum branch length because the computation tree may contain many paths. A polynomial-time NTM may have exponentially many branches, but each branch is only polynomially long.

This convention matches the verifier viewpoint. An accepting branch can be described by a polynomial-length certificate. A deterministic verifier only needs to check that one branch, not the whole tree.

## 10.5 Boundary conditions and assumptions

The NTM time definition requires all branches to halt within the time bound. It is not enough for accepting branches to be short. For a nondeterministic decider, every branch must halt, so the machine gives a well-defined decision process.

Some definitions of nondeterministic time focus on accepting computations for yes-instances, but the standard complexity class NP can be cleanly defined using polynomial-time nondeterministic deciders or polynomial-time verifiers. Both definitions avoid uncontrolled infinite branches.

The input length $n$ is the length of the original input string, not the length of the tape after computation.

## 10.6 Fully worked example: polynomial branch length with exponentially many branches

This example is chosen because it targets the main misunderstanding about nondeterministic time.

Suppose an NTM on an input of length $n$ makes one binary nondeterministic choice at each of $n$ steps. Each branch therefore has length $n$. The number of possible choice sequences is:

$$
2^n
$$

because each of the $n$ positions in the choice sequence has two possibilities.

The machine's nondeterministic running time is $n$, not $2^n$, because time counts the number of steps along a branch. However, a deterministic machine that explicitly checks every branch may need to inspect $2^n$ branches.

The distinction is:

- nondeterministic time: length of a branch;
- deterministic exhaustive simulation time: number of branches times cost per branch.

The conclusion is that a polynomial-time NTM can represent an exponential search space. That does not make the search free in deterministic terms; it means nondeterminism measures the existence of a successful branch rather than the cost of enumerating all branches deterministically.

## 10.7 Misconception block: NP does not mean "not polynomial"

A common beginner mistake is to read NP as "non-polynomial." That is false. NP stands for nondeterministic polynomial time.

Problems in P are also in NP, because a deterministic polynomial-time machine is a special case of a nondeterministic polynomial-time machine. Therefore NP includes many problems that are definitely polynomial-time solvable.

## 10.8 Connection to later material

The definitions of $P$ and $NP$ are central to complexity theory. NP-completeness identifies problems that are, in a precise sense, among the hardest problems in NP. Cook-Levin shows that SAT is NP-complete by encoding accepting computations of polynomial-time NTMs as Boolean formulas.

Understanding nondeterministic time as branch length is essential for seeing why the encoded computation tableau has polynomial size. The tableau represents one accepting branch, not the entire exponentially large computation tree.

## 10.9 Retain / Do not confuse

Retain:

- DTM time is the length of the single computation path.
- NTM time is the maximum length of any branch.
- Polynomial-time NTMs may have exponentially many branches.
- $P$ uses deterministic polynomial time.
- $NP$ uses nondeterministic polynomial time or equivalently polynomial-time verification.

Do not confuse:

- NP with "not polynomial";
- branch length with tree size;
- nondeterministic time with deterministic enumeration time;
- existence of a short accepting branch with all branches accepting.

---

# 11. Worked Comparison: The Same Language Under DTM and NTM Views

## 11.1 Why a side-by-side comparison is useful

Definitions become clearer when applied to the same language. A DTM and an NTM may recognize or decide the same language, but they organize the reasoning differently. The DTM usually performs a systematic search. The NTM expresses the search as a choice followed by a check.

This section exists to show that deterministic and nondeterministic machines are not about different kinds of problems. They are different computational perspectives on languages.

## 11.2 The language being studied

Consider the language:

$$
L = \{ w \in \{0,1\}^* : w \text{ has a } 1 \text{ in some even-numbered position} \}
$$

Use one-based indexing, so the first symbol is position $1$, the second is position $2$, and so on.

The input is fixed as a binary string. The varying object is the position being inspected.

## 11.3 Deterministic view

A deterministic machine can decide $L$ by scanning from left to right while remembering whether the current position is odd or even. The state records parity.

The machine checks positions in order:

1. Start at position $1$, which is odd.
2. If the current position is odd, ignore a $1$ for purposes of this language and move to the next position.
3. If the current position is even and the symbol is $1$, accept.
4. If the machine reaches the blank after the input without accepting, reject.

The state is necessary because the tape symbol alone does not reveal whether the current position is odd or even. The machine must carry that parity information internally.

For input $0100$, the machine sees:

- position $1$: symbol $0$, odd, no acceptance;
- position $2$: symbol $1$, even, accept.

For input $1000$, the machine sees:

- position $1$: symbol $1$, odd, not enough;
- position $2$: symbol $0$, even, no acceptance;
- position $3$: symbol $0$, odd, no acceptance;
- position $4$: symbol $0$, even, no acceptance;
- blank after input, reject.

The deterministic reasoning is exhaustive in order. It checks positions until it either finds evidence or proves none exists.

## 11.4 Nondeterministic view

A nondeterministic machine can decide the same language by choosing a position and checking whether it is even and contains $1$.

The computation tree has branches corresponding to possible choices of positions. On each branch, the machine verifies two facts about the chosen position:

1. the position is even;
2. the symbol at that position is $1$.

If a branch chooses a position satisfying both facts, that branch accepts. If no such position exists, no branch accepts.

For input $0100$, the branch choosing position $2$ accepts. Therefore the NTM accepts.

For input $1000$, the branch choosing position $1$ fails because the position is odd. Branches choosing positions $2$ and $4$ fail because the symbol is $0$. Other branches fail similarly. Since no branch finds an even-position $1$, the machine rejects if all branches halt.

## 11.5 What changed and what stayed invariant

The language did not change. The input did not change. The acceptance condition at the language level did not change: the string belongs to the language exactly when there exists an even position containing $1$.

What changed is the organization of the search. The deterministic machine checks positions sequentially. The nondeterministic machine branches over possible positions and checks one candidate per branch.

The invariant structure is existential:

$$
\exists i \text{ such that } i \text{ is even and } w_i = 1.
$$

The DTM proves or disproves this existential statement by systematic inspection. The NTM accepts by having one branch choose a witnessing $i$.

## 11.6 Misconception block: an NTM does not need every branch to make a good choice

On input $0100$, branches choosing positions $1$, $3$, or $4$ fail. That does not matter. Nondeterministic acceptance requires at least one accepting branch, not all branches.

This is one of the most important rules to internalize. Bad branches do not prevent acceptance if a good branch exists.

## 11.7 Connection to later material

This example mirrors the logic of certificates. The position $i$ is a certificate. A verifier can check whether $i$ is even and whether $w_i = 1$. If such a certificate exists, the string belongs to the language.

Many NP problems have the same form, but with more complex certificates: a satisfying assignment, a Hamiltonian cycle, a subset with a target sum, a coloring of a graph, or a computation history.

## 11.8 Retain / Do not confuse

Retain:

- DTMs and NTMs can decide the same language in different ways.
- DTMs often search systematically.
- NTMs express existence through branching.
- A successful branch corresponds to a witness.

Do not confuse:

- failed nondeterministic branches with rejection of the whole input;
- the chosen witness with the whole input;
- the language-level condition with a particular machine strategy.

---

# 12. Common Equivalences and Non-Equivalences

## 12.1 Why equivalences must be stated carefully

Turing machine variants often turn out to be equivalent in computational power. This can create confusion. If deterministic and nondeterministic machines recognize the same class of languages, why does nondeterminism matter? If multiple tapes do not change computability, why study them?

The answer is that equivalence depends on what is being measured. Some changes preserve computability but affect efficiency. Some preserve polynomial time, while others may change constant factors or polynomial degrees. This section clarifies the most important equivalences and non-equivalences involving DTMs and NTMs.

## 12.2 The objects being compared

We compare models along two axes:

1. **Computability power**: which languages can be recognized or decided at all?
2. **Complexity power**: how efficiently can those languages be recognized or decided?

A model can be equivalent on the first axis but not known to be equivalent on the second.

## 12.3 Formal statements

For language recognition:

$$
\text{DTM-recognizable languages} = \text{NTM-recognizable languages}.
$$

For language decidability:

$$
\text{DTM-decidable languages} = \text{NTM-decidable languages}.
$$

For polynomial time:

$$
P \subseteq NP.
$$

Whether:

$$
P = NP
$$

is unknown.

## 12.4 Interpretation

The first equality says that nondeterminism does not allow machines to recognize languages that deterministic machines cannot recognize. A deterministic machine can simulate the nondeterministic computation tree fairly.

The second equality says that nondeterminism does not allow machines to decide languages that deterministic machines cannot decide. If all nondeterministic branches halt, the deterministic simulator can eventually explore them sufficiently to determine whether any accepts.

The inclusion $P \subseteq NP$ says every deterministic polynomial-time computation is also a nondeterministic polynomial-time computation, because an NTM can simply have one possible move at each step.

The open question $P = NP$ asks whether every polynomial-time nondeterministic decision can be matched by a polynomial-time deterministic decision.

## 12.5 Boundary conditions and assumptions

The equivalence of deterministic and nondeterministic recognition relies on finite branching and fair simulation. If a simulator explores one branch forever, it may fail even when an accepting branch exists elsewhere.

The equality of decidable languages assumes that the nondeterministic machine is a decider in the appropriate sense: all branches halt. If branches can run forever and no branch accepts, the machine may fail to decide.

The statement $P \subseteq NP$ is known. The statement $P = NP$ is not known. One must not slide from the first to the second.

## 12.6 Fully worked example: why $P \subseteq NP$

This example is chosen because it corrects the mistaken idea that deterministic and nondeterministic complexity classes are disjoint.

Suppose $L$ is in $P$. By definition, there is a deterministic Turing machine $M$ deciding $L$ in polynomial time. We can view $M$ as a nondeterministic machine $N$ with exactly one legal transition wherever $M$ has a transition.

On every input $w$, $N$ has exactly one branch. That branch is identical to $M$'s computation. If $M$ accepts, $N$ accepts. If $M$ rejects, $N$ rejects. The running time is the same polynomial bound.

Therefore $L$ is in $NP$. The conclusion follows because deterministic computation is a special case of nondeterministic computation.

This example teaches a general pattern: when one model allows everything another model allows plus more, every language solvable in the restricted model is also solvable in the more general model.

## 12.7 Misconception block: "equivalent computability" does not mean "equivalent efficiency"

Because every NTM can be simulated by a DTM, one might think nondeterminism is irrelevant. It is not. The simulation may require exponential time. Complexity theory cares about such differences.

The equality of decidable languages says both models can eventually decide the same languages. It does not say they decide them with the same time bounds.

## 12.8 Connection to later material

This careful separation of computability and complexity is essential for understanding why $P$ versus $NP$ is meaningful. If nondeterminism gave new decidable languages, the question would be about computability. Instead, the question is about efficient computation.

NP-completeness lives exactly in this space: problems that nondeterministic machines can solve in polynomial time, and for which efficient deterministic algorithms are not known.

## 12.9 Retain / Do not confuse

Retain:

- DTMs and NTMs recognize the same languages.
- DTMs and NTMs decide the same languages.
- $P \subseteq NP$.
- Whether $P = NP$ is unknown.
- Nondeterminism may affect efficiency even when it does not affect computability.

Do not confuse:

- model equivalence for decidability with model equivalence for polynomial time;
- known inclusion with unknown equality;
- deterministic as the opposite of nondeterministic in the sense of disjoint classes;
- direct simulation with efficient simulation.

---

# 13. Edge Cases and Failure Modes

## 13.1 Why edge cases matter

Formal models are often misunderstood at their boundaries. Empty input, missing transitions, infinite loops, dead branches, and rejecting branches all test whether the definitions are really understood.

This section exists to make those boundary cases explicit. Mastery requires knowing not only the standard picture, but also what happens when a machine reaches the edge of its ordinary behavior.

## 13.2 Empty input

The empty string $\epsilon$ has length $0$. It is still a valid input if $\epsilon \in \Sigma^*$, which it always is for any alphabet $\Sigma$. On empty input, the tape begins blank, and the head starts on a blank cell.

A machine deciding whether a string contains a $1$ should reject $\epsilon$, because there is no symbol at all, hence no $1$.

The misconception to avoid is thinking that no input means no computation. The machine still starts in its start state and proceeds according to what it sees, which is a blank.

## 13.3 Missing transitions

Under a partial-transition convention, a missing transition means the machine has no legal move from that state-symbol pair. For a DTM, this may be treated as halting without acceptance or converted into an explicit reject state. For an NTM, a branch with no legal moves dies.

A missing transition is not a nondeterministic choice. It is the absence of a move.

## 13.4 Infinite loops

A DTM loops on an input if its unique computation never reaches an accept or reject state.

An NTM may have some branches that halt and others that loop. For recognition, an accepting branch is enough for acceptance. If no branch accepts and at least one branch loops, the machine does not accept, but it also may not reject in the decider sense.

This is why nondeterministic deciders are usually required to halt on all branches.

## 13.5 Rejecting branches in NTMs

A rejecting branch does not force the NTM to reject the input. It only means that this branch failed. The input is accepted if some other branch accepts.

The whole input is rejected only when acceptance is impossible across all branches, and under decider conventions, all branches halt without accepting.

## 13.6 Worked example: one accepting branch and many rejecting branches

This example is chosen because it directly targets the most common error in NTM acceptance.

Suppose an NTM has four branches on input $w$. Three branches reject, and one branch accepts. The NTM accepts $w$.

The reasoning is:

1. The computation tree contains an accepting node.
2. Nondeterministic acceptance is existential.
3. Therefore $w$ is accepted.
4. The rejecting branches do not override the accepting branch.

Now suppose all four branches reject. Then the machine rejects $w$, assuming those are all the branches and all halt.

Now suppose three branches reject and one branch loops forever. No branch accepts. The machine does not accept $w$. But unless the model treats the looping branch in a special way, the machine is not a decider on $w$, because not all branches halt.

The general lesson is that for NTMs, accepting is easier to establish than rejecting. To establish acceptance, find one accepting branch. To establish rejection, rule out all accepting branches.

## 13.7 Misconception block: nondeterministic rejection is not symmetric with acceptance

Acceptance is existential: some branch accepts.

Rejection, for a halting nondeterministic decider, is universal: all branches reject.

This asymmetry is fundamental. Do not reason as if one rejecting branch proves rejection. It does not.

## 13.8 Connection to later material

The asymmetry between acceptance and rejection is one reason NP and coNP are different classes in complexity theory. NP captures efficiently verifiable yes-certificates. coNP captures languages whose no-instances have efficiently verifiable certificates. Whether NP equals coNP is also unknown.

Understanding this asymmetry at the machine level prepares the reader for those later distinctions.

## 13.9 Retain / Do not confuse

Retain:

- Empty input is a real input.
- Missing transitions are not choices.
- DTMs have one run; NTMs may have halting and nonhalting branches.
- One accepting branch makes an NTM accept.
- Rejection for NTMs requires no accepting branches, and for deciders, all branches halt.

Do not confuse:

- one rejecting branch with rejection of the input;
- looping with rejection;
- no input with no computation;
- a dead branch with an accepting or rejecting whole-machine outcome unless the convention says so.

---

# 14. How These Models Are Used Later

## 14.1 Why this final synthesis matters

The definitions in this chapter are not isolated. They are tools used repeatedly in computability and complexity theory. A student who memorizes the definitions but does not see their future use will struggle when the models reappear inside reductions, undecidability proofs, and NP-completeness arguments.

This section exists to consolidate the main conceptual roles of DTMs and NTMs.

## 14.2 DTMs as models of algorithms

Deterministic Turing machines formalize ordinary algorithms. When a proof says "there exists an algorithm deciding this language," it can be made precise as "there exists a DTM deciding this language."

DTMs are especially important when showing that a problem is decidable. A decidability proof often describes a deterministic procedure and argues that it halts with the correct answer on every input.

In complexity theory, DTMs define deterministic resource classes such as $P$, $EXP$, and deterministic space classes.

## 14.3 NTMs as models of existential search

Nondeterministic Turing machines formalize existential search. They are especially useful when a problem has the form:

$$
\text{Does there exist an object satisfying a checkable property?}
$$

The NTM branches over candidate objects or choices and accepts if some branch verifies success.

This makes NTMs natural for defining NP. Problems in NP often ask whether there exists a certificate of polynomial length that can be checked in polynomial time.

## 14.4 Computation histories as proof objects

Both DTMs and NTMs produce sequences of configurations along a branch. These sequences are computation histories.

A computation history can itself become a mathematical object to encode, inspect, or verify. This is exactly what happens in proofs such as Cook-Levin. A Boolean formula can be constructed to say:

- the first row is the start configuration;
- each row legally follows from the previous row;
- some row contains an accepting state.

The reason this works is that Turing machine computation is local. A valid next configuration differs from the previous one only near the head. That locality lets logical formulas enforce correctness with local constraints.

## 14.5 Misconception block: the machine model is not disposable after intuition is gained

It is tempting to treat Turing machines as a temporary teaching device and then abandon them for informal algorithms. That is dangerous. Informal reasoning is often enough for intuition, but formal models are needed when proving impossibility, completeness, or complexity bounds.

Turing machines remain in the background even when not explicitly mentioned. They supply the formal meaning of "algorithm," "decider," "recognizer," "polynomial time," and "nondeterministic polynomial time."

## 14.6 Retain / Do not confuse

Retain:

- DTMs formalize ordinary deterministic algorithms.
- NTMs formalize branching existential search.
- Configurations and computation histories are central proof objects.
- Local transition rules make computation encodable.
- Complexity classes depend on precise machine-based resource bounds.

Do not confuse:

- informal algorithm descriptions with formal proofs;
- nondeterministic choice with physical magic;
- a computation history with the entire computation tree;
- verification with search.

---

# 15. Final Synthesis

A deterministic Turing machine and a nondeterministic Turing machine share the same basic architecture: states, alphabets, a tape, a head, and halting states. The decisive difference is the transition rule. A DTM has at most one legal move from each nonhalting state-symbol pair. An NTM may have several.

That local difference changes the global shape of computation. A DTM produces one computation path on a given input. An NTM produces a computation tree. A DTM accepts if its unique path reaches the accept state. An NTM accepts if at least one branch reaches the accept state.

This difference does not change which languages can be recognized or decided in principle, because deterministic machines can simulate nondeterministic machines by exploring their computation trees. But it may change efficiency. A polynomial-length nondeterministic branch may exist inside an exponentially large tree. This is why nondeterminism is central to NP and why deterministic simulation does not settle $P$ versus $NP$.

The deepest lesson is that nondeterminism is a way to formalize existence. When a problem asks whether there exists a satisfying assignment, a valid path, a suitable subset, a graph coloring, or an accepting computation history, nondeterminism gives a machine-level language for that structure. Deterministic verification gives the certificate-level language for the same structure.

The student should now be able to read later material with the right mental model:

- A DTM is one disciplined computation path.
- An NTM is a tree of possible computation paths.
- A configuration is a complete snapshot.
- A computation history is a sequence of configurations along one path.
- Recognition and decision differ because looping is neither acceptance nor rejection.
- Nondeterministic acceptance is existential.
- Nondeterministic rejection, for deciders, is universal over branches.
- Polynomial nondeterministic time bounds branch length, not total tree size.
- The machine model matters because it makes these claims precise enough to prove.

---

# 16. Mastery Checklist

Use this section as a final conceptual audit.

You understand deterministic Turing machines if you can explain why the current state and scanned symbol determine a unique next move, why one input gives one computation path, and why determinism does not imply halting or efficiency.

You understand nondeterministic Turing machines if you can explain why the transition rule returns a set of moves, why one input gives a computation tree, and why one accepting branch is enough for acceptance.

You understand configurations if you can identify the state, tape contents, and head position from a notation such as $u q v$, and if you can explain how one configuration legally yields another.

You understand recognition and decidability if you can distinguish accepting, rejecting, and looping, and if you can explain why a recognizer may fail to halt on no-instances while a decider may not.

You understand nondeterministic time if you can explain why a machine with polynomial-length branches may still have exponentially many branches, and why direct deterministic simulation may therefore be exponential.

You understand the connection to NP if you can explain how an accepting branch corresponds to a certificate and how a deterministic verifier checks that certificate.

