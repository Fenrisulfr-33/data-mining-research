\documentclass[10pt,conference]{IEEEtran}

%\AtBeginEnvironment{tabular}{\fontsize{32}{36}\selectfont}
\IEEEoverridecommandlockouts

\AtBeginDocument{%
  \providecommand\BibTeX{{%
    \normalfont B\kern-0.5em{\scshape i\kern-0.25em b}\kern-0.8em\TeX}}}
    
\newcommand{\boldification}[1]{\ifdraft\indent ** \textbf{#1}** \\ \indent\else\relax\fi}
\newif\ifdraft
\drafttrue
\usepackage[numbers,sort&compress,square]{natbib}
\usepackage{soul}
\usepackage{graphicx}
\usepackage{xurl}
\usepackage{booktabs}
\usepackage{multibib}
\usepackage{natbib}
\usepackage{hhline}
\usepackage{xcolor}
\usepackage[compatibility=false]{caption}
\usepackage{graphicx}
\usepackage{colortbl}
\usepackage{multirow}
\usepackage{tabularx}
\usepackage{amsmath}
\usepackage{makecell}
\usepackage{textgreek}
\usepackage{tabularx}
\usepackage{siunitx}
\usepackage{stfloats, caption}%
\usepackage{tablefootnote}
\newcolumntype{Y}{>{\centering\arraybackslash}X}
\usepackage{bookmark}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{microtype}
\usepackage{booktabs}
\usepackage{etoolbox}
\usepackage{enumitem} 
\usepackage{url}
\usepackage{ragged2e}
\usepackage{amsmath}


\author{\IEEEauthorblockN{Template}}

\newcolumntype{P}[1]{***{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}

\newcolumntype{C}[1]{***{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}

\newcommand{\MyBox}[1]{\vspace{3mm}\noindent\framebox[\columnwidth][c]{\parbox[b]{0.95\columnwidth}{ #1 }}\vspace{3mm}}


\begin{document}

\title{Title\\
}

\author{\IEEEauthorblockN{Anonymous}}

%\author{\IEEEauthorblockN{1\textsuperscript{st} Given Name Surname}
%\IEEEauthorblockA{\textit{dept. name of organization (of Aff.)} \\
%\textit{name of organization (of Aff.)}\\
%City, Country \\
%email address or ORCID}

%\and

%\IEEEauthorblockN{2\textsuperscript{nd} Given Name Surname}
%\IEEEauthorblockA{\textit{dept. name of organization (of Aff.)} \\
%\textit{name of organization (of Aff.)}\\
%City, Country \\
%email address or ORCID}

%\and

%\IEEEauthorblockN{3\textsuperscript{rd} Given Name Surname}
%\IEEEauthorblockA{\textit{dept. name of organization (of Aff.)} \\
%\textit{name of organization (of Aff.)}\\
%City, Country \\
%email address or ORCID}

%\and

%\IEEEauthorblockN{4\textsuperscript{th} Given Name Surname}
%\IEEEauthorblockA{\textit{dept. name of organization (of Aff.)} \\
%\textit{name of organization (of Aff.)}\\
%City, Country \\
%email address or ORCID}

%}

\maketitle




% =========================================================
% THIS IS A TEMPLATE TO REPORT A MSR STUDY - READ THE SECTIONS CAREFULLY AND USE THE PARTS THAT ARE APPROPRIATE TO YOUR DESIGN
% =========================================================
\section{Research Design}
\label{sec:research-design}

% This section explains exactly how you conducted the study.
%
% A reader should be able to understand:
% 1. What you studied;
% 2. What data you collected;
% 3. Which observations entered the final dataset;
% 4. How you defined the concepts in the RQ;
% 5. How you analyzed the data; and
% 6. How you checked that your derived data/classifications were correct.
% 7. How another researcher could reproduce the dataset and analysis.


% =========================================================
\subsection{Research Question}
\label{sec:rqs}

%Introduce (concisely) the research problem and why it is important to investigate it. The problem needs to be connected to the RQ that follows.
We investigate the following research question:

\noindent\textbf{RQ:} \textit{For which software engineering activities do Zephyr contributors explicitly use GenAI?}

% After the RQ, add a short paragraph answering:
% - What is currently unknown?
% - Why is this worth investigating?
%
% Do NOT explain your results here.
% Do NOT explain statistical tests here.


% =========================================================
\subsection{Study Context and Data}
\label{sec:data}

\subsubsection{The Zephyr Project}
\label{sec:zephyr}

The Zephyr Project is an open-source real-time operating system (RTOS)
developed publicly on GitHub. Its main repository,
\texttt{zephyrproject-rtos/zephyr}, contains the source code and the
development history of the project, including commits, issues, pull
requests (PRs), code reviews, and contributor activity.

Zephyr is suitable for investigating GenAI usage in software engineering activities for a few reasons. Due to the popularity and longevity of the Zephyr project, the Github has a large quantity of PRs, Issues, Discussions and Comments spanning over multiple years. The data is comprised of a large number of unique contributors improving the validity of the research.

% Make this sentence specific to your project.
%
% Examples:
%
% Review project:
% Zephyr has public PR review conversations and revision histories.
%
% Newcomer project:
% Zephyr has a long PR history that allows contributors to be followed
% from their first contribution onward.
%
% Issue project:
% Issues contain timestamps, labels, comments, closure events, and links
% to development work.
%
% GenAI project:
% Public PRs, issues, reviews, and discussions contain observable
% mentions of GenAI use.
%
% Documentation project:
% Review and issue conversations show when documentation is requested,
% referenced, criticized, or used to resolve a problem.


\subsubsection{Data Sources and Observation Period}
\label{sec:data-sources}

To answer our research question, we analyzed PRs, PR Comments, PR Discussions, Initial Commit Messages, and labels between \emph{October 3rd, 2022} and \emph{October 3rd, 2026}.

We use these artifacts because each artifact covers a different aspect of potential GenAI usage and maximizes our chance to detect GenAI usage. PR labels are static, consistent and specific tags applied to each PR. Each label categorizes what the PR is accomplishing and what section of the codebase the PR is changing. The PR descriptions further add to the context of each PR with more detailed explanations of the changes and may state GenAI usage. Comments and discussions cover contributor discourse within each PR. This allows us to see other contributor's opinions on the PR and any discussions about the GenAI usage. The initial commit message increases our GenAI detection due to the Zephyr contributor rules. Recently, Zephyr requires each initial commit message to state if AI was used for the PR and the specific tool used.


%comments and discussions cover contributor discourse over GenAI usecases. Labels allow us to understand what the PR's goal is and specific sections the PR is changing. Commit messages contain additional information not mentioned in the PR description. Recently, the Zephyr contributor guidelines now require initial commit messages to contain a tag stating if AI assisted the contributor. This increases our chances of detecting GenAI usage. %

%EXPLAIN WHY THESE DATA PROVIDE THE EVIDENCE NEEDED FOR THE RQ

We collected the data on October 3rd, 2026 using the Github REST API. 

For each PR, we collect these fields: PR number, author, description, comments, discussions, initial commit message, and labels. 
 
% Examples of fields:
% timestamps, author, labels, state, comments, reviews, commits,
% changed files, additions/deletions, reviewers, closure events.
%
% If you combine different artifact types, explain how they are connected.
%
% Example:
% ``We associated review comments with their PR using the GitHub PR ID
% and linked contributor activity using GitHub user IDs.''
%
% If links are sometimes missing or ambiguous, explain what you did.


%ATTENTION READ!
% USE OF LLMs IN THE RESEARCH METHOD:
%
% If an LLM is used to collect, detect, classify, code, extract, or
% analyze research data, describe that use in the subsection where the
% corresponding research procedure is explained.
%
% clearly report:
% - model and version;
% - what input was given to the model;
% - what task the model performed;
% - the prompt or decision criteria;
% - relevant model settings, when controlled;
% - how the output was validated by humans;
% - how uncertain/disagreeing cases were handled.
%
% Using an LLM does not by itself weaken the study.
% The methodological risk comes from using it without clearly defining,
% validating, and reporting the research task it performs.
% If an LLM applies a qualitative codebook, first establish the codebook
% and human reference labels independently. Report LLM validation
% separately from human inter-rater reliability.
% Include the complete prompt(s) and LLM-produced research outputs needed
% for reproducibility in the replication package.
%
% =========================================================
\subsection{Dataset Construction}
\label{sec:dataset}

% This subsection explains how the collected data became the dataset
% that you actually analyzed.


\paragraph{Study Population and Unit of Analysis.}

Our initial study population consists of
\emph{[PRECISELY STATE WHICH OBSERVATIONS WERE INITIALLY CONSIDERED]}.

The unit of analysis is
\emph{[PR / ISSUE / REVIEW THREAD / CONTRIBUTOR / CONTRIBUTION /
PR--REVIEWER PAIR / OTHER]}.

% Example:
% ``Our initial population consists of all Zephyr PRs opened between
% January 1, 2021 and December 31, 2025. The unit of analysis is a PR.''
%
% For qualitative conversation studies, the unit may be a complete
% conversation/review thread rather than a single comment.


\paragraph{Filtering and Final Dataset.}

Starting from the initial population, we
\emph{[EXPLAIN WHICH OBSERVATIONS YOU REMOVED OR RETAINED AND WHY]}.

% Report only important filtering decisions.
%
% Examples:
% - remove bot-generated activity;
% - remove false-positive GenAI/documentation candidates;
% - exclude observations missing information required for the analysis;
% - require human review when the RQ concerns review;
% - distinguish relevant issue closure types;
% - other project-specific requirements.
%
% Do NOT simply write ``we cleaned the data.''

% Use the table below when you have several filtering steps.
% If you only have one simple filter, report the numbers in the text
% and delete the table.

Table~\ref{tab:dataset-construction} summarizes the construction of
the analysis dataset.

\begin{table}[htb]
    \caption{Construction of the analysis dataset.}
    \label{tab:dataset-construction}
    \centering
    \small
    \begin{tabularx}{\columnwidth}{@{}Xr@{}}
        \toprule
        \textbf{Dataset construction step} & \textbf{N} \\
        \midrule
        PRs retrieved from the GitHub REST API & 55,212 \\
        After removing duplicate PR rows        & 55,087 \\
        \midrule
        \textbf{Final analysis dataset}         & \textbf{55,087} \\
        \midrule
        \multicolumn{2}{@{}l}{\emph{Of which, PRs with at least one AI signal:}} \\
        \quad Before excluding bot comments     & 5,753 \\
        \quad After excluding bot comments      & 4,282 \\
        \bottomrule
    \end{tabularx}
\end{table}

% If different analyses use different subsets, report that explicitly.
%
% Example:
% ``The final dataset contains 12,430 PRs. The qualitative analysis uses
% a stratified sample of 400 review conversations.''


% =========================================================
\subsection{Definitions and Measures}
\label{sec:measures}

% This is where you explain HOW the concepts in your RQ are represented
% using GitHub data.
%
% Include only the items that your project actually uses.
%
% A good rule:
% If a reader might ask ``How did you decide that?'' or
% ``How exactly did you calculate that?'', explain it here.


\paragraph{Derived Definitions.}

% Use this paragraph when something important is NOT directly available
% as a reliable GitHub field.
%
% Examples:
% - human vs. bot activity;
% - first-time vs. established contributor;
% - maintainer/core contributor;
% - substantive feedback;
% - GenAI-related conversation;
% - documentation-related conversation;
% - subsystem;
% - responsible reviewer;
% - issue closure type;
% - review start.
%
% Delete this paragraph if your study uses no derived definitions.

We define a \emph{labeled AI-assisted PR} as a PR carrying GitHub's
\texttt{AI-assisted} label.

We define a \emph{commit-disclosed AI-assisted PR} as a PR with at least
one commit whose message contains an \texttt{Assisted-by:} trailer,
following Zephyr's own contributor guidelines for disclosing AI
assistance on a commit; we check every commit on the PR, not only the
first.

We define a \emph{GenAI keyword candidate} as a PR whose description,
conversation comments, review discussion, or first commit message
contains at least one term from a predefined list of GenAI-related
keywords and phrases (e.g.\ tool/vendor names such as
\textit{ChatGPT}, \textit{Copilot}, \textit{Claude}, \textit{Gemini},
and generic phrases such as \textit{``ai-generated''} or
\textit{``used ai''}). This is a screening signal, not a confirmed
instance of GenAI use.

% If you use several important definitions, define each one.
%
% Example:
% ``We define a first-time contributor as a contributor whose focal PR
% is their first PR to Zephyr at the time the PR is opened.''
%
% Example:
% ``We define substantive human feedback as a non-bot review comment or
% review event that contains feedback about the contribution.''


\paragraph{Candidate Detection.}

% IMPORTANT:
% Candidate detection is a SCREENING step.
% A keyword/model match is not automatically a confirmed instance of
% the phenomenon unless your method establishes that it is sufficiently
% accurate.

% Use this paragraph ONLY if you first search a larger dataset to find
% possible cases of your phenomenon.
%
% This is needed for projects such as:
% - documentation needs;
% - GenAI perceptions;
% - GenAI use cases;
% - GenAI output evaluation;
% - documentation satisfaction.
%

Candidate cases are confirmed using \emph{manual review}.

We identify candidate PRs by searching the PR description, the PR's
conversation comments, its review discussion (inline review comments
and review summaries), and its commit messages, using a predefined
keyword list covering GenAI tool/vendor names and generic usage
phrases, together with two more precise signals: the GitHub
\texttt{AI-assisted} label and an \texttt{Assisted-by:} commit-message
trailer.

% Explain where the search terms/signals came from.
% If you follow prior research, cite it.

The keyword list was self-compiled for this project rather than drawn
from prior published work; the \texttt{Assisted-by:} trailer format is
defined by Zephyr's own contribution guidelines. Candidate cases
identified by keyword match are treated as unvalidated until confirmed
by manual review.


\paragraph{Historical or Time-Based Measures.}

% NOTE: the mined CSV does not yet store the PR's created_at, and nothing
% computes the first GenAI mention yet. Both must be added to the
% pipeline before these measures can be reported.

To place AI-flagged PRs in time, we reconstruct each PR's timeline
using the timestamps GitHub records for its artifacts: the PR's
\texttt{created\_at}, the \texttt{created\_at} of each conversation
comment and inline review comment, and the \texttt{submitted\_at} of
each review. All timestamps are in UTC.

We define a PR's \emph{creation time} as its \texttt{created\_at}
timestamp. We use it to decide whether a PR falls inside the
observation period and to group PRs by calendar month, so that the
share of AI-flagged PRs can be compared across the period. For
commit-disclosed AI-assisted PRs we also use the PR's creation time
rather than commit dates, because commit dates can be rewritten when a
branch is rebased.

We define a contributor's \emph{first GenAI mention} as the earliest
timestamp at which that contributor authored a PR description, comment,
review comment, or review containing a GenAI keyword, across all PRs in
the observation period. A PR description is timestamped with the PR's
creation time. When a contributor mentions GenAI more than once, only
the earliest mention is counted.

We define the \emph{pre-} and \emph{post-policy} periods relative to
\emph{[DATE]}, when Zephyr's contribution guidelines began requiring an
\texttt{Assisted-by:} trailer on AI-assisted commits. A PR belongs to
the post-policy period if its creation time is on or after that date.


\paragraph{Analysis Variables.}

% Use this paragraph mainly for quantitative projects.
%
% Clearly identify:
% - what you are trying to explain/compare (outcome);
% - the characteristics you examine (predictors);
% - any variables included to account for other explanations (controls).
%
% Do not call every variable a control.

% Decide the principal outcome, explanatory variables, and planned
% controls from the RQ and study design before interpreting the results.
% Do not add variables only because they make a result statistically
% significant.

Our main outcome is \emph{whether a PR is flagged as AI-assisted},
measured as the disjunction of the labeled AI-assisted definition, the
commit-disclosed AI-assisted definition, and the GenAI keyword
candidate definition above.

We examine \emph{what the contributor was working on}, operationalized
as the PR's labels (with the category prefix, e.g.\ \texttt{area:} or
\texttt{platform:}, stripped), to characterize the software engineering
activities associated with flagged PRs.

% Explain why the important variables are relevant to the RQ.
%
% If your project has many variables, use the table below.
% If there are only two or three, prose is enough.

\begin{table*}[t]
    \centering
    \caption{Operationalization of the principal study measures.}
    \label{tab:operationalization}
    \small
    \begin{tabularx}{\textwidth}{@{}p{0.22\textwidth}XX@{}}
        \toprule
        \textbf{Concept / Measure} &
        \textbf{Definition} &
        \textbf{Operationalization / Data Used} \\
        \midrule
        AI-assisted (label) &
        PR carries the GitHub \texttt{AI-assisted} label &
        PR labels, via \texttt{GET /pulls} \\

        GenAI keyword match &
        PR description, comments, discussion, or first commit message
        contains a term from the GenAI keyword list &
        PR description, \texttt{GET /issues/\{pr\}/comments},
        \texttt{GET /pulls/\{pr\}/comments},
        \texttt{GET /pulls/\{pr\}/reviews},
        \texttt{GET /pulls/\{pr\}/commits} \\

        Assisted-by commit trailer &
        Any commit on the PR contains an \texttt{Assisted-by:} trailer &
        \texttt{GET /pulls/\{pr\}/commits}, all commits checked \\

        Tags (what was worked on) &
        PR's labels, category prefix stripped; recorded only when an AI
        signal above is present &
        PR labels, via \texttt{GET /pulls} \\
        \bottomrule
    \end{tabularx}
\end{table*}

% =========================================================
% USE THIS SECTION IF YOU READ ARTIFACTS AND CLASSIFY THEIR CONTENT
\subsection{Qualitative Analysis}
\label{sec:qualitative}

% KEEP THIS SECTION if researchers read PRs, issues, comments,
% conversations, code changes, or other artifacts and assign them to
% categories based on their meaning.
%
% This applies to Projects 1--4, 7--9, and 11.
%
% Examples:
% - types of documentation needs;
% - perceptions or uses of GenAI;
% - responses to GenAI output;
% - reasons for documentation dissatisfaction;
% - types of review feedback;
% - types of rework;
% - reasons that PRs are difficult to review.
%
% DELETE this section if your analysis uses only numerical measures
% extracted or calculated from repository data.


\paragraph{Selection and Coding Procedure.}

% First explain WHAT you qualitatively analyzed.
%
% If you coded all confirmed cases, state that.
%
% If you coded only a sample, report:
% - the population from which the sample came;
% - how the sample was selected (e.g., random, stratified, or selected
%   based on a quantitative result);
% - the sample size;
% - why this sample is appropriate for answering the RQ.
%
% Do not simply say that you selected ``representative'' cases.

We qualitatively analyze
\emph{[ALL CONFIRMED CASES / N ARTIFACTS SELECTED FROM ...]}.

The artifacts were selected using
\emph{[SAMPLING PROCEDURE, IF A SAMPLE IS USED]}.

% Next explain WHERE the categories came from.
%
% Most projects in this course ask you to DEVELOP categories from the
% Zephyr data. In that case, explain the open-coding and codebook
% development process described below.
%
% If your project uses a taxonomy from previous research instead, cite
% that taxonomy and explain whether you:
% - used it as published; or
% - modified/extended it because some Zephyr cases did not fit.
%
% Project 11 is an example in which an existing taxonomy should first be
% investigated.
%
% IMPORTANT:
% If your project description lists possible categories only as examples,
% do not use them automatically as your final taxonomy.

We
\emph{[DEVELOP THE CATEGORIES FROM THE DATA / APPLY AN EXISTING
TAXONOMY / ADAPT AN EXISTING TAXONOMY]}.

% If you DEVELOP categories from the data:
%
% 1. Open coding:
%    Researchers independently examine an initial set of artifacts and
%    assign preliminary codes describing the concepts they observe.
%    At this stage, the researchers do not need to use identical labels.
%
% 2. Draft taxonomy:
%    Researchers compare the preliminary codes, identify recurring
%    concepts, merge similar codes, distinguish different concepts, and
%    organize them into draft categories.
%
% 3. Draft codebook:
%    For each category, define at least:
%    - category name;
%    - definition;
%    - inclusion criteria (when the category applies);
%    - exclusion criteria (similar cases that belong elsewhere);
%    - boundary rules for easily confused categories;
%    - representative examples.
%
%    If one artifact can receive more than one category, state this
%    explicitly and define when multi-label coding is allowed.
%
% 4. Pilot:
%    Researchers independently apply the draft codebook to a NEW small
%    set of artifacts. This pilot is used to find unclear definitions,
%    overlapping categories, missing categories, and ambiguous cases.
%
% 5. Refinement:
%    Researchers may discuss the pilot cases and revise the codebook.
%    Discussion is appropriate here because the goal is to improve the
%    coding instrument.
%
% 6. Freeze:
%    After the pilot and refinement, freeze the codebook before starting
%    the formal inter-rater reliability assessment.

To develop or refine the coding scheme,
\emph{[N]} researchers independently examine an initial set of
\emph{[N]} artifacts and assign preliminary codes describing the
relevant concepts they observe.

The researchers compare the preliminary codes, group recurring concepts
into categories, and create a draft codebook containing
\emph{[CATEGORY DEFINITIONS / INCLUSION AND EXCLUSION CRITERIA /
BOUNDARY RULES / EXAMPLES]}.

They then independently pilot the draft codebook on a new set of
\emph{[N]} artifacts. Based on the pilot, they identify unclear or
overlapping categories and refine the codebook.

After this pilot and refinement process, the codebook is frozen before
the inter-rater reliability assessment.


\paragraph{Inter-Rater Reliability.}

% This paragraph evaluates whether different researchers can apply the
% FROZEN codebook consistently.
%
% IMPORTANT:
% - Do not use the artifacts that were extensively discussed during
%   codebook development as the final IRR sample.
% - The IRR sample should come from the same population as the final
%   qualitative analysis.
% - Do not deliberately select only easy cases.
% - If some categories are rare, consider whether a purely random sample
%   will contain enough variation to evaluate the coding scheme.
%
% Before running IRR, decide:
% - which frozen codebook version is being tested;
% - who the coders are;
% - the unit of analysis;
% - whether coding is single-label or multi-label;
% - the number and percentage of artifacts in the IRR sample;
% - how the IRR sample is selected;
% - which agreement statistic is appropriate.
%
% During the IRR round:
% - coders receive the same codebook;
% - coders receive the same artifact context and instructions;
% - coders classify the same artifacts independently;
% - coders do not see each other's labels;
% - coders do not discuss individual cases.
%
% Calculate IRR on the ORIGINAL INDEPENDENT labels, before any
% adjudication or discussion of disagreement cases.
%
% For two coders assigning one nominal category per artifact,
% Cohen's Kappa is commonly used.
%
% The goal is not simply to obtain a high number. IRR provides evidence
% about whether the coding scheme can be applied reproducibly.
%
% Also inspect WHERE disagreements occur. A single overall agreement
% value may hide systematic confusion between particular categories.

Using the frozen codebook,
\emph{[N]} researchers independently code
\emph{[N]} artifacts
(\emph{[PERCENTAGE]}\% of the qualitative dataset).

The IRR sample was selected using
\emph{[RANDOM / STRATIFIED / OTHER SAMPLING PROCEDURE]}.

The coders use the same unit of analysis, artifact context, coding
instructions, and codebook, and do not discuss individual cases during
the reliability round.

We assess inter-rater reliability using
\emph{[COHEN'S KAPPA / OTHER APPROPRIATE AGREEMENT MEASURE]}
and obtain \emph{[VALUE]}.

% Do not report only the value. When useful, also report:
% - observed/raw agreement;
% - which categories accounted for most disagreements.
%
% Do not treat a single Kappa threshold as an automatic pass/fail rule.
% Interpret the value together with the disagreement patterns and the
% purpose of the coding scheme.


\paragraph{Revising the Codebook After Reliability Testing.}

% KEEP this paragraph only if the IRR round reveals important problems
% that require changes to the codebook.
%
% If IRR is poor or disagreements reveal unclear category boundaries:
% 1. inspect which categories caused disagreement;
% 2. revise definitions, inclusion/exclusion criteria, or boundary rules;
% 3. freeze the revised codebook;
% 4. select a NEW IRR sample;
% 5. code that new sample independently;
% 6. calculate IRR again.
%
% Do not discuss the original disagreement cases, change those labels,
% and then recalculate IRR on the reconciled labels. That is not an
% independent reliability assessment.

Because the initial reliability assessment revealed
\emph{[PROBLEMATIC CATEGORY BOUNDARIES / OTHER ISSUE]},
we revised \emph{[EXPLAIN WHICH PART OF THE CODEBOOK CHANGED]}.

We then independently coded a new set of
\emph{[N]} artifacts using the revised frozen codebook and obtained
\emph{[AGREEMENT MEASURE AND VALUE]}.

% DELETE this paragraph if no substantial codebook revision was needed.


\paragraph{Final Coding and Adjudication.}

% Explain how the FINAL labels used in the analysis were produced.
%
% Examples:
% - both researchers independently coded all artifacts;
% - after satisfactory IRR, one trained researcher coded the remainder;
% - a third researcher independently adjudicated disagreement cases.
%
% IMPORTANT:
% Adjudication is separate from IRR.
% Do not report negotiated consensus as the reliability result.
%
% Preserve the original independent labels separately from the final
% analysis label.

After the reliability assessment,
\emph{[EXPLAIN WHO CODED THE REMAINING ARTIFACTS]}.

For artifacts that received different independent labels,
the final classification was determined by
\emph{[INDEPENDENT THIRD RESEARCHER / OTHER PREDEFINED
ADJUDICATION PROCEDURE]}.

The original independent coder labels were preserved separately from
the final analysis labels.

% If only one researcher codes the remaining artifacts after satisfactory
% IRR, state this clearly.
%
% If the coding scheme changes substantially during final coding, do not
% silently continue. Explain the revision and whether a new reliability
% assessment was performed.


% OPTIONAL:
% Use the table below when the qualitative coding procedure has several
% stages and a compact summary would help the reader understand the method.
%
% The table summarizes the METHOD, not the findings.
%
% Keep the detailed explanation in the text above. The table should make
% it easy to see:
% - how the coding scheme was developed;
% - how it was piloted;
% - how IRR was assessed;
% - how the final coding was completed.
%
% Delete the table if the procedure is simple enough to explain clearly
% in prose.

Table~\ref{tab:qualitative-method} summarizes the qualitative coding
procedure.

\begin{table}[htb]
    \caption{Qualitative coding procedure.}
    \label{tab:qualitative-method}
    \centering
    \small
    \begin{tabularx}{\columnwidth}{@{}p{0.24\columnwidth}X@{}}
        \toprule
        \textbf{Step} & \textbf{Procedure} \\
        \midrule

        Open coding &
        \emph{[N]} researchers independently examined
        \emph{[N]} artifacts and assigned preliminary codes. \\

        Codebook development &
        Preliminary codes were organized into categories with definitions,
        inclusion/exclusion criteria, boundary rules, and examples. \\

        Pilot coding &
        The draft codebook was independently applied to
        \emph{[N]} new artifacts and refined based on unclear or
        overlapping categories. \\

        IRR assessment &
        \emph{[N]} researchers independently coded
        \emph{[N]} artifacts (\emph{[X]}\%) using the frozen codebook.
        Agreement was assessed using \emph{[MEASURE]}, yielding
        \emph{[VALUE]}. \\

        Final coding &
        \emph{[EXPLAIN WHO CODED THE REMAINING ARTIFACTS AND HOW
        DISAGREEMENTS WERE ADJUDICATED]}. \\

        \bottomrule
    \end{tabularx}
\end{table}


\paragraph{Reporting Category Frequencies.}

% KEEP THIS SHORT PARAGRAPH if you report how often the categories occur.
% Most of the qualitative projects in this course should do this.
%
% This paragraph describes HOW frequencies will be calculated; the actual
% category frequencies belong in the Results section.
%
% Report BOTH the number of cases and the percentage in the Results,
% for example:
% ``Testing guidance appeared in 42 of 180 conversations (23.3%).''
%
% Always state the denominator.
%
% Make sure the denominator matches the UNIT OF ANALYSIS. For example,
% do not report percentages of comments if the unit of analysis is a
% review conversation.
%
% If artifacts can have multiple categories, percentages may add to more
% than 100%; say so explicitly.

We calculate the number and percentage of analyzed artifacts assigned to
each category. The denominator is
\emph{[DEFINE THE TOTAL NUMBER OF ARTIFACTS USED TO CALCULATE
THE PERCENTAGES]}.

% If multiple labels are allowed:
% ``Because an artifact may receive more than one category, category
% percentages do not necessarily sum to 100%.''
%=========================================================
% USE THIS SECTION IF YOU ANALYZE NUMERICAL DATA
\subsection{Quantitative Analysis}
\label{sec:quantitative}

% Keep this section if the RQ requires numerical description, comparison,
% association, modeling, longitudinal analysis, or time-to-event analysis.
%
% This applies especially to Projects 5, 6, 8--12.


\paragraph{Descriptive Analysis.}

% Begin by characterizing the data relevant to the RQ.
%
% Report counts and percentages for categorical variables.
% For numerical variables, inspect the distribution before choosing
% summaries. Repository measures are often skewed; median and IQR may be
% more informative than mean and standard deviation.

We summarize \emph{[VARIABLES / OUTCOMES / GROUPS]}
using \emph{[APPROPRIATE DESCRIPTIVE STATISTICS]}.


\paragraph{Group Comparisons.}

% USE when the RQ compares two or more groups.
%
% Examples:
% - first-time vs. established contributors;
% - different contribution stages;
% - issue closure groups.
%
% Choose the test based on the variable type, distribution, and whether
% the observations are independent.
%
% Report the magnitude of the difference using an appropriate effect size
% in addition to statistical significance.

% If you perform several related statistical tests, explain how you
% address multiple comparisons (e.g., Holm correction), when applicable.

To compare \emph{[GROUPS]}, we use
\emph{[TEST]} because \emph{[WHY IT FITS THESE DATA]}.

We report \emph{[EFFECT-SIZE MEASURE]} to quantify the magnitude of
the observed difference.


\paragraph{Association Analysis.}

% USE when the RQ asks whether two variables are related but does not
% require a multivariable explanatory model.
%
% Example:
% whether contributor experience is associated with review delay.
%
% Select Pearson, Spearman, or another measure based on the type and
% distribution of the variables.

To examine the relationship between
\emph{[VARIABLE 1]} and \emph{[VARIABLE 2]},
we use \emph{[CORRELATION/ASSOCIATION METHOD]}.


\paragraph{Statistical Models.}

% USE when the RQ asks which factors or characteristics are associated
% with an outcome.
%
% This is especially relevant to Projects 5, 9, 10, 11, and 12.
%
% Identify:
% - the outcome;
% - the main explanatory variables;
% - other relevant variables included in the model;
% - why the model is appropriate for the outcome.
%
% Examples:
% binary outcome -> logistic model
% count outcome -> count model
% repeated observations -> account for dependence/clustering
% time-to-event outcome -> survival model
%
% Repository observations are not always independent.
% If the same contributor, reviewer, PR, issue, or subsystem contributes
% multiple observations, explain whether and how your analysis accounts
% for this dependence.
% Before interpreting the model, check important problems such as highly
% correlated predictors or violated model assumptions.

To examine which factors are associated with
\emph{[OUTCOME]}, we use \emph{[MODEL]}.

The model includes \emph{[MAIN EXPLANATORY VARIABLES]} and
\emph{[OTHER VARIABLES, IF USED]}.

We assess \emph{[RELEVANT DIAGNOSTICS, e.g., predictor correlation,
multicollinearity, residual/model assumptions, dependence]} before
interpreting the results.

% Report estimates with uncertainty, such as coefficients/odds ratios
% and confidence intervals. Do not report only p-values.


\paragraph{Time-to-Event Analysis.}

% USE only when the RQ concerns how long it takes until an event occurs
% and some observations may not experience that event before data
% collection ends.
%
% Particularly relevant to Project 12 and potentially Projects 5 and 10.
%
% Do not silently remove unresolved/open observations.
% Clearly define:
% - the event;
% - time origin;
% - censoring date;
% - treatment of reopened observations, if relevant.

Because some \emph{[OBSERVATIONS]} have not experienced
\emph{[EVENT]} by the end of the observation period, we use
\emph{[TIME-TO-EVENT METHOD]} and treat those observations as
right-censored at \emph{[CENSORING POINT]}.
% USE THIS SECTION IF YOU DERIVED/CLASSIFIED INFORMATION THAT NEEDED CHECKING

% =========================================================
% USE THIS SECTION IF YOU DERIVED/CLASSIFIED INFORMATION THAT NEEDED CHECKING
\subsection{Validation}
\label{sec:validation}

% Keep this section when you use:
% - keyword/pattern detection;
% - automated or LLM classification;
% - bot identification;
% - contributor-history reconstruction;
% - reviewer assignment;
% - subsystem classification;
% - review-round reconstruction;
% - workload/rework calculations;
% - issue closure classification;
% - another nontrivial derived measure.
%
% Delete this section only if all important information used in the
% analysis comes directly and unambiguously from GitHub.
%
% NOTE:
% Reliability of qualitative coding was already reported above.
% Do not repeat it here.
%
% Choose validation measures that match the task.
%
% Candidate detection:
% - report precision and, when possible, recall.
%
% Multi-category classification:
% - report overall performance;
% - also report category-level performance when relevant.
%
% Numerical or event reconstruction:
% - compare the derived values/events against manual reconstruction and
%   report an appropriate error or agreement measure.
%
% Do not rely only on overall accuracy when classes are imbalanced.
% Inspect where errors occur and whether they affect important categories.

\paragraph{Validation Procedure.}

We validate \emph{[DERIVED MEASURE / DETECTION PROCEDURE /
CLASSIFICATION / RECONSTRUCTION]} using
\emph{[N]} observations selected through
\emph{[SAMPLING PROCEDURE]}.

For each observation, we compare
\emph{[AUTOMATED OR DERIVED RESULT]} against
\emph{[MANUAL CLASSIFICATION / REPOSITORY HISTORY /
OTHER REFERENCE]}.


\paragraph{Validation Performance.}

We evaluate the procedure using
\emph{[PRECISION / RECALL / F1 / ACCURACY / KAPPA /
ERROR RATE / OTHER APPROPRIATE MEASURE]} and obtain
\emph{[VALUE]}.

When relevant, we also examine performance separately for
\emph{[CATEGORIES / TYPES OF CASES]}.


\paragraph{Use of the Validated Procedure.}

Based on the validation, we
\emph{[RETAIN THE PROCEDURE / REFINE IT AND REVALIDATE /
MANUALLY REVIEW SOME CASES / EXCLUDE AN UNRELIABLE CATEGORY /
OTHER ACTION]}.
% =========================================================
\subsection{Replication Package}
\label{sec:replication}

% Every study must provide enough material to reproduce the construction
% of the analysis dataset and the reported analyses.
%
% At minimum, include:
% - README with reproduction instructions;
% - data-collection and processing scripts;
% - final analysis dataset;
% - analysis scripts;
% - important configuration/decision files.
%
% When applicable, also include:
% - qualitative codebook and coded artifacts;
% - independent IRR labels;
% - validation sample and validation results;
% - LLM prompts, model information, scripts, and outputs used in the study.
%
% Do not include credentials, API tokens, or other secrets.

Our replication package contains
\emph{[LIST THE MAIN DATA, CODE, CODING, AND VALIDATION ARTIFACTS]}
needed to reproduce the study.

\bibliographystyle{IEEEtranN}
\footnotesize{\bibliography{References}}
[1] Y. Chen, T. Zimmermann, and B. Trinkenreich, “Making AI Visible, Not Vanished: How AI Policies Reshape Developer Experience on GitHub,” Aug. 04, 2026. Accessed: Oct. 04, 2026. [Online]. Available: https://arxiv.org/abs/2608.03329v1
\end{document}