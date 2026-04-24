# Applied Rigorous Specification: Read-Only Tool-Use Evaluation on `tanbiralam/claude-code/src`

## 0. Purpose and Scope

This document specializes the earlier general specification for **read-only repository question answering on a fixed Ubuntu filesystem snapshot** to the repository subtree:

```text
https://github.com/tanbiralam/claude-code/tree/main/src
```

The goal is to define, rigorously and without compression, how to model a tool-using coding agent that answers questions about this `src/` tree by choosing among repository-inspection actions such as search, grep-like content search, file read, and final answer. The purpose is not to reimplement the entire application. The purpose is to construct a mathematically clean experimental environment for studying **tool-use policy quality**.

The central object is a **finite-horizon partially observable decision process** induced by a real agentic codebase. The relevant source tree contains an agent loop, tool registry, tool interface, tool implementations, permission checks, message history, compaction, memory-related logic, and other runtime machinery. For a rigorous first experiment, this document defines a restricted benchmark that keeps the repository frozen and permits only read-only analysis tools. The full runtime is then treated as a richer extension.

The document defines:

1. the source paths that matter;
2. the benchmark boundary;
3. the formal environment;
4. observations, actions, transitions, admissibility, and rewards;
5. learner information state and policy class;
6. value objects and objectives;
7. data collection, exploration, and credit assignment;
8. argument-generation semantics;
9. conformance testing;
10. evaluation estimands;
11. statistical protocol;
12. baselines and ablations;
13. generalization axes;
14. failure taxonomy;
15. reproducibility bundle;
16. theorem-style correctness claims.

The recurring principle is:

> Tool implementations are environment mechanics. Tool selection, argument construction, continuation, and stopping are policy decisions.

That distinction is the backbone of the rigorous formulation.

---

## 1. Source Paths to Inspect

The following paths are the applied reading map for `tanbiralam/claude-code/src`. The exact content may change with repository updates, so the experiment must freeze a commit hash before any formal evaluation.

### 1.1 Top-Level Runtime and Query Loop Paths

```text
src/QueryEngine.ts
src/query.ts
src/main.tsx
src/replLauncher.tsx
src/interactiveHelpers.tsx
```

These paths matter because they define or connect the main interactive loop. For this project, the most important conceptual function of the query layer is that it receives user input, constructs context, calls the language model, receives possible tool-use blocks, executes tools through a tool-execution layer, appends the tool results back into the conversation, and repeats until a terminal response or a budget boundary occurs.

For the rigorous environment, the query layer is not itself the learned object unless the experiment explicitly studies runtime orchestration. In the minimal benchmark, the query layer is abstracted as an interaction loop that repeatedly asks the policy for an action and feeds back observations.

### 1.2 Tool Registry and Tool Interface Paths

```text
src/tools.ts
src/Tool.ts
src/services/tools/toolOrchestration.ts
src/services/tools/StreamingToolExecutor.ts
```

These paths matter because they define the available tool universe, the interface every tool must satisfy, and the execution pathway for tool calls.

For rigor, the tool registry determines the possible action types. The tool interface determines the action grammar. The tool orchestration path determines how a structured tool call becomes a concrete environment transition.

### 1.3 Read-Only Tool Paths for the First Benchmark

```text
src/tools/GlobTool/GlobTool.ts
src/tools/GrepTool/GrepTool.ts
src/tools/FileReadTool/FileReadTool.ts
```

The first rigorous sub-environment should use only these read-oriented tools, plus a terminal answer action. The induced action types are:

```text
glob/search_name
repeatable content search/grep
read file or read file slice
answer
stop/fail
```

These tools form the simplest useful pipeline:

```text
find candidate paths -> search candidate content -> read evidence -> answer
```

### 1.4 Higher-Risk or Later-Stage Tool Paths

```text
src/tools/FileEditTool/FileEditTool.ts
src/tools/FileWriteTool/FileWriteTool.ts
src/tools/BashTool/BashTool.ts
src/tools/NotebookEditTool/NotebookEditTool.ts
src/tools/WebFetchTool/WebFetchTool.ts
src/tools/WebSearchTool/WebSearchTool.ts
src/tools/AgentTool/AgentTool.ts
src/tools/TodoWriteTool/TodoWriteTool.ts
src/tools/TaskOutputTool/TaskOutputTool.ts
src/tools/TaskStopTool/TaskStopTool.ts
```

These are not part of the first theorem-level benchmark. They introduce side effects, external dependencies, subagent behavior, web nondeterminism, task coordination, or planning artifacts. They can be added later, but each addition changes the formal environment.

The key boundary is:

```text
Read/search tools reveal state.
Write/edit/bash tools modify state.
Web tools introduce external non-repository state.
Agent/task tools introduce nested policies.
Memory tools introduce cross-episode or cross-turn persistence.
```

### 1.5 Permission, Context, Memory, and Compaction Paths

```text
src/hooks/useCanUseTool.ts
src/context.ts
src/utils/messages.ts
src/utils/attachments.ts
src/utils/toolResultStorage.ts
src/services/compact/
src/memdir/
src/state/
src/tasks.ts
src/Task.ts
```

These paths matter for full-runtime rigor. They can change what the model sees, which tools it can use, whether actions are allowed, how results are stored or truncated, and whether memory-like context is injected.

For the first benchmark, the clean choice is:

```text
memory disabled
compaction disabled or fixed
permissions deterministic
read-only tools enabled
write/edit/bash/web/agent tools disabled
fresh runtime state per episode
```

If these are not fixed, the benchmark is not a fixed POMDP.

---

## 2. Legal and Methodological Boundary

The referenced repository publicly describes itself as a leaked source archive. A class project should avoid depending on redistribution, modification, or reproduction of proprietary code. The rigorous benchmark can still be stated in a clean-room way:

1. freeze a public repository snapshot for academic analysis;
2. use the observed architecture only to choose abstractions;
3. implement a minimal independent read-only environment with equivalent search/read semantics;
4. report source paths as motivation, not as required dependency.

The mathematical environment defined here does not require executing the original application. It requires only a frozen filesystem snapshot and specified read-only tool semantics.

---

## 3. Three Levels of Modeling

The repository can be modeled at three levels. Rigorous work should explicitly state which level is being used.

### 3.1 Level A: Induced Read-Only Repo-QA Benchmark

This is the recommended first level.

Only the following action types are enabled:

```text
glob/search-name
content-search/grep
file-read
answer
stop-fail
```

The repository is frozen. The filesystem does not change. The environment is deterministic conditional on the task instance and the action. The only stochasticity comes from task sampling and policy sampling.

This level supports the strongest mathematical claims.

### 3.2 Level B: Claude-Code-Style Tool Loop Benchmark

This level preserves the idea of an agent loop with a tool registry, schemas, tool results, budget, and message history. It still disables write/edit/bash/web/memory to preserve read-only semantics.

At this level, observations resemble a conversation transcript and tool-use messages. The action grammar resembles structured tool calls. The policy is closer to an LLM wrapper.

This level is more realistic than Level A but still controlled.

### 3.3 Level C: Full Runtime POMDP

This level includes the complete runtime: all tools, permissions, budgets, memory injection, compaction, subagents, background tasks, feature flags, and state persistence.

This is not recommended as the first rigorous environment. It is a valid research target, but it requires a much larger formal state, more transition cases, more conformance tests, and a more complicated safety model.

The rest of this document defines Level A in full, then states the modifications needed for Level B and Level C.

---

## 4. Frozen Filesystem Snapshot

### 4.1 Repository Snapshot

Let `c` be a fixed commit identifier of `tanbiralam/claude-code`. Let $R_c$ be the repository snapshot at commit $c$, and let $R_{\text{src}}$ be the subtree $R_c/\texttt{src}$.

The benchmark filesystem state is the immutable tree `R_src`.

No episode may modify `R_src`. All tool calls are read-only. If the underlying implementation uses a real Ubuntu filesystem, the benchmark runner must mount or copy the snapshot in read-only mode, or must verify after each episode that the file tree digest is unchanged.

### 4.2 Filesystem Objects

Let `P` be the finite set of normalized relative paths under `src/` at commit `c`.

For each path `p in P`, define:

- $\mathrm{kind}(p) \in \{\text{file}, \text{directory}, \text{symlink}, \text{other}\}$,
- $\mathrm{content}(p)$ is the byte sequence if $p$ is a regular file,
- $\mathrm{text}(p)$ is the decoded text if $\mathrm{content}(p)$ is valid under the benchmark encoding policy.

The benchmark must define:

1. path root: `src/`;
2. path representation: normalized POSIX-style relative paths;
3. disallowed path elements: `..`, absolute paths, null bytes;
4. symlink policy: either reject symlinks or resolve only if target stays inside `src/`;
5. binary file policy: reject or return a fixed binary marker;
6. encoding: UTF-8 with replacement or strict UTF-8 rejection;
7. line numbering: one-indexed or zero-indexed, fixed globally;
8. newline handling: preserve original or normalize to `\n`, fixed globally.

Without these decisions, `read_file` and `grep` are not mathematically well-defined.

### 4.3 Repository Digest

Define a snapshot digest:

$$
D(R_{\text{src}}) = \mathrm{hash}\big(\mathrm{sort}\{(\text{path}, \mathrm{kind}, \mathrm{content\_hash})\}\big).
$$

The runner should compute `D(R_src)` before evaluation and after evaluation. The digest must be identical. This verifies read-only environment invariance.

---

## 5. Task Distribution

### 5.1 Episode Instance

An episode instance is:

$$
\omega = (R_{\text{src}}, q, Y^{\star}, E^{\star}, m).
$$

where:

- `R_src` is the frozen source snapshot;
- `q` is a natural-language question about the source tree;
- `Y_star` is the set of acceptable correct answers;
- `E_star` is the set of answer-supporting evidence locations;
- `m` is metadata used only for evaluation and not shown to the agent unless explicitly allowed.

Evidence locations have the form:

$$
(\text{path}, \texttt{line\_start}, \texttt{line\_end}, \texttt{evidence\_role}).
$$

where `evidence_role` may be one of:

```text
definition
caller
callee
registry-entry
configuration
permission-check
runtime-loop
memory-injection
budget-control
other
```

### 5.2 Task Types

The benchmark may include several question families. Each family should have a separate identifier.

Recommended families for `claude-code/src`:

1. **Tool registry questions**: ask which tool class is included or how a tool is registered.
2. **Tool interface questions**: ask which fields a tool must define.
3. **Read-only pipeline questions**: ask how a code-search or file-read flow is represented.
4. **Query loop questions**: ask where tool-use results enter the conversation loop.
5. **Permission questions**: ask what mechanism decides whether a tool can be used.
6. **Budget questions**: ask where max turns, token budget, or tool-result budget enters.
7. **Memory-context questions**: ask where memory or attachment context can be injected.
8. **Failure-routing questions**: ask where missing tool results, invalid calls, or errors are represented.

The first benchmark should prefer families 1 through 4 because they can be answered using read/search tools without modifying the repository.

### 5.3 Task Distribution

Let `Omega` be a distribution over episode instances. In practice, `Omega` is approximated by a finite dataset:

$$
D = \{\omega_i\}_{i=1}^{N}.
$$

If tasks are generated by humans, the generation procedure must be documented. If tasks are generated automatically, the generator must be specified and frozen.

### 5.4 Train, Validation, and Test Splits

Define three disjoint sets:

```text
D_train
D_val
D_test
```

The following conditions must hold:

1. `D_train`, `D_val`, and `D_test` are disjoint at the episode level.
2. The answer strings in `D_test` are not used for training.
3. The test set is not inspected for prompt tuning, reward tuning, feature selection, or hyperparameter selection.
4. If multiple questions share the same evidence location, grouped splitting should be used to prevent leakage.

A stronger split is by evidence file:

$$
\\mathrm{files}(E^{\\star}(\\omega_i)) \\cap \\mathrm{files}(E^{\\star}(\\omega_j)) = \\emptyset.
$$

for train-test pairs. This tests whether the policy generalizes beyond memorized source locations.

### 5.5 Generalization Splits

Different splits answer different questions.

Same-repo, new-question split:

```text
train and test use the same R_src but different questions
```

This tests question-level generalization.

Same-repo, held-out-file split:

```text
test evidence files are excluded from train evidence files
```

This tests file-discovery generalization.

New-commit split:

```text
train on commit c_train, test on commit c_test
```

This tests robustness to code evolution.

New-repo split:

```text
train on claude-code/src, test on a different repository
```

This tests broader code-agent generalization.

The first project should use same-repo new-question plus, if possible, held-out-file evaluation.

---

## 6. Formal Environment

### 6.1 Environment Class

The benchmark is a finite-horizon POMDP:

$$
M = (S, A, O, P, Z, R, H, \gamma, \rho_0).
$$

where:

- `S` is the hidden state space;
- `A` is the structured action space;
- `O` is the observation space;
- `P` is the transition kernel;
- `Z` is the observation kernel;
- `R` is the reward function;
- `H` is the maximum number of decision steps;
- `gamma` is the discount factor;
- `rho_0` is the initial-state distribution induced by `Omega`.

Because the agent does not observe the whole repository at once, the problem is partially observable. Because `H` is finite, every episode terminates by construction.

### 6.2 Hidden State

At decision step `t`, the hidden state is:

$$
s_t = (\omega, h_{t-1}, b_t, \xi_t).
$$

where:

- `omega = (R_src, q, Y_star, E_star, m)` is the task instance;
- `h_{t-1}` is the full action-observation history before step `t`;
- `b_t` is the remaining step budget;
- `xi_t` is runtime metadata needed to make transitions deterministic.

For Level A, `xi_t` includes only deterministic bookkeeping:

$$
\xi_t =
(\texttt{seen\_paths}_t, \texttt{read\_ranges}_t, \texttt{search\_queries}_t, \texttt{terminal\_flag}_t).
$$

For Level B, `xi_t` may also include:

```text
message transcript
read-file cache state
tool-result truncation state
budget counters
permission decisions
effective enabled-tool set
```

For Level C, `xi_t` additionally includes:

```text
memory state
compaction state
slash-command state
subagent/task state
plugin state
external-tool state
```

### 6.3 Initial State

An initial state is sampled by:

- $\omega \sim \Omega$,
- $h_0$ is the empty history,
- $b_1 = H$,
- $\xi_1$ is the initial runtime metadata,
- $s_1 = (\omega, h_0, H, \xi_1)$.

The reset operation must clear all per-episode history, caches, memory attachments, and prior tool results unless the experiment explicitly studies cross-episode persistence.

### 6.4 Observation

The agent observes:

$$
o_t = Z(s_t).
$$

For Level A, the observation contains:

```text
q
visible prior tool calls and tool outputs
remaining budget b_t
available tool descriptions
```

The agent does not observe:

```text
Y_star
E_star
unread file contents
unsearched path matches
hidden metadata m
```

For Level B, the observation can be represented as a message transcript:

Let $messages_t$ be the full transcript rendered from the interaction so far (system messages, the user question, prior assistant messages, prior tool results, and any budget/context annotations).

The key is that the observation is generated by a deterministic renderer from `h_{t-1}` and runtime configuration.

### 6.5 History

The full interaction history through step `t` is:

$$
h_t = (o_1, a_1, r_1, o_2, a_2, r_2, \dots, o_t, a_t, r_t, o_{t+1}).
$$

A policy in a POMDP is generally history-dependent:

$$
\pi(a_t \mid h_{t-1}, o_t).
$$

For a language model, the practical conditioning object is the rendered prompt or message transcript derived from that history.

---

## 7. Action Space

### 7.1 Structured Action

An action is a pair:

$$
a_t = (u_t, x_t).
$$

where `u_t` is an action type and `x_t` is a structured argument object.

For the Level A read-only benchmark:

$$
U = \{\texttt{glob}, \texttt{grep}, \texttt{read\_file}, \texttt{answer}, \texttt{stop\_fail}\}.
$$

### 7.2 `glob` Action

Purpose: find candidate paths.

Argument schema:

```text
x = {
  pattern: string,
  root: optional relative path under src/
}
```

Required semantics:

1. `pattern` must be nonempty;
2. `root`, if present, must normalize inside `src/`;
3. the result is a sorted list of matching relative paths;
4. the result is truncated according to a fixed policy if necessary.

### 7.3 `grep` Action

Purpose: find candidate content locations.

Argument schema:

```text
x = {
  query: string,
  root: optional relative path under src/,
  mode: one of {literal, regex},
  max_matches: optional integer
}
```

Required semantics:

1. `query` must be nonempty;
2. `root` must normalize inside `src/`;
3. regex mode must have a fixed regex engine and error policy;
4. literal mode must specify case sensitivity;
5. output must include path and line range for each match;
6. result ordering must be deterministic;
7. truncation must be deterministic.

### 7.4 `read_file` Action

Purpose: reveal file contents or a line slice.

Argument schema:

```text
x = {
  path: relative path under src/,
  line_start: optional positive integer,
  line_end: optional positive integer
}
```

Required semantics:

1. `path` must exist;
2. `path` must refer to a regular text file;
3. if a line interval is supplied, it must satisfy `1 <= line_start <= line_end <= n_lines(path)`;
4. if no interval is supplied, the return may be the full file or a fixed default slice, but that policy must be specified;
5. output must include path, line interval, and text.

### 7.5 `answer` Action

Purpose: terminate with a proposed answer.

Argument schema:

```text
x = {
  answer_text: string,
  cited_evidence: optional list of (path, line_start, line_end)
}
```

The benchmark may require evidence citations. If evidence is required, the action is admissible only if cited evidence refers to previously observed content. If evidence is optional, correctness is judged only by `answer_text`, but separate evidence-use metrics may still be reported.

### 7.6 `stop_fail` Action

Purpose: terminate without claiming an answer.

Argument schema:

```text
x = {}
```

This action ends the episode with a failure reward or abstention reward. It is useful because it separates honest failure from hallucinated incorrect answers.

### 7.7 Full Runtime Action Space

If applying the rigor to the actual `src/tools.ts` registry, the action-type set becomes:

```text
U_full = enabled tools from the registry plus normal assistant response
```

Then each tool has its own schema, permission conditions, read-only/destructive classification, and execution semantics. This is too broad for the first benchmark, but the same formal structure applies.

---

## 8. Admissibility Relation

### 8.1 Definition

For each state `s_t`, define the admissible set:

$$
A_{\text{adm}}(s_t) \subseteq A.
$$

An action outside `A_adm(s_t)` is invalid.

Admissibility is not the same as usefulness. An action can be valid but useless.

### 8.2 Global Admissibility Conditions

An action is globally admissible only if:

1. its action type is enabled;
2. its argument object satisfies the schema for that action type;
3. all paths normalize inside `src/`;
4. no argument violates length, encoding, or formatting constraints;
5. the episode is not already terminal;
6. the remaining budget is positive.

### 8.3 `glob` Admissibility

`glob(pattern, root)` is admissible if:

1. `pattern` is a string;
2. `pattern` length is between fixed bounds;
3. `root` is absent or is an existing directory under `src/`;
4. the glob syntax is valid under the fixed glob semantics.

A glob action may return no matches; no matches does not make the action invalid.

### 8.4 `grep` Admissibility

`grep(query, root, mode, max_matches)` is admissible if:

1. `query` is nonempty;
2. `query` length is below the maximum;
3. `root` is absent or exists under `src/`;
4. `mode` is valid;
5. regex mode compiles successfully if regex is allowed;
6. `max_matches`, if supplied, is in the allowed range.

A grep action may return no matches; no matches does not make the action invalid.

### 8.5 `read_file` Admissibility

`read_file(path, line_start, line_end)` is admissible if:

1. `path` exists under `src/`;
2. `path` is a regular text file;
3. line indices, if provided, are within bounds;
4. file size is below the allowed maximum, or truncation semantics are defined;
5. the requested path is not excluded by benchmark policy.

### 8.6 `answer` Admissibility

`answer(answer_text, cited_evidence)` is admissible if:

1. `answer_text` is nonempty;
2. its length is within bounds;
3. if citations are required, every cited span was previously observed;
4. no cited span is outside `src/`.

### 8.7 `stop_fail` Admissibility

`stop_fail` is admissible whenever the episode is nonterminal.

### 8.8 Runtime Admissibility for Claude-Code-Like Loop

For Level B or C, admissibility must also include:

1. the tool is present in the effective enabled tool set;
2. feature flags permit the tool;
3. permission checks allow the tool call;
4. the tool is not disallowed by mode, plan state, or policy;
5. the call respects max turns, token budget, tool-result budget, and task budget.

This is one of the main ways the applied rigor differs from the generic repo-QA spec.

---

## 9. Tool Semantics

### 9.1 Deterministic Tool Operator

For each nonterminal tool `u`, define a deterministic operator:

$$
T_u(R_{\text{src}}, x) = y.
$$

where `x` is an admissible argument and `y` is the observation returned by the tool.

If the implementation uses a real Ubuntu command, the formal semantics must still be specified independently. The tool result must not depend on uncontrolled shell configuration, locale, filesystem ordering, environment variables, or time.

### 9.2 `glob` Semantics

Let `P` be the sorted set of normalized paths under `src/`. Then:

$$
T_{\texttt{glob}}(R_{\text{src}}, x) = \mathrm{sort}\{\,p \in P : p \text{ matches } x.\texttt{pattern} \text{ under } x.\texttt{root}\,\}.
$$

The output is:

```text
{
  status: success,
  matches: [path_1, ..., path_k],
  truncated: boolean,
  total_matches: integer
}
```

If no matches are found:

```text
matches = []
truncated = false
total_matches = 0
```

### 9.3 `grep` Semantics

Let `F(root)` be the deterministic ordered list of text files under `root`. For each file, scan lines in increasing line order.

For literal search:

```text
match(line, query) = query is substring of line
```

For regex search:

```text
match(line, query) = regex query matches line under fixed regex engine
```

The output is:

```text
{
  status: success,
  matches: [
    {path, line_number, line_text, optional_context}
  ],
  truncated: boolean,
  total_matches: integer
}
```

Ordering is lexicographic by path, then increasing line number, unless a different fixed ranking is explicitly specified.

### 9.4 `read_file` Semantics

For path `p`, let file lines be:

$$
L_p = [\ell_1, \dots, \ell_n].
$$

If no line interval is requested, the benchmark must define whether the result is the entire file or a fixed slice. For large files, the recommended policy is:

```text
return at most B_read bytes or L_read lines, whichever comes first
```

The output is:

```text
{
  status: success,
  path: p,
  line_start: a,
  line_end: b,
  text: lines a through b,
  truncated: boolean
}
```

### 9.5 Error Semantics

Invalid actions should be caught by admissibility before execution. If the implementation still reaches a tool with invalid input, the result is:

```text
{
  status: error,
  error_type: schema_error | path_error | permission_error | range_error | regex_error | budget_error | internal_error,
  message: fixed diagnostic string class
}
```

The reward must handle errors consistently.

### 9.6 Truncation Semantics

Every tool output must obey fixed output limits:

$$
B_{\texttt{glob}} = \text{max returned paths},\quad
B_{\texttt{grep}} = \text{max returned matches or bytes},\quad
B_{\texttt{read}} = \text{max returned lines or bytes}.
$$

Truncation must be included in the observation. If the result is truncated, the agent must know that the returned result is incomplete.

This matters because truncation changes the observation function.

---

## 10. Transition Law

### 10.1 Nonterminal Valid Tool Action

If `a_t = (u_t, x_t)` is valid and `u_t` is one of `glob`, `grep`, or `read_file`, then:

$$
\begin{aligned}
y_t &= T_{u_t}(R_{\text{src}}, x_t), \\
h_t &= \mathrm{append}\!\big(h_{t-1}, (a_t, y_t)\big), \\
b_{t+1} &= b_t - 1, \\
s_{t+1} &= (\omega, h_t, b_{t+1}, \xi_{t+1}).
\end{aligned}
$$

The runtime metadata `xi_{t+1}` is updated to record:

```text
used action
returned paths
read spans
search queries
truncation flags
invalid/error flags if any
```

### 10.2 Invalid Action

If `a_t` is invalid, the environment returns an error observation and applies an invalid-action penalty. There are two valid designs:

Design A: invalid action consumes a step.

$$
b_{t+1} = b_t - 1.
$$

Design B: invalid action terminates immediately.

```text
episode terminates
```

The benchmark must choose one. For tool-use learning, Design A is often better because it allows recovery and makes invalid-argument behavior measurable.

### 10.3 Terminal Answer Action

If `a_t = answer(x_t)`, the episode terminates. The answer checker determines correctness.

No further tool calls are permitted.

### 10.4 Terminal Stop-Fail Action

If `a_t = stop_fail`, the episode terminates with abstention/failure reward.

### 10.5 Horizon Termination

If `b_t = 0` before a terminal answer, the episode terminates with horizon-exhaustion reward.

Termination is guaranteed because `b_t` decreases for each nonterminal step and `H` is finite.

---

## 11. Answer Correctness

### 11.1 Correctness Relation

Define an answer checker:

$$
M(\texttt{answer\_text}, Y^{\star}) \in \{0, 1\}.
$$

`M = 1` means the answer is correct.

The checker must be fixed before evaluation.

### 11.2 Acceptable Checker Types

Exact normalized match:

```text
normalize(answer_text) in normalize(Y_star)
```

This is clean but may be too strict.

Set-valued answer check:

```text
extracted set from answer_text equals required set
```

Good for questions asking for filenames, tool names, function names, or paths.

Evidence-grounded check:

```text
answer is correct and cited_evidence intersects E_star
```

Good for source-code QA.

Human adjudication:

```text
independent graders apply a written rubric
```

This is flexible but requires inter-rater agreement.

For rigorous source-code QA, the recommended default is:

```text
structured answer extraction + evidence-grounded check
```

### 11.3 Evidence Correctness

Define:

$$
C_{\text{evidence}}(\texttt{cited\_evidence}, E^{\star}) \in \{0, 1\}.
$$

This equals 1 if the cited evidence contains at least one sufficient supporting span or all required supporting spans, depending on task type.

Two variants:

Weak evidence criterion:

```text
at least one cited span overlaps E_star
```

Strong evidence criterion:

```text
every required evidence role is covered by at least one cited span
```

The benchmark should report both answer correctness and evidence correctness separately.

---

## 12. Reward Function

### 12.1 Reward Checks in Order

The reward function must check conditions in a fixed order.

For each step:

1. check whether the episode is already terminal;
2. check whether the action is admissible;
3. if invalid, assign invalid-action reward and produce error observation;
4. if action is `answer`, check answer correctness;
5. if action is `stop_fail`, assign abstention/failure reward;
6. if action is a valid tool call, assign tool-use cost;
7. optionally add potential-based shaping;
8. if horizon is reached, assign horizon-exhaustion handling.

Terminal correctness must dominate shaping.

### 12.2 Base Reward

Let:

$$
R_{\text{correct}} > 0,\;
R_{\text{wrong}} > 0,\;
R_{\text{fail}} > 0,\;
R_{\text{invalid}} > 0,\;
c_{\text{glob}} \ge 0,\;
c_{\text{grep}} \ge 0,\;
c_{\text{read}} \ge 0,\;
R_{\text{horizon}} \ge 0.
$$

For invalid actions:

$$
r_t^{\text{base}} = -R_{\text{invalid}}.
$$

For correct answer:

$$
r_t^{\text{base}} = +R_{\text{correct}}.
$$

For incorrect answer:

$$
r_t^{\text{base}} = -R_{\text{wrong}}.
$$

For stop-fail:

$$
r_t^{\text{base}} = -R_{\text{fail}}.
$$

For valid tool calls:

$$
r_t^{\text{base}} = -c(u_t).
$$

For horizon exhaustion without answer:

$$
\text{terminal reward includes } -R_{\text{horizon}}.
$$

### 12.3 Recommended Magnitudes

A clean relative scale is:

$$
\begin{aligned}
R_{\text{correct}} &= 1.0 \\
R_{\text{wrong}} &= 1.0 \\
R_{\text{fail}} &= 0.5 \\
R_{\text{invalid}} &= 0.2 \\
c_{\text{glob}} &= 0.01 \\
c_{\text{grep}} &= 0.02 \\
c_{\text{read}} &= 0.03 \\
R_{\text{horizon}} &= 0.5
\end{aligned}
$$

These are not universal. The important constraint is:

```text
R_correct and R_wrong dominate accumulated shaping and tool costs.
```

For horizon `H`, require:

$$
\sum_{t=1}^{H} \max\{\text{possible shaping bonus at step } t\} < R_{\text{correct}}
$$

if the goal is to prevent reward farming.

### 12.4 Potential-Based Shaping

If dense progress reward is used, define a potential:

$$
\Phi : S \to \mathbb{R}.
$$

and shaping term:

$$
F(s_t, s_{t+1}) = \gamma\,\Phi(s_{t+1}) - \Phi(s_t).
$$

Then:

$$
r_t = r_t^{\text{base}} + F(s_t, s_{t+1}).
$$

Potential-based shaping is preferred because it preserves optimal policies under standard assumptions.

### 12.5 Applied Potential for Repo-QA

A possible potential is:

$$
\Phi(s_t) =
\alpha_1 \, I(\texttt{candidate\_path\_seen})
\;+\; \alpha_2 \, I(\texttt{evidence\_file\_seen})
\;+\; \alpha_3 \, I(\texttt{answer\_span\_seen}).
$$

where:

- `candidate_path_seen` means some path related to `E_star` has appeared in observations;
- `evidence_file_seen` means a file containing required evidence has been found;
- `answer_span_seen` means the actual answer-bearing span has been read.

This potential uses hidden evaluation metadata and is therefore available only to the environment, not to the agent. That is acceptable for reward calculation, but it must be disclosed.

If using hidden metadata for shaping feels too strong, use terminal-only reward and report sample efficiency separately.

### 12.6 Reward Validity Claim

The reward is valid only relative to the stated task. If arbitrary bonuses are added for human-looking reasoning, long explanations, or tool-call style, then the policy may optimize a proxy rather than correct repository QA.

---

## 13. Learner Information State

### 13.1 Non-Tabular History

This project explicitly does not use tabular state.

The learner receives a history-derived input:

$$
I_t = \mathrm{render}(o_1, a_1, y_1, \dots, o_t).
$$

For an LLM, `I_t` is a prompt or message list. For a neural policy that is not an LLM, `I_t` may be tokenized text plus structured features.

### 13.2 Representation

The learner may form:

$$
z_t = f_\phi(I_t).
$$

where `z_t` is a learned representation.

The rigorous assumption must be stated:

Option 1:

```text
z_t is treated as an approximate information state with no exact sufficiency guarantee.
```

Option 2:

```text
z_t is claimed to be sufficient for control, requiring a proof or strong modeling assumption.
```

For a natural-language tool agent, Option 1 is the honest default.

### 13.3 Consequence of Non-Tabular State

Because the state is non-tabular:

1. exact dynamic programming over states is not available;
2. exact tabular Q-learning is not available;
3. learned value functions or policies require function approximation;
4. convergence guarantees are weaker;
5. evaluation becomes empirical rather than purely deductive.

The rigorous claim shifts from exact optimality to well-specified optimization and statistically valid evaluation.

---

## 14. Policy Class

### 14.1 Factorized Tool Policy

The policy should be factorized:

$$
\pi_\theta(a_t \mid I_t) = \pi_\theta(u_t \mid I_t)\,\pi_\theta(x_t \mid I_t, u_t).
$$

where:

- `u_t` is the action type;
- `x_t` is the structured argument.

This matches tool use better than treating every complete tool call as an atomic class.

### 14.2 Action-Type Policy

The action-type policy chooses among:

```text
glob
grep
read_file
answer
stop_fail
```

A failure at this level means the agent chose the wrong kind of operation. Examples:

- answers before gathering evidence;
- reads before identifying any candidate file;
- searches again after the answer span has already been read;
- stops despite enough evidence.

### 14.3 Argument Policy

The argument policy chooses:

- glob patterns;
- grep strings or regexes;
- file paths;
- line ranges;
- answer text;
- evidence citations.

A failure at this level means the tool type was reasonable but the argument was wrong.

### 14.4 Grammar-Constrained Output

The policy output must be parseable into the action grammar.

For LLM policies, there are two designs:

Design A: structured tool-call output.

```text
The model emits a JSON-like call conforming to schema.
```

Design B: text output parsed by a deterministic parser.

```text
The parser maps text into an action or invalid-action error.
```

Design A is preferred. Design B requires stronger parser conformance tests.

### 14.5 Action Masking

At training and evaluation time, the environment may provide an admissibility mask over action types, but not over hidden correct arguments.

Allowed masking:

```text
mask disabled tools
mask answer after terminal
mask read_file when path argument is syntactically invalid
```

Disallowed leakage:

```text
mask only the correct tool
mask only evidence-containing paths
mask based on E_star unless evaluating an oracle
```

Action masking must equal the admissibility relation. If the mask is stricter or looser than admissibility, the training problem is different from the stated environment.

---

## 15. Value Objects

### 15.1 History-Based Value Function

For a policy `pi`, define:

$$
V^{\pi}(h_t) = \mathbb{E}_{\pi}\!\left[\sum_{k=t}^{T} \gamma^{k-t} r_k \,\middle|\, h_t\right].
$$

This is the expected future return after history `h_t`.

### 15.2 History-Based Action-Value Function

Define:

$$
Q^{\pi}(h_t, a_t) = \mathbb{E}_{\pi}\!\left[\sum_{k=t}^{T} \gamma^{k-t} r_k \,\middle|\, h_t, a_t\right].
$$

This is the expected future return after taking action `a_t` at history `h_t` and following `pi` afterward.

### 15.3 Advantage Function

Define:

$$
A^{\pi}(h_t, a_t) = Q^{\pi}(h_t, a_t) - V^{\pi}(h_t).
$$

The advantage measures whether action `a_t` is better or worse than the policy's average action at that history.

### 15.4 Function Approximation

Approximate value functions may be:

$$
V_{\psi}(I_t),\quad Q_{\psi}(I_t, a_t),\quad A_{\psi}(I_t, a_t).
$$

The approximation error is not zero in general. Any theoretical claim involving these objects must be conditional on approximation quality or limited to the optimization objective actually used.

---

## 16. Optimization Objective

### 16.1 Environment Objective

The environment-level objective is:

$$
J(\pi) = \mathbb{E}_{\omega \sim \Omega,\; \tau \sim \pi}\!\left[\sum_{t=1}^{T} \gamma^{t-1} r_t\right].
$$

where `T <= H` is the terminal time.

### 16.2 Policy Parameter Objective

For a parameterized policy `pi_theta`:

$$
J(\theta) = J(\pi_{\theta}).
$$

The learning goal is to find parameters with higher expected return.

### 16.3 Actor-Critic Objective

If using actor-critic, the practical training objective contains:

1. policy improvement term;
2. value regression term;
3. entropy regularization term;
4. optional KL or trust-region term.

A generic form is:

$$
L(\theta, \psi) =
L_{\text{policy}}(\theta)
 + \lambda_{V} L_{\text{value}}(\psi)
 - \lambda_{H}\,\mathcal{H}(\pi_{\theta})
 + \lambda_{KL}\,\mathrm{penalty}_{KL}(\theta, \theta_{\text{old}}).
$$

The report must state which objective is optimized. It is not enough to say the agent maximizes return if the actual update optimizes a surrogate.

### 16.4 Tool-Improvement Without RL

If the current project is tool-improvement rather than RL-objective improvement, the optimization may be absent. In that case the policy is fixed and the study is evaluative:

```text
compare policy variants with different tool access, prompts, schemas, or tool descriptions
```

The rigorous environment still matters because it makes the comparison valid.

### 16.5 Intervention Classes

Tool-improvement interventions can be classified as:

1. **Tool availability intervention**: add/remove `glob`, `grep`, or `read_file`.
2. **Tool-description intervention**: change descriptions or schemas shown to the model.
3. **Argument-constraint intervention**: enforce stricter or looser argument grammar.
4. **Observation-format intervention**: change returned result formatting.
5. **Budget intervention**: change horizon or result truncation.
6. **Policy-training intervention**: train or fine-tune the model/policy.

Only the last one is RL. The others are controlled tool-system experiments.

---

## 17. Data Collection Regimes

### 17.1 On-Policy RL

Trajectories are generated by the current policy:

$$
\tau_i \sim \pi_{\theta}^{\text{current}}.
$$

Updates assume data comes from the current or near-current policy. PPO-style methods are in this family.

### 17.2 Off-Policy RL

Trajectories come from a replay buffer generated by older policies or other behavior policies:

$$
\tau_i \sim \beta.
$$

The learning rule must account for distribution mismatch.

### 17.3 Offline RL

A fixed dataset of trajectories is collected once:

$$
D_{\text{traj}} = \{\tau_i\}.
$$

No new exploration is allowed during training. This is safer but can fail if the learned policy chooses actions outside the support of the data.

### 17.4 Imitation or Behavior Cloning

If trajectories from a strong heuristic or human policy are available, the model can be trained to imitate:

$$
\text{maximize } \log \pi_{\theta}(a_t^{\text{expert}} \mid I_t).
$$

This is not RL unless reward optimization is added, but it is a useful baseline.

### 17.5 Recommendation for First Tool-Improvement Study

Start with no RL training:

```text
fixed policy variants + controlled tool access + held-out evaluation
```

Then add imitation or contextual bandit. Then add full RL only after the environment and metrics are stable.

---

## 18. Exploration

### 18.1 Why Exploration Matters

If training with RL, the agent must sometimes try non-greedy tool choices. Otherwise it may never discover that a different search query or read sequence leads to higher terminal reward.

### 18.2 Exploration Mechanisms

Possible mechanisms:

1. stochastic sampling from the policy;
2. temperature adjustment;
3. entropy regularization;
4. epsilon-style random action-type selection;
5. randomized argument perturbation;
6. curriculum over task difficulty.

### 18.3 Safety and Admissibility

Exploration must respect the admissibility relation. In the read-only benchmark, this mainly prevents invalid paths, malformed schemas, and disabled actions. In the full runtime, it also prevents destructive actions, permission violations, and external side effects.

### 18.4 Exploration Metrics

Report:

```text
action-type entropy
unique tools used
invalid-action rate
unique query strings
unique files read
coverage of evidence files
```

These metrics show whether the learner is exploring the tool space or collapsing prematurely.

---

## 19. Credit Assignment

### 19.1 The Problem

The final answer reward may occur several steps after useful search and read actions. The system must assign credit to earlier actions.

### 19.2 Monte Carlo Credit Assignment

For each step `t`, define full return:

$$
G_t = \sum_{k=t}^{T} \gamma^{k-t} r_k.
$$

This is unbiased but high variance.

### 19.3 TD or Actor-Critic Credit Assignment

Use a critic:

$$
\text{TD target} = r_t + \gamma V_{\psi}(I_{t+1}),\qquad
\text{TD error} = r_t + \gamma V_{\psi}(I_{t+1}) - V_{\psi}(I_t).
$$

This reduces variance but introduces bias from value approximation.

### 19.4 Applied Tool-Use Credit

A successful answer after the sequence:

```text
glob -> grep -> read_file -> answer
```

should assign positive credit to the specific earlier actions that led to evidence. A failed answer after redundant searches should assign lower credit or negative credit to wasteful actions.

The benchmark should log enough intermediate information to reconstruct which actions contributed to evidence discovery.

---

## 20. Argument-Generation Semantics

### 20.1 Why This Is Separate

In tool agents, choosing the tool type is not enough. A `grep` action with the wrong pattern can be worse than no action. A `read_file` action with the wrong path is useless even if reading was the right operation.

### 20.2 Argument Validity

For every tool call, record:

```text
schema_valid
path_valid
permission_valid
range_valid
query_valid
```

These should be separate flags, because they correspond to different failure modes.

### 20.3 Argument Usefulness

For every valid tool call, record:

```text
returns_nonempty
returns_candidate_file
returns_evidence_file
returns_answer_span
reduces_candidate_set
```

Usefulness is not the same as correctness. A query can be valid and nonempty but still irrelevant.

### 20.4 Argument Granularity

Arguments may be evaluated at different levels:

1. exact path match;
2. directory-level match;
3. symbol-level match;
4. evidence-file match;
5. answer-span match.

This enables a richer failure taxonomy.

---

## 21. Verification Layer

Testing verifies that the implementation matches the specification. It is not policy evaluation.

### 21.1 Filesystem Verification

Tests must check:

1. snapshot digest is fixed;
2. all benchmark paths normalize inside `src/`;
3. symlink behavior matches the policy;
4. binary files are handled according to spec;
5. text decoding is deterministic;
6. line numbering is consistent.

### 21.2 Tool Semantics Verification

For `glob`, test:

1. known matching pattern returns exact sorted paths;
2. no-match pattern returns empty list;
3. root restriction works;
4. truncation flags work.

For `grep`, test:

1. literal match correctness;
2. regex match correctness if enabled;
3. invalid regex handling;
4. deterministic ordering;
5. truncation behavior.

For `read_file`, test:

1. full read or default slice policy;
2. line-range read;
3. out-of-bounds range rejection;
4. nonexistent path rejection;
5. large-file truncation.

### 21.3 Parser Verification

If the model emits textual actions, test:

1. valid action strings parse correctly;
2. malformed action strings become invalid actions;
3. missing required fields are detected;
4. extra fields are either rejected or ignored by written policy;
5. parser output is deterministic.

### 21.4 Permission Verification

For Level B/C, test:

1. enabled tools are accepted;
2. disabled tools are rejected;
3. permission denial is represented as a distinct error;
4. denial consumes or does not consume a step according to the spec;
5. denial is counted separately from schema invalidity.

### 21.5 Reset Verification

Each episode must start fresh:

1. empty tool history;
2. empty message transcript except initial prompt/system context;
3. reset read cache unless cache persistence is part of the experiment;
4. reset budgets;
5. no memory injection unless enabled by condition;
6. no leftover task/subagent state.

This is especially important when adapting the rigor to a stateful runtime like `QueryEngine`.

### 21.6 Reward Verification

For fixed synthetic episodes, verify that reward is exactly the stated formula:

1. invalid action penalty;
2. tool cost;
3. correct answer reward;
4. wrong answer penalty;
5. stop-fail penalty;
6. horizon-exhaustion penalty;
7. shaping term if enabled.

### 21.7 Termination Verification

Tests must show:

1. `answer` terminates immediately;
2. `stop_fail` terminates immediately;
3. horizon termination occurs at `H`;
4. no tool call is executed after terminal state;
5. terminal observations are consistent.

---

## 22. Evaluation Estimands

Evaluation estimates policy performance. It is not the same as testing.

Let `Omega_test` be the held-out test distribution.

### 22.1 Expected Return

$$
J_{\text{test}}(\pi) = \mathbb{E}_{\omega \sim \Omega_{\text{test}},\; \tau \sim \pi}\!\big[G(\tau)\big].
$$

where:

$$
G(\tau) = \sum_{t=1}^{T} \gamma^{t-1} r_t.
$$

### 22.2 Success Probability

$$
P_{\text{success}}(\pi) = \Pr\!\big[M(\texttt{answer\_text}, Y^{\star}) = 1\big].
$$

where failure includes wrong answers, stop-fail, and horizon exhaustion.

### 22.3 Evidence Grounding Rate

$$
P_{\text{grounded}}(\pi) = \Pr[\text{answer correct and cited evidence satisfies } C_{\text{evidence}}].
$$

If citations are not required, report evidence-observed rate:

$$
P_{\text{evidence\_seen}}(\pi) = \Pr[\text{trajectory reads at least one required evidence span}].
$$

### 22.4 Tool Efficiency

Expected number of tool calls:

$$
\mathbb{E}[N_{\text{tools}}].
$$

Expected count by type:

$$
\mathbb{E}[N_{\texttt{glob}}],\quad \mathbb{E}[N_{\texttt{grep}}],\quad \mathbb{E}[N_{\texttt{read}}].
$$

### 22.5 Invalid-Action Rate

$$
\mathbb{E}\!\left[\frac{N_{\text{invalid}}}{\max(1, T)}\right].
$$

Also report invalidity categories:

```text
schema_invalid
path_invalid
range_invalid
permission_denied
parser_failed
```

### 22.6 Redundancy Rate

A redundant action is a valid action whose result provides no new information compared to prior observations under a fixed redundancy definition.

Report:

$$
\mathbb{E}[N_{\text{redundant}}].
$$

Examples:

1. same grep query under same root repeated;
2. same file range read twice;
3. glob pattern repeated with same output;
4. read after answer-ready evidence already observed, if no new information is needed.

### 22.7 Premature Answer Rate

$$
\Pr[\text{answer chosen before any evidence-bearing span was observed}].
$$

This is important for distinguishing lucky guesses from grounded reasoning.

### 22.8 Latency and Budget

If runtime matters, report:

```text
wall-clock time per episode
token count per episode
tool-result bytes per episode
budget-exhaustion rate
```

These are secondary unless the project explicitly studies efficiency.

---

## 23. Statistical Protocol

### 23.1 Sample Mean Estimator

For test episodes `omega_1, ..., omega_N`, define:

$$
\hat{J}_N(\pi) = \frac{1}{N}\sum_i G_i.
$$

This estimates `J_test(pi)` under i.i.d. test sampling.

### 23.2 Confidence Intervals

For scalar metrics, report:

```text
mean +/- standard error
```

or nonparametric bootstrap confidence intervals.

For success rates, use binomial or bootstrap intervals.

### 23.3 Paired Evaluation

When comparing two policies, use the same test episodes:

$$
d_i = \mathrm{metric}_i(\pi_A) - \mathrm{metric}_i(\pi_B).
$$

Report mean paired difference and confidence interval. This reduces variance.

### 23.4 Multiple Seeds

If training is stochastic, report across seeds:

```text
seed-level mean
seed-level standard deviation
within-seed test uncertainty
```

Do not report only the best seed.

### 23.5 Model Selection

Use validation set for:

1. prompt selection;
2. reward coefficient selection;
3. horizon selection;
4. truncation limits;
5. hyperparameters;
6. checkpoint selection.

Use test set once for final reporting.

### 23.6 Minimum Reporting

A rigorous report should include:

```text
N_train, N_val, N_test
number of random seeds
confidence intervals
all reward coefficients
horizon H
gamma
tool-output limits
commit hash
split construction method
```

---

## 24. Baselines

### 24.1 Direct Answer Baseline

The policy receives the question but no tools. It must answer directly.

Purpose: measure parametric knowledge or guessing ability.

### 24.2 Fixed Heuristic Pipeline

A deterministic baseline:

```text
grep query terms from question
read top matching file
answer from read content
```

or:

```text
glob likely file names -> grep likely symbols -> read top evidence -> answer
```

Purpose: measure whether a simple non-learning tool strategy is already strong.

### 24.3 ReAct-Style Prompted Tool Policy

The LLM is prompted to reason and choose tools but receives no training.

Purpose: measure inference-time tool-use capability.

### 24.4 Oracle Tool-Type Baseline

The environment supplies the correct next tool type but not the arguments.

Purpose: isolate argument-generation failures.

### 24.5 Oracle Evidence Baseline

The model receives the evidence file or evidence span directly.

Purpose: measure answer-generation ceiling once retrieval is solved.

### 24.6 Behavior Cloning Baseline

Train on expert trajectories:

```text
question -> tool sequence -> answer
```

Purpose: compare RL or tool prompt changes against supervised imitation.

### 24.7 Contextual Bandit Baseline

Only the first tool decision is learned:

```text
choose first action type from question/context
```

Purpose: determine whether full sequential RL is necessary.

---

## 25. Ablation Protocol

Each component should be removable one at a time.

### 25.1 Tool Availability Ablations

Compare:

```text
no tools
glob only
grep only
read only
glob + read
grep + read
glob + grep + read
```

This identifies marginal utility of each tool.

### 25.2 Observation Formatting Ablations

Compare different result formats:

```text
path-only grep results
path + line number
path + line number + line text
path + line number + context lines
```

This tests whether the model benefits from richer observations or gets distracted by them.

### 25.3 Budget Ablations

Vary:

```text
H = 2, 4, 6, 8, 10
B_grep
B_read
```

This tests whether failures are due to policy or insufficient observation budget.

### 25.4 Reward Ablations

For RL variants:

```text
terminal-only reward
terminal + tool cost
terminal + potential shaping
terminal + invalid penalty
terminal + all terms
```

This tests whether improvements come from reward shaping or genuine policy learning.

### 25.5 Representation Ablations

Compare:

```text
full history
last observation only
summarized history
retrieved memory summary
recurrent state
```

This addresses partial observability.

### 25.6 Runtime Ablations

For Level B:

```text
fresh engine per episode vs persistent engine
memory disabled vs memory enabled
compaction disabled vs fixed compaction
permissions deterministic vs interactive simulation
tool result truncation small vs large
```

This tests whether runtime state affects measured tool policy.

---

## 26. Failure Taxonomy Specialized to `claude-code/src`

Every failed episode should be assigned one or more failure labels.

### 26.1 Tool-Type Failure

The agent chose the wrong operation type.

Examples:

1. answered without searching;
2. read a file before locating candidate paths;
3. used glob when content search was needed;
4. kept searching after enough evidence was read.

### 26.2 Argument Failure

The tool type was plausible but the argument was bad.

Examples:

1. grep query omitted the relevant symbol;
2. glob pattern was too broad or too narrow;
3. read path did not exist;
4. read path existed but was unrelated;
5. line range excluded the relevant span.

### 26.3 Evidence Discovery Failure

The agent never observed the necessary evidence.

Subtypes:

```text
candidate file never found
candidate file found but not read
evidence span read but truncated away
evidence span unavailable due to budget
```

### 26.4 Evidence Integration Failure

The agent observed the evidence but produced a wrong answer.

This suggests the retrieval policy was adequate but reasoning or answer synthesis failed.

### 26.5 Schema or Parser Failure

The model produced an action that could not be parsed or did not satisfy schema.

This is a tool-call interface failure.

### 26.6 Permission or Enabled-Tool Failure

The action was rejected because the tool was disabled or permission denied.

This matters for Level B/C when applying the actual tool registry and permission layer.

### 26.7 Redundancy Failure

The agent spent steps on repeated or non-informative actions.

This is often a stopping-policy failure.

### 26.8 Premature Stopping Failure

The agent answered or stopped before gathering sufficient evidence.

### 26.9 Horizon Exhaustion Failure

The agent failed because it reached `H` without terminal answer.

### 26.10 Runtime-State Contamination Failure

For Level B/C, the agent used information from a previous episode, stale memory, stale cache, or non-reset state.

This is an environment-conformance failure, not a policy success.

---

## 27. Applying the Formalism to Actual Claude-Code Runtime

### 27.1 Modification to Hidden State

For the actual runtime, hidden state should be expanded:

$$
s_t = (R_{\text{src}}, q, Y^{\star}, E^{\star}, M_t, C_t, K_t, P_t, B_t, H_t).
$$

where:

- `M_t` is message/conversation state;
- `C_t` is cache and context state;
- `K_t` is effective tool configuration;
- `P_t` is permission state;
- `B_t` is budget/cost state;
- `H_t` is history and task/subagent state.

### 27.2 Modification to Observation

Observation becomes the rendered model context:

```text
system prompt fragments
tool descriptions
user message
prior assistant messages
prior tool results
context attachments
memory attachments if enabled
budget warnings or compaction summaries
```

This means observation design is no longer trivial. The context builder is part of the observation function.

### 27.3 Modification to Action Space

The action space becomes:

```text
normal assistant response
or tool_use block for any enabled tool
```

Each tool action must satisfy the tool's declared schema and permission logic.

### 27.4 Modification to Transition

The transition includes:

1. model response sampling;
2. parsing tool-use blocks;
3. permission checks;
4. tool execution;
5. result storage and truncation;
6. message appending;
7. possible compaction;
8. budget updates;
9. terminal conditions.

### 27.5 Modification to Reward

Additional penalties or metrics may include:

```text
permission-denied penalty
budget-overrun penalty
context-overflow penalty
tool-result-truncation penalty
unapproved side-effect penalty
memory-contamination penalty
```

For a read-only benchmark, these should be mostly disabled or reduced to conformance errors.

### 27.6 Modification to Verification

The conformance test suite must verify:

1. effective enabled tool set equals experimental condition;
2. write/edit/bash/web tools are disabled when read-only is claimed;
3. memory injection is disabled or controlled;
4. compaction is disabled or deterministic;
5. per-episode reset clears state;
6. permission outcomes are deterministic;
7. tool result storage preserves specified observations.

---

## 28. Theorems and Proof Obligations

### 28.1 Proposition: Well-Defined Induced POMDP

Claim:

Given a frozen repository snapshot `R_src`, finite horizon `H`, fixed task distribution `Omega`, fixed action grammar, fixed tool semantics, fixed admissibility relation, fixed reward function, and fixed observation renderer, the read-only repo-QA benchmark is a well-defined finite-horizon POMDP.

Proof sketch:

1. `S`, `A`, and `O` are defined sets.
2. `rho_0` is induced by `Omega` and deterministic reset.
3. For each state-action pair, admissibility and transition behavior are defined.
4. For each transition, an observation is produced by a fixed renderer.
5. Rewards are defined for every transition case.
6. Horizon `H` is finite.
7. Therefore every policy induces a unique distribution over finite trajectories and returns.

### 28.2 Proposition: Termination

Claim:

Every episode terminates in at most `H` nonterminal tool steps plus a terminal condition.

Proof sketch:

1. Initial budget is `H`.
2. Each nonterminal action decreases budget by one.
3. Terminal actions end immediately.
4. When budget reaches zero, horizon termination occurs.
5. Therefore infinite trajectories are impossible.

### 28.3 Proposition: Read-Only Invariance

Claim:

If the enabled tool set is restricted to `glob`, `grep`, and `read_file`, and each tool is implemented as specified, then the repository snapshot remains unchanged throughout the episode.

Proof sketch:

1. Each enabled tool is defined as a pure function of `R_src` and arguments.
2. No transition rule modifies file contents or path structure.
3. Therefore `R_src` is invariant.
4. This can be empirically verified by checking the snapshot digest before and after episodes.

### 28.4 Proposition: Potential-Based Shaping Preserves Optimal Policies

Claim:

If shaping reward has the form:

$$
F(s, s') = \gamma\,\Phi(s') - \Phi(s).
$$

then the set of optimal policies is preserved under standard finite-horizon shaping assumptions, up to terminal potential handling.

Proof sketch:

1. The shaping rewards telescope over a trajectory.
2. The total shaping contribution depends only on initial and terminal potentials, not on intermediate action choices, under fixed terminal handling.
3. Therefore action preferences induced by base returns are preserved.

The exact proof must account for finite-horizon terminal potential convention.

### 28.5 Proposition: Sample Mean Estimates Test Performance

Claim:

If test episodes are sampled i.i.d. from `Omega_test`, then the sample mean return is an unbiased estimator of expected test return.

Proof sketch:

1. Each episode return is an i.i.d. random variable under fixed policy and test distribution.
2. The sample mean expectation equals the population expectation.
3. Confidence intervals follow from standard finite-sample or asymptotic methods depending on assumptions.

---

## 29. Reproducibility Bundle

A complete experiment release should include:

```text
repository URL
commit hash c
snapshot digest D(R_src)
list of enabled tools
tool semantics specification
action grammar
admissibility relation
reward formula and coefficients
horizon H
discount gamma
train/val/test task files
answer checker implementation or rubric
evidence annotations E_star
prompt templates or observation renderer
parser specification
random seeds
model checkpoint identifiers
training logs
trajectory logs
evaluation scripts
conformance tests
statistical analysis scripts
```

For each trajectory log, store:

```text
episode id
task question
action sequence
tool arguments
tool outputs or output hashes
reward sequence
terminal result
failure labels
model/policy version
seed
runtime configuration
```

Without this bundle, the result is hard to audit.

---

## 30. Minimal First Experiment

The smallest rigorous experiment is:

```text
Repository: tanbiralam/claude-code/src at frozen commit c
Tools: glob, grep, read_file
Actions: glob, grep, read_file, answer, stop_fail
Horizon: H = 6 or H = 8
Reward: terminal correctness + small tool cost + invalid penalty
Memory: disabled
Write/edit/bash/web: disabled
Compaction: disabled or deterministic
Reset: fresh per episode
Evaluation: held-out source-code QA tasks
Baselines: direct answer, fixed heuristic, tool-enabled prompted policy
Metrics: success, grounded success, tool calls, invalid rate, premature answer rate
```

This experiment directly studies whether structured read/search tools improve repository understanding on the `src/` tree.

---

## 31. What Must Be Known Before Implementation

Before writing any code, the researcher must be able to answer the following precisely:

1. What exact commit hash defines the repository snapshot?
2. Which paths are in scope?
3. Which tools are enabled?
4. What is the action grammar?
5. What makes an action admissible?
6. What happens when an action is invalid?
7. How are tool outputs ordered and truncated?
8. What is the horizon?
9. What is the reward formula?
10. What counts as a correct answer?
11. What counts as sufficient evidence?
12. What is reset between episodes?
13. What is hidden from the agent?
14. What does the agent observe?
15. What policy variants are compared?
16. What dataset split protects the test set?
17. What metrics define improvement?
18. What conformance tests prove the environment matches the spec?
19. What statistical procedure supports comparison claims?
20. What failure taxonomy explains errors?

Only after these are fixed should training or evaluation begin.

---

## 32. Summary

Applying the rigorous read-only repo-QA specification to `tanbiralam/claude-code/src` does not merely substitute one repository name into a generic POMDP. It changes the specification by introducing an actual agentic runtime with a query loop, tool registry, tool interface, permissions, budgets, context construction, memory-related machinery, and many side-effectful tools.

The correct response is to define an induced read-only sub-environment first:

```text
GlobTool + GrepTool + FileReadTool + answer
```

This sub-environment is clean enough for theorem-style well-posedness, termination, read-only invariance, tool semantic conformance, and statistically valid evaluation.

The full runtime can be modeled later by expanding the hidden state, action space, transition law, reward, and verification layer. That expansion should be done deliberately, one component at a time.

The most important conceptual boundary remains:

```text
Tool implementation = environment mechanics.
Tool choice, argument choice, continuation, and stopping = policy.
```

That is the exact place where tool analysis, supervised improvement, or RL can be applied.
